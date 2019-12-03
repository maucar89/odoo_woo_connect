# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import date, datetime
from openerp import models, fields, exceptions, api, _
from openerp.exceptions import UserError

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    credit_limit_id = fields.Integer(string="Credit Limit")
    total_receivable = fields.Integer(string="Amount Receivable",compute='_compute_total_receivable')

    #res_partner_id = fields.Many2one('res.partner')
    #credit_limit_id = fields.Float(string='Credit Limit',related='res_partner_id.credit_limit',readonly=True)
    
    @api.multi
    def _compute_total_receivable(self):
        self.update({'total_receivable':self.partner_id.credit})
            

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        account_id = False
        payment_term_id = False
        fiscal_position = False
        bank_id = False
        warning = {}
        domain = {}
        company_id = self.company_id.id
        p = self.partner_id if not company_id else self.partner_id.with_context(force_company=company_id)
        type = self.type
        if p:
            rec_account = p.property_account_receivable_id
            pay_account = p.property_account_payable_id
            if not rec_account and not pay_account:
                action = self.env.ref('account.action_account_config')
                msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))

            if type in ('out_invoice', 'out_refund'):
                account_id = rec_account.id
                payment_term_id = p.property_payment_term_id.id
            else:
                account_id = pay_account.id
                payment_term_id = p.property_supplier_payment_term_id.id

            delivery_partner_id = self.get_delivery_partner_id()
            fiscal_position = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id, delivery_id=delivery_partner_id)

            # If partner has no warning, check its company
            if p.invoice_warn == 'no-message' and p.parent_id:
                p = p.parent_id
            if p.invoice_warn != 'no-message':
                # Block if partner only has warning but parent company is blocked
                if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
                    p = p.parent_id
                warning = {
                    'title': _("Warning for %s") % p.name,
                    'message': p.invoice_warn_msg
                    }
                if p.invoice_warn == 'block':
                    self.partner_id = False

        self.account_id = account_id
        self.payment_term_id = payment_term_id
        self.date_due = False
        self.fiscal_position_id = fiscal_position
        self.credit_limit_id = self.partner_id.credit_limit
        self.total_receivable = self.partner_id.credit
        

        if type in ('in_invoice', 'out_refund'):
            bank_ids = p.commercial_partner_id.bank_ids
            bank_id = bank_ids[0].id if bank_ids else False
            self.partner_bank_id = bank_id
            domain = {'partner_bank_id': [('id', 'in', bank_ids.ids)]}

        res = {}
        if warning:
            res['warning'] = warning
        if domain:
            res['domain'] = domain
        return res


    @api.multi
    def action_invoice_open(self):
        res = super(account_invoice, self).action_invoice_open()
        partner = self.partner_id
        
        account_move_line = self.env['account.move.line']
        account_move_line = account_move_line.\
            search([('partner_id', '=', partner.id),
                    ('account_id.user_type_id.name', 'in',
                     ['Receivable', 'Payable'])
                    ])
                    
        debit, credit = 0.0, 0.0
        for line in account_move_line:
            credit += line.debit
            debit += line.credit
                
        for order in self:
            
            
            if (credit - debit + self.amount_total) > partner.credit_limit:
                if not partner.override_limit:
                    order.write({'credit_limit_id':partner.credit_limit})
                    raise UserError(_('You can not confirm invoice, Please check partner credit and amount receivable'))
                    return False
                else:
                    partner.write({
                        'credit_limit': credit - debit + self.amount_total})
                    order.write({'credit_limit_id':partner.credit_limit})
                    return True
            else:
                order.write({'credit_limit_id':partner.credit_limit})
                return True
        return res
            
class res_partner(models.Model):
    _inherit = 'res.partner'

    #res_credit_limit = fields.Integer(string="Credit Limit")
    override_limit = fields.Boolean(string="Allow Override")
    
