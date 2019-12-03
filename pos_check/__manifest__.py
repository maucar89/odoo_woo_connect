# -*- coding: utf-8 -*-
{
    'name': 'POS Check',
    'version': '10.0.1.0.1',
    'summary': """Allow users to pay by check and to record details about the check paid
 directly from the user interface""",
    'category': 'Point Of Sale',
    'license': 'LGPL-3',
    'author': "Mplus Software",
    'website': "http://mplus.software",
    'depends': ['point_of_sale'],
    'data': [
        'wizard/pos_payment.xml',
        'views/pos_check.xml',
        'views/pos_check_view.xml',
        'views/account_journal_view.xml',
        'views/pos_order_view.xml',
    ],
    'images': [
        'static/description/app.png'
    ],
    'installable': True,
    'application': True,
    'qweb': ['static/src/xml/pos_check.xml'],
}
