from odoo import api, fields, models, _
import time
from odoo.tools import amount_to_text_en

class invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.depends('amount_total','currency_id')
    def _amount_to_text(self):
        for record in self:
            record.amount_to_text = amount_to_text_en.amount_to_text(record.amount_total, 'id', record.currency_id.name)

    amount_to_text = fields.Char(compute='_amount_to_text', string="amount text",  required=False, )
    
