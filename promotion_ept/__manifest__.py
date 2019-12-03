# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    # App information
    
    'name' : 'Manage Sale Promotions in Odoo',
    'category' : 'Sales',
    'version' : '10.0.2.0',
    'license': 'OPL-1',
    'summary': 'Delight your customers and boost your sales by offering attractive coupons and promotional offers using Odoo Promotions',
    'description': """""",
   
   # Dependencies
	'depends': ['sale'],

   # Views
    'data': [  
	    'wizard/promotion_extend_wizard.xml',
        'report/promotion_report_template.xml',
        'report/promotion_barcode_report.xml',
        'views/promotion_coupon.xml',
        'views/promotion_view.xml',
        'security/promotion_security.xml',
        'views/product.xml',
        'views/sale_order.xml',
        'data/email_template.xml',
       
	 #'data/promotion_demo.xml',
        'views/sequence.xml',
        'views/sale_config_setting.xml',
	    'security/ir.model.access.csv',],
    
    # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    
    # Odoo Store Specific
    
    'images': ['static/description/main.jpg'],
  
    
    # Technical
   
    'live_test_url' :'http://www.emiprotechnologies.com/free-trial?app=promotion-ept&version=10',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '149' ,
    'currency': 'EUR',



   
}
