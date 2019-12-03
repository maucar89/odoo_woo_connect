# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Hide Vendors Of Product",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "category": "Purchases",
    "summary": "This module useful to hide or show vendors to users.",
    "description": """
    
Easy to hide/show vendors list of product to users.

                    """,    
    "version":"10.0.1",
    "depends" : ["base","purchase","product"],
    "application" : True,
    "data" : ['security/hide_vendor_security.xml',
              'views/product_view.xml',
            ],            
    "images": ["static/description/background.png",],              
    "auto_install":False,
    "installable" : True,
    "price": 8,
    "currency": "EUR"   
}
