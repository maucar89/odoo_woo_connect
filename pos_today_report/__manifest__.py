# -*- coding: utf-8 -*-

{
    'name': 'POS Today Report',
    'version': '1.4',
    'sequence': 0,
    'summary': 'Add Action print report POS today to POS Dashboard kanban',
    'depends': [
        'account', 'point_of_sale'
    ],
    'data': [
        'report/template_page.xml',
        'report/pos_today_report.xml',
        'report/pos_yesterday_report.xml',
        'report/report.xml',
        'view/pos_config.xml',
    ],
    'application': True,
    'price': '0',
    "currency": 'EUR',
    'images': [],
    'support': 'thanhchatvn@gmail.com'
}
