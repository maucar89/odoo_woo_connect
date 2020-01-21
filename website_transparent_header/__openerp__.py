# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to odoo
#
#    Copyright (C) 2016 - Today Icap Inc. <http://www.icapsystems.com>
#
###########################################################################
 
{
    'name': 'Website Transparent and Fix Header',
    'summary': 'Website Transparent and Fix Header',
    'description': 'Website Transparent and Fix Header to have cool header look on image and get fixed header when get scrolled down.',
    'version': '1.0',
    'website': 'http://www.icapsystems.com/',
    'category': 'Website',
    'author': 'Icap Inc.',
    'depends': ['website'],
    'data': [
        'views/layout.xml',
    ],
    'images': [
        'static/description/transperent_and_fix_header_icaps.png',
    ],
    'application': False, 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: