# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import Warning

class ResUsers(models.Model):
    _inherit = 'res.users'

    user_restricted_ids = fields.Many2many(
        'res.partner',
        'customer_user_id',
        'user_id',
        'partner_id',
        'Allowd User')

    