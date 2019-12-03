# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from odoo import models,fields, api
from odoo import tools

class sale_order(models.Model):
    _inherit ='sale.order'
    
    
    delivery_notes = fields.Text('Delivery Notes')
    

    
# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:    
