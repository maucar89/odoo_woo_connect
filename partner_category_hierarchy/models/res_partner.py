# -*- coding: utf-8 -*-
# © 2017 Nedas Žilinskas <nedas.zilinskas@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    hcategory_id = fields.Many2one(
        comodel_name='res.partner.hcategory',
        string='Category',
    )
