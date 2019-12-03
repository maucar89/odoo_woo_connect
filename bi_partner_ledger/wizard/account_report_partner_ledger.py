# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class account_report_partner_ledger(models.TransientModel):
    _inherit = "account.report.partner.ledger"

    partner_ids = fields.Many2many('res.partner', 'partner_ledger_partner_rel', 'id', 'partner_id', string='Partners')

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'reconciled': self.reconciled, 'amount_currency': self.amount_currency,
                             'partner_ids': self.partner_ids.ids})
        return self.env['report'].get_action(self, 'account.report_partnerledger', data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: