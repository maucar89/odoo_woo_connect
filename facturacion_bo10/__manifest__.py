# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services (<http://www.serpentcs.com>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
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


{
    'name': 'Facturacion computarizada v10',
    'version': '1.1',
    'category': 'Account',
    'description': """
        Datos para la facturacion computarizada y la genercion de libros de venta IVA
    """,
    'author': 'ISBOL',
    'website': 'http://www.odoobolivia.com',
    'depends': ['account','sale'],
    'data': [
        'isbol_control_code_view.xml',
        'isbol_res_partner_view.xml',
        #'isbol_iva_ventas_view.xml',
       # 'account_view.xml',
    ],
    'installable': True,   
    'application': True, 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: