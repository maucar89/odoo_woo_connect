# -*- coding: utf-8 -*-

from odoo import api, fields, models


class product_template(models.Model):
    _inherit = 'product.template'

    @api.multi
    def _compute_alternatives_count(self):
        for rec in self:
            rec.alternatives_count = len(rec.alternative_product_ids)

    @api.multi
    def _compute_accessories_count(self):
        for rec in self:
            rec.accessories_count = len(rec.accessory_product_ids)

    alternative_product_ids = fields.Many2many(
        'product.template',
        'product_alternative_rel',
        'src_id',
        'dest_id',
        string='Alternative Products',
        help='Appear on the product page',
    )
    accessory_product_ids = fields.Many2many(
        'product.product',
        'product_accessory_rel',
        'src_id',
        'dest_id',
        string='Accessory Products',
        help='Appear on the shopping cart',
    )
    alternatives_count = fields.Integer(
        compute='_compute_alternatives_count',
        string='# of alternatives',
    )
    accessories_count = fields.Integer(
        compute='_compute_accessories_count',
        string='# of accessories',
    )
