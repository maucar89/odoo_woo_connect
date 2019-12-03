# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################
{
    "name" : " Dynamic / Global Export Excel Report For all Application-xls",
    "version" : "1.0",
    'sequence':1,
    'category': 'Tools',
    'summary': 'Apps will Export excel view for all application like: Sale, Purchase, Invoice, Picking, Hr, Project, MRP and New Custom Application',
    "depends" : ['sale','purchase','sale_stock'],
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com/',
    'images': ['images/main_screenshot.png'],
    "description": """
        Apps will Export excel view for all application like: Sale, Purchase, Invoice, Picking, Hr, Project, MRP and New Custom Application
    """,
    "data" : [
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/dev_export_views.xml',
            'wizard/dev_export_wizard_view.xml',
#            'data/sale_order_data.xml',
#            'data/purchase_order_data.xml',
#            'data/account_invoice_data.xml',
    ],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':35.0, 
    'currency':'EUR', 
    'live_test_url':'https://youtu.be/JA7q6naSmW0',    
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
