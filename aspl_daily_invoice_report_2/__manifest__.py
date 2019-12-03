# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    "name" : "Daily Invoice Report",
    'summary' : "This report will show daily invoices of customer \
                grouped by sale teams.",
    "version" : "1.0",
    "description": """
        This report will show daily invoices of custome
                grouped by sale teams.
    """,
    'author' : 'Acespritech Solutions Pvt. Ltd.',
    'category' : 'Accounting',
    'website' : 'http://www.acespritech.com',
    'price': 15,
    'currency': 'EUR',
    'images': ['static/description/main_screenshot.png'],
    "depends" : ['base', 'account', 'account_accountant', 'sale', 'crm', 'partner_category_hierarchy'],
    "data" : [
        'views/report.xml',
        'views/daily_invoice_view.xml',
        'views/daily_invoice_report_template.xml',
    ],
    "auto_install": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: