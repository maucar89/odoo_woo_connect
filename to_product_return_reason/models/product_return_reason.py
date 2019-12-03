# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductReturnReason(models.Model):
    _name = 'product.return.reason'
    _inherit = 'mail.thread'
    _description = 'Products Return Reason'

    name = fields.Char(string='Title', required=True, translate=True, track_visibility='onchange', help="The title of the reason,"
                       " e.g. Bad quality, Customer changed mind, etc")
    active = fields.Boolean(string='Active', default=True, help="If unchecked, it will allow you to hide"
                            " the reason without removing it.")

    description = fields.Text(string='Description')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Title of the reason must be unique"),
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the reason should not be the description"),
    ]
