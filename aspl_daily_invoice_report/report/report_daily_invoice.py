# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from openerp import api, models
from datetime import datetime, date
from operator import itemgetter
import itertools
from collections import defaultdict,OrderedDict


class report_daily_invoice(models.AbstractModel):
    _name = 'report.aspl_daily_invoice_report.report_daily_invoice'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('aspl_daily_invoice_report.report_daily_invoice')
        docargs = {
            'doc_ids': self.env['daily.invoice'].browse(data['id']),
            'doc_model': report.model,
            'docs': self,
            'query': self._query,
            'team_summary': self.team_summary
        }
        return report_obj.render('aspl_daily_invoice_report.report_daily_invoice', docargs)

    def _query(self, obj):
        crm_team = self.env['crm.team']
        product_categ = self.env['product.category']
        res_partner = self.env['res.partner']
        if not obj.customer_ids:
            if obj.partner_categ_ids:
                partner_ids = [customer.id for customer in self.env['res.partner'].search([('customer', '=', True),
                                                                                           ('hcategory_id', 'in', obj.partner_categ_ids.ids)])]
            else:
                partner_ids = [customer.id for customer in self.env['res.partner'].search([('customer', '=', True)])]
        else:
            partner_ids = [customer.id for customer in obj.customer_ids]
        if not obj.sale_team_ids:
            sale_team_ids = [team.id for team in self.env['crm.team'].search([])]
        else:
            sale_team_ids = [team.id for team in obj.sale_team_ids]
        if not obj.to_date:
            to_date = datetime.strftime(date.today(),'%Y-%m-%d')
            to_date = datetime.strptime(to_date,'%Y-%m-%d')
        else:
            to_date = str(obj.to_date) + " 23:59:59"
        if not obj.from_date:
            from_date = datetime.strptime(obj.from_date,'%Y-%m-%d')
            from_date = datetime.strftime(from_date,'%Y-%m-%d')
        else:
            from_date = obj.from_date
        SQL = """SELECT ai.date_invoice as date,
                ai.number as number, ai.team_id, ai.id,
                (ai.amount_untaxed) as product_amt,
                (ai.amount_untaxed) as inv_total,
                rp.id as partner_id
                from account_invoice ai, res_partner rp, account_invoice_line ail
                WHERE rp.id = ai.partner_id
                AND ail.invoice_id = ai.id
                AND ai.date_invoice <= '%s'
                AND ai.date_invoice >= '%s'
                AND ai.partner_id in %s
                AND ai.team_id in %s
                AND ai.state in ('open', 'paid')
                Group BY ai.number, ai.date_invoice,ai.id,
                rp.id, ai.team_id,ai.amount_untaxed"""% (str(to_date), str(from_date),
                    " (%s) " % ','.join(map(str, partner_ids)),
                    " (%s) " % ','.join(map(str, sale_team_ids)))
        self._cr.execute(SQL)
        result = self._cr.dictfetchall()
        for each in result:
            inv_brw = self.env['account.invoice'].browse(each['id'])
            partner_brw = self.env['res.partner'].browse(each['partner_id'])
            partner_name = partner_brw.name or partner_brw.parent_id.name or " "
            team_name = crm_team.browse(each['team_id']).name
            each['name'] = partner_name
            each.update({'tax_amt': inv_brw.amount_tax or 0.00,
                         'team_name': team_name})
            if inv_brw.type == 'out_refund' and each['inv_total']:
                each['inv_total'] = -each['inv_total']
        result = sorted(result, key=itemgetter('date'))
        result = sorted(result, key=itemgetter('name'))
        team_dict = defaultdict(list)
        for team in crm_team.browse(sale_team_ids):
            partner_dict = defaultdict(list)
            for each in result:
                if team.name == each['team_name']:
                    partner_dict[each['name']].append(each)
            if partner_dict:
                team_dict[team.name].append(OrderedDict(sorted(dict(partner_dict).items(), key=lambda t: t[0])))
        final_dict = dict(team_dict)
        return OrderedDict(sorted(final_dict.items(), key=lambda t: t[0]))

    def team_summary(self, obj):
        crm_team = self.env['crm.team']
        if not obj.sale_team_ids:
            sale_team_ids = [team.id for team in self.env['crm.team'].search([])]
        else:
            sale_team_ids = [team.id for team in obj.sale_team_ids]
        data = self._query(obj)
        new_dict = {}
        for team in crm_team.browse(sale_team_ids):
            for d,key in data.items():
                if d == team.name:
                    team_total = 0
                    for k in key:
                        for kv,val in k.iteritems():
                            for value in val:
                                team_total += value['inv_total']
                        new_dict[d] = team_total
        return OrderedDict(sorted(new_dict.items(), key=lambda t: t[0]))
