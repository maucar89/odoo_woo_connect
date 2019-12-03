# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api,_
from pygments.lexer import _inherit


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self._context.get('partner_categ_ids'):
            args = args or []
            new_args = []
            if self._context.get('partner_categ_ids')[0][2]:
                new_args += [('hcategory_id', 'in', self._context.get('partner_categ_ids')[0][2])]
                recs = self.sudo().browse()
                if not recs:
                    recs = self.sudo().search([('name', operator, name)] +new_args, limit=limit)
                return recs.name_get()
            else:
                return super(res_partner, self).name_search(name, args=args, operator=operator, limit=limit)
        return super(res_partner, self).name_search(name, args=args, operator=operator, limit=limit)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: