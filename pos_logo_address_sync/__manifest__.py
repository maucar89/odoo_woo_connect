# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) All rights reserved:
#        (c) 2015  TM_FULLNAME
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses
#
###############################################################################
{
    'name': 'Point of Sale Logo',
    'summary': 'Logo For Every Point of Sale',
    'version': '10.0.1.0.0',
    'description': """This module helps you to set a logo for every point of sale. This will help you to
                 identify the point of sale easily. You can also see this logo in pos screen and pos receipt.""",
    'author': 'Ananthu',
    'website': 'http://www.codersfort.com/',
    'license': 'AGPL-3',
    'category': 'Point Of Sale',
    'depends': [
        'base',
        'point_of_sale',
    ],
    'data': [
        'views/pos_image_view.xml',
        'views/pos_config_view.xml',
        
    ],
    'qweb': [
        'static/src/xml/pos.xml',
        'static/src/xml/pos_ticket_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

