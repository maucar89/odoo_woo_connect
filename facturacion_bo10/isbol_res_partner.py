##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api, _
import string
from openerp.exceptions import except_orm, Warning, RedirectWarning

class res_partner(models.Model):
    _inherit = "res.partner"

    nit = fields.Char(string='NIT', default="0")
    res_operador = fields.Char(string='Observaciones', default="0")


    @api.one
    @api.constrains('nit')
    def nit_change(self):
        if self.nit and not self.nit.isdigit() :
            raise Warning(_('Please Enter Valid NIT'))
        if self.nit and len(self.nit) >= 31:
            raise Warning(_('NIT Takes maximum 30 Digits '))

    @api.multi
    def name_get(self):
        result = []
        for inv in self:
            result.append((inv.id, "%s" % (inv.name or '')))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        ids = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]
            query_args = {'name': search_name}
            limit_str = ''
            if limit:
                limit_str = ' limit %(limit)s'
                query_args['limit'] = limit
            search_name = query_args['name']
            self._cr.execute("SELECT p.id FROM res_partner p WHERE (p.name ilike '" + (search_name or '') + "%') OR (p.nit ilike '" + (search_name or '') + "%') ")
            
            ids = map(lambda x: x[0], self._cr.fetchall())
            ids = self.search([('id', 'in', ids)] + args, limit=limit)
            if ids:
                return ids.name_get()
        return super(res_partner, self).name_search(name, args, operator=operator, limit=limit)

 #   _defaults = {	 	

  #      'nit' : 0,

	#	        }	


class account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
        payment_term=False, partner_bank_id=False, company_id=False):
        account_id = False
        payment_term_id = False
        fiscal_position = False
        bank_id = False
        if partner_id:
            p = self.env['res.partner'].browse(partner_id)
            rec_account = p.property_account_receivable
            pay_account = p.property_account_payable
            if company_id:
                if p.property_account_receivable.company_id and \
                        p.property_account_receivable.company_id.id != company_id and \
                        p.property_account_payable.company_id and \
                        p.property_account_payable.company_id.id != company_id:
                    prop = self.env['ir.property']
                    rec_dom = [('name', '=', 'property_account_receivable'), ('company_id', '=', company_id)]
                    pay_dom = [('name', '=', 'property_account_payable'), ('company_id', '=', company_id)]
                    res_dom = [('res_id', '=', 'res.partner,%s' % partner_id)]
                    rec_prop = prop.search(rec_dom + res_dom) or prop.search(rec_dom)
                    pay_prop = prop.search(pay_dom + res_dom) or prop.search(pay_dom)
                    rec_account = rec_prop.get_by_record(rec_prop)
                    pay_account = pay_prop.get_by_record(pay_prop)
                    if not rec_account and not pay_account:
                        action = self.env.ref('account.action_account_config')
                        msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                        raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))

            if type in ('out_invoice', 'out_refund'):
                account_id = rec_account.id
                payment_term_id = p.property_payment_term.id
            else:
                account_id = pay_account.id
                payment_term_id = p.property_supplier_payment_term.id
            fiscal_position = p.property_account_position.id
            bank_id = p.bank_ids and p.bank_ids[0].id or False

        partner = self.env['res.partner'].browse(partner_id)
        result = {'value': {
            'account_id': account_id,
            'payment_term': payment_term_id,
            'fiscal_position': fiscal_position,
            'nit':partner.nit
            
        }}

        if type in ('in_invoice', 'in_refund'):
            result['value']['partner_bank_id'] = bank_id

        if payment_term != payment_term_id:
            if payment_term_id:
                to_update = self.onchange_payment_term_date_invoice(payment_term_id, date_invoice)
                result['value'].update(to_update.get('value', {}))
            else:
                result['value']['date_due'] = False

        if partner_bank_id != bank_id:
            to_update = self.onchange_partner_bank(bank_id)
            result['value'].update(to_update.get('value', {}))

        return result
