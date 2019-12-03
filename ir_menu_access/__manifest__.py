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
    'name': 'Security for Menu',
    'version': '1.0',
    'category': 'Tools',
    'summary': """
This module is used to hide menu for user or groups..
""",
    'description': """
This module is used to hide menu for user or groups..
""",
    'price': 15.00,
    'currency': 'EUR',
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "http://www.acespritech.com",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_view.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: