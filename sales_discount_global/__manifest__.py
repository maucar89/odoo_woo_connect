# -*- coding: utf-8 -*-

{
    'name': 'Sales Discount with Journal Entry',
    'version': '1.0',
    'category': 'sales',
    'summary': 'Apply global discount in Sale & Invoice with journal entries',
    'sequence': 3,
    'description': """
Sales Discount with Journal Entry
=======================
    * Module to manage apply global discount in sale order & invoice.
    * Apply global discount by Fixed Price or Percentage.
    * Discount manage as a fixed price or percentage.
    * Discount display in journal entry with configured account.
    * Support multi currency feature for applied discount.
""",
    'author': 'AVP Technolabs',
    'company': 'AVP Technolabs',
    'price': 20.00,
    'currency': 'EUR',
    'website': 'https://www.avptechnolabs.com',
    'license': 'OPL-1',
    'depends' : ['sale', 'stock'],
    'data': [
        'views/sale_view.xml',
        'views/account_invoice_view.xml',
        'views/invoice_report.xml',
        'views/sale_order_report.xml',
        'views/res_config_view.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.png'],
    'qweb': [],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
