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


class ir_menu_access(models.Model):
    _name = 'ir.menu.access'

    group_ids = fields.Many2many('res.groups', 'rel_menu_access_group',
                                 'access_id', 'group_id', 'Groups')
    user_ids = fields.Many2many('res.users', 'rel_menu_access_users',
                                 'access_id', 'user_id', 'Users')
    menu_ids = fields.Many2many('ir.ui.menu', 'rel_menu_access_menus',
                                 'access_id', 'menu_id', 'Menus')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: