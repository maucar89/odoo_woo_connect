# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from lxml import etree


class sale_order(models.Model):

    """Adds the fields for options of the customer order delivery"""

    _inherit = "sale.order"
    _description = 'Sale Order'

    customer_order_delivery_date = fields.Date(string='Delivery Date')
    customer_order_delivery_comment = fields.Text(string='Delivery Comment', translate=True)

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        res = super(sale_order,self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=False)
        if res:
            doc = etree.XML(res['arch'])
            if view_type == 'form':
                is_customer_order_delivery_date_feature = False 
                is_customer_order_delivery_comment_feature = False
                                   
                search_websites = self.env['website'].search([('id','!=',False)])
                for setting in search_websites:
                    if setting.is_customer_order_delivery_date_feature:
                        is_customer_order_delivery_date_feature = True

                    if setting.is_customer_order_delivery_comment_feature:
                        is_customer_order_delivery_comment_feature = True


                if is_customer_order_delivery_date_feature:
                    for node in doc.xpath("//page[@class='delivery_date']"):
                        node.set('string', '')
                        
                if is_customer_order_delivery_comment_feature:
                    for node in doc.xpath("//field[@name='customer_order_delivery_comment']"):
                        node.set('style', 'display:none')

                res['arch'] = etree.tostring(doc)
        return res
