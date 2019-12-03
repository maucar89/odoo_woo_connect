from odoo import api, fields, models

class product(models.Model):
    _inherit='product.product'
    
    is_promo_product=fields.Boolean("Is Promotion Product")
