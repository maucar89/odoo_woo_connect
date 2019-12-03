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

from odoo import models, fields, api,_
from datetime import datetime, date


class daily_invoice(models.TransientModel):
    _name = "daily.invoice"

    to_date = fields.Date(string="To Date", default=datetime.today())
    from_date = fields.Date(string="From Date", default=datetime.today())
    partner_categ_ids = fields.Many2many('res.partner.hcategory', string="Partner Category")
    customer_ids = fields.Many2many('res.partner',
                                    'daily_invoice_customer_rel',
                                    'daily_inv_id', 'cust_id',
                                    string="Customers", domain=[('customer', '=', True)])
    sale_team_ids = fields.Many2many('crm.team',
                                    'daily_invoice_crm_team_rel',
                                    'team_daily_inv_id', 'team_id',
                                    string="Sale Teams")

    @api.multi
    def action_print(self):
        datas = {
            'id': self.id
        }
        return self.env['report'].get_action(self,
                                              'aspl_daily_invoice_report.report_daily_invoice',
                                              data=datas)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: