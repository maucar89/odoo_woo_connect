# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_auto_fiscal_postion(self):
        self.property_account_position_id = self.env['account.fiscal.position'].get_fiscal_position(self.id)
        fp = self.env['account.fiscal.position']._get_fpos_by_region(self.country_id.id, self.state_id.id, self.zip, True)
        if fp and not self.vat:
            raise ValidationError(_("Vat is required. Please enter the valid vat number."))

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        res.get_auto_fiscal_postion()
        return res

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if vals and vals.get('country_id'):
            self.get_auto_fiscal_postion()
        return res

    @api.onchange('country_id')
    def _onchange_country_id(self):
        res = super(ResPartner, self)._onchange_country_id()
        self.property_account_position_id = False
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
