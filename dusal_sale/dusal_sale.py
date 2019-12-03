# -*- coding: utf-8 -*-
##############################################################################
#
#    Addon for Odoo sale by Dusal.net
#    Copyright (C) 2015 Dusal.net Almas
#
##############################################################################
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    print_product_image = fields.Boolean(string='Print product image', readonly=False, index=True, help="If this checkbox checked then print product images on Sales order & Quotation", default=True)
    image_size = fields.Selection([('small', 'Small'), ('medium', 'Medium'), ('big', 'Big')], string='Image sizes', help="Choose an image size here", index=True, default='small')
    print_line_number = fields.Boolean(string='Print line number', readonly=False, index=True, help="Print line number on Sales order & Quotation", default=False)

class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    product_image = fields.Binary(string="Image", related="product_id.image")
    product_image_medium = fields.Binary(string="Image", related="product_id.image_medium")
    product_image_small = fields.Binary(string="Image", related="product_id.image_small")

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    print_product_image = fields.Boolean(string='Print product image', readonly=False, index=True, help="If this checkbox checked then print product images on Invoice", default=True)
    print_line_number = fields.Boolean(string='Print line number', readonly=False, index=True, help="Print line number on Invoice", default=False)

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    product_image = fields.Binary(string="Image", related="product_id.image")
