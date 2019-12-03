# -*- coding: utf-8 -*-

from odoo import models


class AccMoveReport(models.Model):
    _inherit = 'account.move'

    def print_journal_entry(self):
        return self.env['report'].get_action(self, 'iwesabe_reports_journal_entry.tmpte_journal_entry')
