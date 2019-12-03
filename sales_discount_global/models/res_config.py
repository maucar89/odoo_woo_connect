# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountDiscountSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    global_dis_account_id = fields.Many2one('account.account',
                                            string="Global Discount Account",
                                            related="company_id.global_dis_account_id")

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            company = self.company_id
            self.global_dis_account_id = company.global_dis_account_id and \
                                         company.global_dis_account_id.id
            res = super(AccountDiscountSettings, self).onchange_company_id()
            return res

    @api.multi
    def set_default_global_dis_account_id(self):
        """ Set the default_global_dis_account_id if it has changed.
            @Return: global discount id.
            """
        for rec in self:
            ir_values_obj = self.env['ir.values']
            ir_values_obj.sudo().set_default('account.config.settings', "global_dis_account_id",
                                             [self.global_dis_account_id.id] if self.global_dis_account_id else False,
                                             for_all_users=True, company_id=self.company_id.id)
