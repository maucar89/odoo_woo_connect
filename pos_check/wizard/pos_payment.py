# -*- coding: utf-8 -*-
from odoo import models, api, fields

class PosMakePayment(models.TransientModel):
    _inherit = 'pos.make.payment'

    check_bank_id = fields.Many2one('res.bank', string="Check bank")
    check_bank_acc = fields.Char('Check bank account')
    check_number = fields.Char()
    check_owner = fields.Char()
    check_info_required = fields.Boolean('Check info required?')
    check_bank_name_visible = fields.Boolean('Bank name visible?')
    check_bank_name_required = fields.Boolean('Bank name required?')
    check_bank_acc_visible = fields.Boolean('Bank account number visible?')
    check_bank_acc_required = fields.Boolean('Bank account number required?')
    check_owner_visible = fields.Boolean('Check owner visible?')
    check_owner_required = fields.Boolean('Check owner required?')

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        self.check_info_required = self.journal_id.check_info_required
        self.check_bank_name_visible = self.journal_id.check_bank_name_visible
        self.check_bank_name_required = self.journal_id.check_bank_name_required
        self.check_bank_acc_visible = self.journal_id.check_bank_acc_visible
        self.check_bank_acc_required = self.journal_id.check_bank_acc_required
        self.check_owner_visible = self.journal_id.check_owner_visible
        self.check_owner_required = self.journal_id.check_owner_required

