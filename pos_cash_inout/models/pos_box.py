# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
#################################################################################

from openerp import models, fields, api, _
 
class pos_session(models.Model):
    _inherit = 'pos.session'

    @api.model
    def take_money_out(self, name, amount, session_id):
        try:
            cash_out_obj = self.env['cash.box.out']
            total_amount = 0.0
            active_model = 'pos.session'
            active_ids = [session_id]
            if active_model == 'pos.session':
                records = self.env[active_model].browse(active_ids)
                bank_statements = [record.cash_register_id for record in records if record.cash_register_id]
                if not bank_statements:
                    raise Warning(_('There is no cash register for this PoS Session'))
                res = cash_out_obj.create({'name': name, 'amount': amount})
                return res._run(bank_statements)
            else:
                return {}
        except:
           return {'error':'There is no cash register for this PoS Session '}

    @api.model
    def put_money_in(self, name, amount, session_id):
        try:
            cash_out_obj = self.env['cash.box.in']
            total_amount = 0.0
            active_model = 'pos.session'
            active_ids = [session_id]
            if active_model == 'pos.session':
                records = self.env[active_model].browse(active_ids)
                bank_statements = [record.cash_register_id for record in records if record.cash_register_id]
                if not bank_statements:
                    raise Warning(_('There is no cash register for this PoS Session'))
                res = cash_out_obj.create({'name': name, 'amount': amount})
                return res._run(bank_statements)
            else:
                return {}
        except Exception, e:
           return {'error':'There is no cash register for this PoS Session '}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: