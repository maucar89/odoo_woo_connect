# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

{
    'name': 'Customer Credit Limit',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 1,
    'description': """
        Apps will check the Customer Credit Limit on Sale order and notify to the sales manager
    """,
    'summary':"""Apps will check the Customer Credit Limit on Sale order and notify to the sales manager""",
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://devintellecs.com/',
    'images': ['images/main_screenshot.png'],
    'depends': ['sale','account'],
    'data': [
        "security/security.xml",
        "wizard/customer_limit_wizard_view.xml",
        "views/partner_view.xml",
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price':30,
    'currency':'EUR', 
    'live_test_url':'https://youtu.be/CC-a6QQcxMc',    
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
