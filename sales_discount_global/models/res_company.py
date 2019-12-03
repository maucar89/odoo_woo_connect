# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    global_dis_account_id = fields.Many2one('account.account', string="Global Discount Account")


    @api.multi
    def set_default_discount(self):
        if self.global_dis_account_id:
            self.company_id.write({'global_dis_account_id': self.global_dis_account_id.id or False})
