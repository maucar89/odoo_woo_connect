# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Website(models.Model):

    """Adds the fields for options of the Customer Order Delivery Date Feature."""

    _inherit = 'website'

    is_customer_order_delivery_date_feature = fields.Boolean(
        string='Do you want to disable customer order delivery date feature',
        translate=False) 
    is_customer_order_delivery_comment_feature = fields.Boolean(
        string='Do you want to disable customer order delivery comment feature',
        translate=False) 

class WebsiteConfigSettings(models.TransientModel):

    """Settings for the Customer Order Delivery Date."""

    _inherit = 'website.config.settings'

    is_customer_order_delivery__date_feature = fields.Boolean(
        related='website_id.is_customer_order_delivery_date_feature',
        string="Do you want to disable customer order delivery date feature",
        translate=False)
    is_customer_order_delivery__comment_feature = fields.Boolean(
        related='website_id.is_customer_order_delivery_comment_feature',
        string="Do you want to disable customer order delivery comment feature",
        translate=False)
