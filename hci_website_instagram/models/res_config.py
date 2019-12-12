# -*- coding: utf-8 -*-
# Copyright (C) 2016 Harma Consulting, Inc.

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    social_newwindow = fields.Boolean(related='website_id.social_newwindow')
    social_instagram = fields.Char(related='website_id.social_instagram')
    social_pinterest = fields.Char(related='website_id.social_pinterest')
