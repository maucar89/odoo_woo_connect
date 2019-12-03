# -*- coding: utf-8 -*-
{
    'name': "Restriction on Users",

    'summary': """
    Access Customers Allowed Only.
    """,

    'description': """
        - This Module adds restriction on users for accessing Customers for any kind of operation.
        - User can not see the Customers if not allowed by the admin.
        - User can only see and operate on Allowed Customers.
        - Restriction also applies to sales order, purchase order, stock transfer etc.
        - Admin can edit the user and add allowed customers to a specific user.
        - Note : This Restriction is Not Applied On Adminstrator.
    """,

    'author': "Techspawn Solutions",
    'website': "http://www.techspawn.com",

    'category': 'Others',
    'version': '0.1',

    'depends': ['base', 'stock', 'sale', 'product'],

    'data': [
        # 'security/ir.model.access.csv',
        "security/security.xml", 
        'user_view.xml',
    ],
}