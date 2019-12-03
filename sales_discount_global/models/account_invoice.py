# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'discount_type', 'discount_rate')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount for line in self.tax_line_ids)
        #self.amount_total = self.amount_untaxed + self.amount_tax
        #self.amount_discount = sum((line.quantity * line.price_unit * line.discount) / 100 for line in self.invoice_line_ids)

        if self.discount_type == 'percent':
            self.amount_discount += (self.amount_untaxed * self.discount_rate)/100
        else:
            self.amount_discount = self.discount_rate

        self.amount_total = (self.amount_untaxed + self.amount_tax) - self.amount_discount
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    discount_type = fields.Selection([('percent', 'Percentage'),
                                      ('amount', 'Amount')], string='Discount Type',
                                     states={'draft': [('readonly', False)]},
                                     readonly=True, copy=False, default='percent')
    discount_rate = fields.Float('Discount Amount', readonly=True, copy=False,
                                 states={'draft': [('readonly', False)]})
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True,
                                      compute='_compute_amount', copy=False,
                                      track_visibility='always')

    @api.constrains('discount_type', 'discount_rate')
    def check_discount(self):
        for inv in self:
            amount = sum(line.price_subtotal for line in inv.invoice_line_ids)
            if inv.discount_type == 'percent' and inv.discount_rate > 100:
                    raise UserError(_('You can not give more than 100% discount.'))

    @api.multi
    def compute_invoice_totals(self, company_currency, invoice_move_lines):
        total = 0
        total_currency = 0
        for line in invoice_move_lines:
            if self.currency_id != company_currency:
                currency = self.currency_id.with_context(date=self.date_invoice or fields.Date.context_today(self))
                line['currency_id'] = currency.id
                line['amount_currency'] = currency.round(line['price'])
                line['price'] = currency.compute(line['price'], company_currency)
            else:
                line['currency_id'] = False
                line['amount_currency'] = False
                line['price'] = line['price']
            if self.type in ('out_invoice', 'in_refund'):
                total += line['price']
                total_currency += line['amount_currency'] or line['price']
                line['price'] = - line['price']
            else:
                total -= line['price']
                total_currency -= line['amount_currency'] or line['price']
        return total, total_currency, invoice_move_lines
