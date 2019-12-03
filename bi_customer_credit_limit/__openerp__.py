# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 BrowseInfo(<http://www.browseinfo.in>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Customer Credit Warning on Sales and Invoice',
    'version': '10.0.0.1',
    'sequence': 4,
    'summary': 'Customer credit limit warning agaist account receivable amount',
    'description': """ This openerp module show credit limit on partner, Account receivable amount agaist credit limit, Partner credit limit Warning, customer credit limit Warning, Total Account Receivable amount on sale. AR on sales,Partner AR agaist credit limit, ovedue warning, customer warning , customer credit warning,Customer Credit limit Warning on Sales, Sales Credit Warning Against AR.Payment credit warning, Account limit warning, Client overdemand warning, Client overlimit warning.
    """,
    'category' : 'Sales',
    'author': 'BrowseInfo',
    'website': '',
    'depends': ['base','sale','account'],
    'data': [
             "views/sale_order.xml"
             ],
	'qweb': [
		],
    'demo': [],
    'price': '20',
    'currency': "EUR",
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "images":['static/description/banner.png'],
}

