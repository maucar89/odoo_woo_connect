# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from odoo import fields, models, api, _

class res_users(models.Model):
    _inherit = 'res.users'

    is_allow_payments = fields.Boolean('Allow Payments')
    is_allow_discount = fields.Boolean('Allow Discount')
    is_allow_qty = fields.Boolean('Allow Qty')
    is_edit_price = fields.Boolean('Allow Edit Price')
    is_allow_remove_orderline = fields.Boolean('Allow Remove Order Line')


class pos_order(models.Model):
    _inherit = 'pos.order'

    def get_cashier_value(self):
        user = self.env['res.users'].browse(self.id)
        lst = [user.is_allow_payments,user.is_allow_qty,user.is_allow_discount,user.is_edit_price,user.is_allow_remove_orderline]   
        return lst
