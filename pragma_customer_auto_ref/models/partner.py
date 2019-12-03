# -*- coding: utf-8 -*-

#
#    odoo extensions
#
#    © 2017-now Josef Kaser (<http://www.pragmasoft.de>).
#
#   See the LICENSE file in the toplevel directory for copyright
#   and license details.
#


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _name = _inherit

    @api.model
    def create(self, vals):
        if 'customer' in vals and vals['customer']:
            vals['ref'] = self.env['ir.sequence'].get('customer.number')

        return super(ResPartner, self).create(vals)
