# -*- coding: utf-8 -*-

{
    'name': 'Product Rating',
    'version': '0.1',
    'summary': 'Product Rating & Review at Backend',
    'description': """
Features
=============
This specific module allows you manage ratings and reviews of website products at Odoo backend.
    """,
    'category': 'Product',
    'author': 'Aktiv Software',
    'depends': [
        'website_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
