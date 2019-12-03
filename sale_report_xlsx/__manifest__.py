# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2018 darkknightapps@gmail.com
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
{
    'name': "Sales Report - Excel",
    'summary': """
        This module allows to export sales report based on different filters """,
    'description': """
=======================================================================================
        * Filter by date range
        * Filter by order status
        * Filter by customer
        * Filter by sales person
        * Filter by sales channel
        * Filter by payment terms
        * Filter by products

""",

    'author': 'Dark Knight',
    'website': '',
    'support': 'darkknightapps@gmail.com',
    'category': 'Reporting',
    'version': '1.0',
    'depends': ['sale', 'report_xlsx'],
    'data': [
        'report/sale_reports.xml',
        'wizard/sale_report_export_views.xml',
    ],
    'demo': [
    ],
    'images': ['static/description/SaleReportWizard.png'],
    'price': 10.00,
    'currency': 'EUR',
    'license': 'OPL-1',
    'installable': True,
    'application': False,
}
