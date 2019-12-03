# -*- coding: utf-8 -*-
{
    "name": "Product Accessories & Alternatives",
    "version": "10.0.1.0.1",
    "category": "Sales",
    "author": "Odoo Tools",
    "website": "https://odootools.com",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "product"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "wizard/product_accessories_wizard.xml",
        "wizard/product_alternatives_wizard.xml",
        "views/product_template.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "Manage accessories and alternative without E-Commerce",
    "description": """
The app aims to add accessories and alternatives to products. Odoo standard package let such functionality but only with E-shop installed
Manage accessories and alternatives through the smart buttons. Comfortable and clear. Counters in real time
The app is anyway compatible with 'website_sale'. It means that if you installed the latter, the data would be kept safe and may be used in E-shop
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "0.0",
}