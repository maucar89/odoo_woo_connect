# -*- coding: utf-8 -*-
{
    'name': 'Evo Sale Order Scheduling',
    'version': '1.0',
    'category': 'Sale',
    'summary': 'Evo Scheduling',
    'website': 'www.evozard.com',
    'author': 'Evozard',
    'description': """
		Schedule date on Sale order and Delivery.
""",
    'depends': ['sale', 'stock'],
    'data': [
        'views/sale_order_view.xml',
        'views/picking_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
