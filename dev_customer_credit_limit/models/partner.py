# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

from openerp import api, models, fields, _

class res_partner(models.Model):
    _inherit= 'res.partner'
    
    check_credit = fields.Boolean('Check Credit')
    credit_limit_on_hold  = fields.Boolean('Credit limit on hold')
    credit_limit = fields.Float('Credit Limit')
