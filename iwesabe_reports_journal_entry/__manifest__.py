# -*- coding: utf-8 -*-
{
    'name': 'Journal Entry Report',
    'version': '1.1',
    'author': 'iWesabe',
    'summary': 'Print a particular Journal Entry',
    'description': """  """,
    'category': 'Accounting',
    'website': 'http://iwesabe.com/',

    'depends': ['base', 'account_accountant',
                ],

    'data': [
        'views/report_journal_entry.xml'
    ],

    'qweb': [],
    'images': ['static/description/iWesabe-Apps-Journal-Entry-Report.png'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
