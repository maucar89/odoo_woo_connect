# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

{
    'name': 'Sale Delivery Notes ',
    'version': '1.0',
    'sequence':1,
    'category': 'Sale',
    'description': """
                This apps will help to pass the delivery notes from sale order to delivery order and also print notes in delivery order. 
         
         Sale delivery, Sale notes, Delivery Notes, Sale delivery notes, Delivery reminder,  Notes pass to delivery , Picking notes,
         Delivery driver notes, Shipment notes, picking slip, pick up notes
    """,
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'summary':'Add delivery notes in sale order and pass to the delivery order.',
    'website': 'http://www.devintellecs.com',
    'depends': ['sale','sale_stock'],
    'data': [
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/report_picking_operation.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':15.0,
    'currency':'EUR',
    'live_test_url':'https://youtu.be/fcifWR9A5J8',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
