# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Users(models.Model):
    _inherit = 'res.users'

    journal_ids = fields.Many2many(
        'account.journal',
        'users_journals_restrict',
        'user_id',
        'journal_id',
        'Allowed Journals',
    )

    @api.constrains('journal_ids')
    def update_journal_restrict(self):
        restrict_group = self.env.ref('dvit_account_journal_restrict.journal_restrict_group')
        for user in self:
            if user.journal_ids:
                # add users to restriction group
                # Due to strange behaviuor, we must remove the user from the group then
                # re-add him again to get restrictions applied
                restrict_group.write({'users':  [(3, user.id)]})
                user.groups_id =[(3, restrict_group.id)]
                ## re-add
                restrict_group.write({'users':  [(4, user.id)]})
                user.groups_id =[(4, restrict_group.id)]
            else:
                restrict_group.write({'users':  [(3, user.id)]})
                user.groups_id =[(3, restrict_group.id)]

            self.env.user.context_get.clear_cache(self)
