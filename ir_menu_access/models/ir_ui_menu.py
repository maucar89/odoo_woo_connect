# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
#################################################################################

from openerp import models, fields, api, _


class ir_ui_menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        if args is None:
            args = []
        group_ids = self.env['res.groups'].search([('users', 'in', [self._uid])])
        ima_ids = self.env['ir.menu.access'].search(['|', ('group_ids', 'in', [group_id.id for group_id in group_ids]),
                                                          ('user_ids', 'in', [self._uid])])
        if ima_ids:
            menu_ids = []
            for ima in ima_ids:
                menu_ids += map(lambda a: a.id, ima.menu_ids)
            args += [('id', 'not in', menu_ids)]
        return super(ir_ui_menu, self).search(args, offset, limit,
                                              order, count=count)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: