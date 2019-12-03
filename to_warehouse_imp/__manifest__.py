# -*- coding: utf-8 -*-
{
    'name': "Warehouse Improvement",

    'summary': """
        Provide additional improvements to the default Odoo Warehouse/Inventory""",

    'description': """

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    'author': 'T.V.T Marine Automation (aka TVTMA)',
    'website': 'https://www.tvtmarine.com',
    'live_test_url': 'https://v10demo-int.erponline.vn',
    'support': 'support@ma.tvtmarine.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'views/stock_move_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
        'views/stock_warehouse_views.xml',
    ],
    'installable': True,
    'price': 0.0,
    'currency': 'EUR',
    'license': 'OPL-1',
}
