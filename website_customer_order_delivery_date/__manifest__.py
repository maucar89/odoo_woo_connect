# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    "name" : "Customer Order Delivery Date",
    "author" : "AppJetty",
    "version": "10.0.1.0.0",
    "category" : "Website",
    "website" : "https://www.appjetty.com/odoo/odoo-apps.htm",
    "description": "This module is used for add customer order delivery date section at payment page",
    "summary" : "Know when your customers want products delivered",
    "depends" : ['website_sale'],
    "data":[
            'views/customer_order_delivery_config_view.xml',
            'views/sale_order_view.xml',
            'views/template.xml',
    ],
    'images': ['static/description/order-delivery-date-comments-profile.png'],
    # 'price': 10.00,
    # 'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'support': 'support@appjetty.com',
}
