# -*- coding: utf-8 -*-
{
    'name': 'List Due Invoices',
    'version': '1.0',
    'summary': 'List Due Invoices',
    'description': """
List Due Invoices
=================

This module lists (customer or vendor) invoices on or before the due date selected.


Keywords: Odoo Due Customer Invoices, Odoo Due Vendor Invoices, Odoo Due Supplier Invoices,
Odoo Due Vendor Bills, Odoo Due Invoices
""",
    'category': 'Accounting',
    'author': 'MAC5',
    'contributors': ['Michael Aldrin C. Villamar'],
    'website': 'https://apps.odoo.com/apps/modules/browse?author=MAC5',
    'depends': ['account'],
    'data': [
        'wizard/account_invoice_due_list_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/list_due_invoices_result.png'],
}
