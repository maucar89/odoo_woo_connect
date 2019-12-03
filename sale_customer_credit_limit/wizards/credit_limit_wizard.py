# -*- coding: utf-8 -*-
# © 2017 Tobias Zehntner
# © 2017 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, exceptions, fields, models


class SaleCustomerCreditLimitWizard(models.TransientModel):
    _name = 'sale.customer.credit.limit.wizard'

    sale_order = fields.Many2one('sale.order', compute='get_vals')
    credit_limit_currency_id = \
        fields.Many2one('res.currency',
                        related='sale_order.partner_id.credit_limit_currency_id',
                        readonly=1)
    so_currency_id = \
        fields.Many2one('res.currency',
                        related='sale_order.pricelist_id.currency_id',
                        readonly=1)
    partner_id = fields.Many2one('res.partner', related='sale_order.partner_id',
                                 readonly=1)
    credit_limit = fields.Monetary('Credit Limit',
                                   related='sale_order.partner_id.credit_limit',
                                   readonly=1,
                                   currency_field='credit_limit_currency_id')
    order_amount = fields.Monetary('Order Amount',
                                   related='sale_order.amount_total',
                                   readonly=1,
                                   currency_field='so_currency_id')

    open_credit = fields.Monetary('Overdue Invoices', compute='get_vals',
                                  currency_field='credit_limit_currency_id')
    exceeded_credit = fields.Monetary('Exceeded Credit', compute='get_vals',
                                      currency_field='credit_limit_currency_id')

    @api.multi
    @api.depends('credit_limit_currency_id')
    def get_vals(self):
        self.ensure_one()
        self.sale_order = self.env['sale.order'].browse(
            self._context['active_id'])

        vals = self._context.get('credit')
        self.open_credit = vals.get('open_credit')
        self.exceeded_credit = vals.get('exceeded_credit')

    @api.multi
    def action_exceed_limit(self):
        self.ensure_one()
        order = self.sale_order
        if order.user_is_manager:
            # Skip approval process for Sale Managers
            context = {'exceed_credit_limit': True}
            order.with_context(context).action_confirm()
        else:
            # Set order 'To Approve' and notify manager
            order.state = 'approve'

            employee = self.env['hr.employee'].search(
                [('user_id', '=', order.user_id.id)], limit=1)

            order.message_subscribe([employee.parent_id.user_id.partner_id.id])

            credit_limit = '%.2f' % self.credit_limit
            open_credit = '%.2f' % self.open_credit
            order_amount = '%.2f' % self.order_amount
            exceeded_credit = '%.2f' % self.exceeded_credit
            symbol = self.credit_limit_currency_id.symbol
            so_symbol = self.so_currency_id.symbol

            subject = '%s needs approval' % order.name
            message = '''
            The Sale Order %s exceeds the customer credit limit and needs approval by %s:
            <ul>
                <li>Customer: %s</li>
                <li>Credit Limit: %s %s</li>
                <li>Overdue Invoices: %s %s</li>
                <li>Order Amount: %s %s</li>
                <li>Exceeded Credit: <span style="color:red">%s %s</span</li>
            </ul>
            ''' % (order.name, employee.parent_id.name,
                   self.partner_id.name,
                   credit_limit, symbol,
                   open_credit, symbol,
                   order_amount, so_symbol,
                   exceeded_credit, symbol)

            order.message_post(message, subject=subject,
                               subtype='mail.mt_comment',
                               type='comment')
