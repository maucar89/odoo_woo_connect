# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

from openerp import api, fields, models, _


class customer_limit_wizard(models.TransientModel):
    _name = "customer.limit.wizard"
    
    @api.multi
    def set_credit_limit_state(self):
        order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        order_id.state = 'credit_limit'
        order_id.exceeded_amount = self.exceeded_amount
        order_id.send_mail_approve_credit_limit()
        self.partner_id.credit_limit_on_hold = self.credit_limit_on_hold
        return True
    
    current_sale = fields.Float('Current Quotation')
    exceeded_amount = fields.Float('Exceeded Amount')
    credit = fields.Float('Total Receivable')
    partner_id = fields.Many2one('res.partner',string="Customer")
    credit_limit = fields.Float(related='partner_id.credit_limit',string="Credit Limit")
    sale_orders = fields.Char("Sale Orders")
    invoices = fields.Char("Invoices")
    credit_limit_on_hold = fields.Boolean('Credit Limit on Hold')
    
    
    
            
