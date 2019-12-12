# -*- coding: utf-8 -*-
# Copyright (C) 2016 Harma Consulting, Inc.

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    social_newwindow = fields.Boolean("Launch in new window", help="All social media links launch in a new window")
    social_instagram = fields.Char("Instagram Account")
    social_pinterest = fields.Char("Pinterest Account")
