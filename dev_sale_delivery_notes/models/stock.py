# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from odoo import models,fields, api, _  

class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    delivery_notes = fields.Text('Delivery Notes')
    
    
class stock_move(models.Model):
    _inherit = 'stock.move'
    
    def _get_new_picking_values(self):
        res=super(stock_move,self)._get_new_picking_values()
        if res.get('origin'):
            sale_id = self.env['sale.order'].search([('name','=',res.get('origin'))],limit=1)
            if sale_id:
                res.update({
                    'delivery_notes':sale_id.delivery_notes,
                })
        return res
    
# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:
