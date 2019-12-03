# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class pos_config(models.Model):
    _inherit = "pos.config"

    invoice_journal_ids = fields.Many2many(
        'account.journal',
        'pos_config_invoice_journal_rel',
        'config_id',
        'journal_id',
        'Invoice Journal',
        domain=[('type', '=', 'sale')],
        help="Accounting journal used to create invoices.")