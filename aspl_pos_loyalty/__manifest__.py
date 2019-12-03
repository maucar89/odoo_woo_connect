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
{
    'name': 'POS Loyalty',
    'category': 'Point of Sale',
    'summary': 'This module allows customers earn loyalty points.',
    'description': """
This module allows customers earn loyalty points.
""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'price': 20.00, 
    'currency': 'EUR',
    'version': '1.0.1',
    'depends': ['base', 'point_of_sale', 'sale'],
    'images': ['static/description/main_screenshot.png'],
    "data": [
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'views/loyalty_config_view.xml',
        'views/loyalty_view.xml',
        'views/point_of_sale.xml',
        'views/aspl_pos_loyalty.xml'
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: