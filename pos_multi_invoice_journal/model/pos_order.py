# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class pos_order(models.Model):
    _inherit = "pos.order"

    invoice_journal_id = fields.Many2one('account.journal', 'Journal account', readonly=1)

    def _prepare_invoice(self):
        res = super(pos_order, self)._prepare_invoice()
        if self.invoice_journal_id:
            res['journal_id'] = self.invoice_journal_id.id
        return res

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(pos_order, self)._order_fields(ui_order)
        if ui_order.get('invoice_journal_id', False):
            order_fields['invoice_journal_id'] = ui_order.get('invoice_journal_id')
        return order_fields
