# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Bank Statement Line Reconciliation',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'summary': 'OCA Financial Reports',
    'author': "Camptocamp, Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/account-financial-reporting',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_accountant',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
        # Wizard
        'wizard/account_bank_statement_line_reconciliation_wizard.xml',
    ],
    'installable': True,
    'application': False,
}
