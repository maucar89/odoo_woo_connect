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

{
    'name': 'POS Cash In-Out',
    'version': '1.0',
    'category': 'Point of Sale',
    'description': """
This module allows user to put money in and take money out facility in pos frontend.
""",
    'summary': 'This module allows user to put money in and take money out facility.',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'price': 25.00,
    'currency': 'EUR',
    'depends': ['base', 'point_of_sale'],
    "data": [
        'views/pos_cash_inout.xml'
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: