# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################
{
    'name': 'Stock Inventory Real Time Report(PDF/XLS)',
    'version': '10.0.1.1',
    'sequence':1,
    'category': 'Stock',
    'description': """
        Print Stock Inventory Report -Beginning, Received, Sales, Internal, Adjustment, Ending
        
        Stock Inventory Real Time Report(PDF/XLS) odoo apps Tags
        Inventory Report, Beginning Stock, Received Stock, Sales Stock, Internal Stock , Adjustment Stock, Ending  Stock
        Stock Inventory Real Time Report(PDF/XLS)
        Easily generate stock inventory report in Excel
        Easily generate stock inventory report in XLS
        Easily generate stock inventory report in PDF
        generate stock inventory report in Excel
        generate stock inventory report in XLS
        generate stock inventory report in PDF
        easily generate real time stock inventory in Excel
        easily generate real time stock inventory in PDF
        easily generate real time stock inventory in XLS
        stock inventory report in excel
        stock inventory report in pdf
        stock inventory in XLS
        stock inventory real time report in Excel       
        stock inventory real time report in pdf
        stock inventory real time report in xls
        Easily generate PDF Report And XLS file for stock valuation inventory
        Easily generate PDF Report in detail with and without product.
        Easily generate XLS file for stock valuation with summarized data.
        Generate Stock Inventory Real Time Report - PDF / XLS by specific dates
        Generate Stock Inventory Report for Particular Date Range 
        Generate Report in PDF , XLS , Excel Format  
        Stock inventory report
        Odoo stock inventory report
        Odoo stock report
        Odoo stock inventory real time report
        Odoo stock inventory report in excel
        Odoo stock inventory report in pdf
        Odoo stock inventory report in XLS
        
        
        """,
    'summary': 'Print Stock Inventory Report -Beginning, Received, Sales, Internal, Adjustment, Ending',
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com/',
    'depends': ['sale_stock','purchase'],
    'data': [
        'wizard/dev_stock_inventory_views.xml',
        'report/stock_inventory_template.xml',
        'report/dev_stock_inventory_menu.xml',
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
    'price':49.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
