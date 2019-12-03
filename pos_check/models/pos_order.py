# -*- coding: utf-8 -*-
from odoo import models

class PosOrder(models.Model):
    _inherit = "pos.order"

    def _payment_fields(self, ui_paymentline):
        res = super(PosOrder, self)._payment_fields(ui_paymentline)
        res.update({
            'check_bank_id': ui_paymentline.get('check_bank_id'),
            'check_bank_acc': ui_paymentline.get('check_bank_acc'),
            'check_number': ui_paymentline.get('check_number'),
            'check_owner': ui_paymentline.get('check_owner')
        })
        return res

    def add_payment(self, data):
        statement_id = super(PosOrder, self).add_payment(data)
        StatementLine = self.env['account.bank.statement.line']
        statement_lines = StatementLine.search([
            ('statement_id', '=', statement_id),
            ('pos_statement_id', '=', self.id),
            ('journal_id', '=', data['journal']),
            ('amount', '=', data['amount'])
        ])
        for line in statement_lines:
            if line.journal_id.check_info_required and not line.check_bank_id:
                check_bank_id = data.get('check_bank_id')
                if isinstance(check_bank_id, (tuple, list)):
                    check_bank_id = check_bank_id[0]

                check_vals = {
                    'check_bank_id': check_bank_id,
                    'check_bank_acc': data.get('check_bank_acc'),
                    'check_number': data.get('check_number'),
                    'check_owner': data.get('check_owner')
                }
                line.write(check_vals)
                break

        return statement_id
