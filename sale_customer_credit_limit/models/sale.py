# -*- coding: utf-8 -*-
# © 2017 Tobias Zehntner
# © 2017 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date
from odoo import api, exceptions, fields, models, SUPERUSER_ID


class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    company_currency_id = fields.Many2one('res.currency',
                                          compute='get_currency')
    default_credit_limit = fields.Monetary(
        'Default Customer Credit Limit *',
        related='company_id.default_credit_limit',
        currency_field='company_currency_id')

    def get_currency(self):
        self.company_currency_id = self.env.user.company_id.currency_id


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Add 'To Approve' to Sale Order states
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('approve', 'To Approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')])

    user_is_manager = fields.Boolean('User is manager',
                                     compute='compute_manager')

    @api.multi
    @api.depends('state')
    def compute_manager(self):
        current_user = self.env.user
        manager_group = 'sales_team.group_sale_manager'
        for order in self:
            employee = self.env['hr.employee'].search([('user_id', '=', order.user_id.id)], limit=1)
            if current_user.id == SUPERUSER_ID:
                order.user_is_manager = True
            else:
                if not employee:
                    raise exceptions.ValidationError(
                        'The user %s has no employee defined. Please contact '
                        'the Administrator.' % order.user_id.name)
                if not employee.parent_id:
                    raise exceptions.ValidationError(
                        'The employee %s has no manager defined. Please contact '
                        'the Administrator.' % employee.name)
                manager = employee.parent_id.user_id
                order.user_is_manager = manager == current_user \
                                        or current_user.has_group(manager_group)

    @api.multi
    def action_confirm(self):
        for order in self:
            if not order._context.get('exceed_credit_limit', False):
                customer = order.partner_id

                credit_limit = order.partner_id.credit_limit
                credit_limit_currency = \
                    order.partner_id.credit_limit_currency_id

                order_amount = order.currency_id.compute(order.amount_total,
                                                         credit_limit_currency)
                open_credit = 0

                past_due_invoices = self.env['account.invoice'].search([
                    ('type', '=', 'out_invoice'),
                    ('company_id', '=', order.company_id.id),
                    ('partner_id', '=', customer.id),
                    ('state', 'in', ['open']),
                    '|', ('payment_term_id', '=', False),
                    ('date_due', '<', date.today()),
                ])
                for invoice in past_due_invoices:
                    amount = invoice.currency_id.compute(invoice.residual,
                                                         credit_limit_currency)
                    open_credit += amount

                exceeded_credit = (open_credit + order_amount) - credit_limit

                if self._context.get('force_exceed_limit', False) or \
                        (open_credit > 0 and exceeded_credit > 0):
                    context = {'credit': {'open_credit': open_credit,
                                          'exceeded_credit': exceeded_credit}}
                    return {
                        'context': context,
                        'type': 'ir.actions.act_window',
                        'name': 'Above Customer Credit Limit',
                        'res_model': 'sale.customer.credit.limit.wizard',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'view_id': self.env.ref(
                            'sale_customer_credit_limit.credit_limit_wizard').id,
                        'target': 'new',
                    }
                else:
                    super(SaleOrder, self).action_confirm()
            else:
                super(SaleOrder, self).action_confirm()
        return True

    @api.multi
    def action_approve(self):
        # Approve Sale Order
        for order in self:
            if order.user_is_manager:
                context = {'exceed_credit_limit': True}
                order.with_context(context).action_confirm()
            else:
                raise exceptions.ValidationError(
                    'You do not have the rights to approve this Sale Order')

    # 'Set to Draft' function for state 'to approve'
    @api.multi
    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['approve'])
        if orders:
            orders.write({
                'state': 'draft',
                'procurement_group_id': False,
            })
            orders.mapped('order_line').mapped('procurement_ids').write(
                {'sale_line_id': False})
        else:
            super(SaleOrder, self).action_draft()
