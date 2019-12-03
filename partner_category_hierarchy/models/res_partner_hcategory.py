# -*- coding: utf-8 -*-
# © 2017 Nedas Žilinskas <nedas.zilinskas@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerHCategory(models.Model):

    _name = 'res.partner.hcategory'

    name = fields.Char(
        required=True,
    )

    parent_id = fields.Many2one(
        comodel_name='res.partner.hcategory',
        string='Parent Category',
    )

    child_ids = fields.One2many(
        comodel_name='res.partner.hcategory',
        inverse_name='parent_id',
        string='Child Categories',
    )

    partner_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='hcategory_id',
        string='Related Partners',
    )
