# -*- coding: utf-8 -*-
# © 2016 Tobias Zehntner
# © 2016 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, exceptions, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Monetary(string='Credit Limit',
        default=lambda self: self.env.user.company_id.default_credit_limit,
        currency_field='credit_limit_currency_id',
        help='Total amount this customer is allowed to purchase on credit.')

    credit_limit_currency_id = fields.Many2one(
        "res.currency", related='property_product_pricelist.currency_id',
        string="Credit Limit Currency", readonly=True, required=True)

    @api.constrains('credit_limit')
    @api.onchange('credit_limit')
    @api.multi
    def check_amount(self):
        for customer in self:
            if customer.credit_limit < 0:
                raise exceptions.Warning(
                    'Credit Limit cannot be a negative number')

    @api.multi
    def write(self, vals):

        # if we updated the pricelist, we should also update the credit limit
        # to match with the new currency. Only if the limit was not also updated
        if vals.get('property_product_pricelist', False) and not\
                vals.get('credit_limit', False):

            for partner in self:
                current_currency = partner.credit_limit_currency_id
                new_currency = self.env['product.pricelist'].browse(
                    vals.get('property_product_pricelist')).currency_id

                new_amount = current_currency.compute(
                    partner.credit_limit,
                    new_currency)

                partner.credit_limit = new_amount

        return super(ResPartner, self).write(vals)
