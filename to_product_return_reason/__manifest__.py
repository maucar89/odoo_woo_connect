# -*- coding: utf-8 -*-

{
    'name' : 'Product Return Reasons',
    'version': '1.0.0',
    'author' : 'T.V.T Marine Automation (aka TVTMA)',
    'website': 'https://www.tvtmarine.com',
    'live_test_url': 'https://v10demo-int.erponline.vn',
    'support': 'support@ma.tvtmarine.com',
    'summary': 'Add reason for return products',
    'sequence': 30,
    'category': 'Sales',
    'description':"""
Summary
=======

This module offers a new model for users to define return reason. A return reason consists of the following information:

1. Name: The name of the Return Reason, for example: Bad quality, Customer changed mind, etc
2. Description: Description of the reason

Except that, this module does nothing. It aims to provide the base for other applications to extend.
For example, Point of Sales Return Reason, Stock Return Reason, etc

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,
    'depends': ['mail'],
    'data': [
        'security/module_security.xml',
        'security/ir.model.access.csv',
        'views/products_return_reason.xml',
    ],
    'installable': True,
    'application': False,
    'price': 0.0,
    'currency': 'EUR',
    'license': 'OPL-1',
}
