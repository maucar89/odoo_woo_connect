# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def convert_to_currency(self, invoice_data, amount):
        res = 0.0
        res = self.env['res.currency']._compute(invoice_data.currency_id, invoice_data.company_id.currency_id, amount)
        return res

    @api.model
    def create(self, vals):
        """
        Customize: Create new discount with JE's line with configured global discount account.
        """
        context = dict(self._context)
        acc_inv_obj = self.env['account.invoice']
        discount_account_id = False

        company_rec = self.env.user.company_id
        if company_rec and company_rec.global_dis_account_id:
            discount_account_id = company_rec.global_dis_account_id.id
        if discount_account_id:
            if vals.get('invoice_id') and not vals.get('product_id'):
                invoice_data = acc_inv_obj.search([('id', '=', vals.get('invoice_id'))])
                # Check for company currency.
                company_currency = invoice_data.company_id.currency_id
                invoice_currency = invoice_data.currency_id

                # Discount calculation.
                discount = invoice_data.amount_discount
                if company_currency != invoice_currency:
                    discount = self.convert_to_currency(invoice_data, discount)

                # If invoice type is OUT INVOICE.
                if vals.get('debit') and invoice_data and invoice_data.type == 'out_invoice':
                    debit = vals.get('debit')

                    # final_total = debit + discount
                    final_total = debit - discount
                    diff_amount = 0.0
                    if not invoice_data.amount_total and company_currency != invoice_currency:
                        if invoice_data.discount_type and invoice_data.discount_rate:
                            diff_amount = final_total
                        if abs(diff_amount) < 1:
                            diff_amount = diff_amount
                        else:
                            diff_amount = 0.0

                    vals.update({'debit': abs(final_total) if invoice_data.amount_total else 0.0})
                    if company_currency != invoice_currency:
                        vals.update({'amount_currency': invoice_data.amount_total})

                    if invoice_data.discount_type and invoice_data.discount_rate:
                        discount_vals = vals.copy()
                        discount_vals.update({'name': u'Discount',
                                              'debit': abs(discount),
                                              'account_id': discount_account_id})
                        if discount_vals:
                            amt_currency = 0.0
                            if company_currency != invoice_currency:
                                amt_currency = abs(invoice_data.amount_discount)
                            discount_vals.update({'amount_currency': amt_currency})
                            if diff_amount:
                                discount_vals.update({'debit': abs(discount) + diff_amount})
                        res = super(AccountMoveLine, self).create(discount_vals)

                # IF invoice type is OUT REFUND.
                elif vals.get('credit') and invoice_data and invoice_data.type == 'out_refund':
                    credit = vals.get('credit')

                    # final_total = credit + discount
                    final_total = credit - discount
                    diff_amount = 0.0
                    if not invoice_data.amount_total and company_currency != invoice_currency:
                        if invoice_data.discount_type and invoice_data.discount_rate:
                            diff_amount = final_total
                        if abs(diff_amount) < 1:
                            diff_amount = diff_amount
                        else:
                            diff_amount = 0.0

                    vals.update({'credit': abs(final_total) if invoice_data.amount_total else 0.0})
                    if company_currency != invoice_currency and invoice_data.amount_total:
                        vals.update({'amount_currency': (-1) * invoice_data.amount_total})
                    elif company_currency != invoice_currency and not invoice_data.amount_total:
                        vals.update({'amount_currency': 0.0})

                    if invoice_data.discount_type and invoice_data.discount_rate:
                        discount_vals = vals.copy()
                        discount_vals.update({'name': u'Discount',
                                              'credit': abs(discount),
                                              'account_id': discount_account_id})
                        if discount_vals:
                            amt_currency = 0.0
                            if company_currency != invoice_currency:
                                amt_currency = invoice_data.amount_discount
                            discount_vals.update({'amount_currency': amt_currency})
                            if diff_amount:
                                discount_vals.update({'credit': abs(discount) + diff_amount})
                        res = super(AccountMoveLine, self).create(discount_vals)
        else:
            if not discount_account_id and vals.get('discount_type') and vals.get('amount_discount'):
                raise UserError(_('Please set global discount account in configuration.!'))
        res = super(AccountMoveLine, self).create(vals)
        return res
