# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Reporte de Estado de Cuenta - Clientes',
    'version': '10.0.1.0',
    'sequence': 1,
    'category': 'Account',
    'description': """
        Este modulo le ayudará a imprimir estado de cuenta de clientes en reporte xls
""",
    'summary':'generar estado de cuenta clientes en xls',
    'author': 'Ing. Mauricio C.',
    'website': 'http://www.odoo.org.bo',
    'depends': ['sale','account', 'partner_category_hierarchy'],
    'data': [
        'wizard/invoice_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
