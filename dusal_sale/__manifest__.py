# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Dusal.net
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Sales order and Quotation extension with product images and line numbers",
    'summary': "Sales order line numbering, product photo, product image, sale order",
    "version": "3.3",
    "description": """
        Add line numbering, image (product picture, product photo) of products to list and print (pdf) of sales order and quotation product line. Image size is selectable. Support and contact email: almas@dusal.net Feel free to contact us.
    """,
    'author': 'Dusal Solutions',
    'category': 'Sales',
    'support': 'almas@dusal.net',
    # 'website' : 'http://dusal.net',
    'license': 'Other proprietary',
    'price': 10.00,
    'currency': 'EUR',
    'images': ['static/images/main_screenshot.png',
               'static/images/screenshot1.png',
               'static/images/screenshot2.png',
               # 'static/images/edit_line_screenshot.png',
               'static/images/screenshot.png'],
    "depends": [
        "sale",
        "product",
        "dusal_web_tree_image",
        "website_quote",
    ],
    "data": [
        'data.xml',
        'views/views.xml',
        'views/reports.xml',
        'views/website_quote_template.xml',
    ],
    "auto_install": False,
    "installable": True,
}
