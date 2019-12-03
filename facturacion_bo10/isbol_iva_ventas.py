# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp.tools
from openerp.osv import fields,osv
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare 

class account_invoice(osv.Model):
    
    _inherit = 'account.invoice'
    _order = 'id desc'

    def get_bruto(self, cr, uid, ids, field_name, arg, context=None):
        x={}
        y={}
        print "get_bruto"
        for record in self.browse(cr, uid, ids, context=None):
		x[record.id] = float(record.amount_total)
        y[record.id] = float(record.amount_total) * 0
        estado = record.com_estadofiscal
        if estado == "V":
            return x
        else:
            return y
     		                             

    def get_neto(self, cr, uid, ids, field_name, arg, context=None):
        x={}
        y={}
        print "get_neto"
        for record in self.browse(cr, uid, ids, context=None):
            x[record.id] = float(record.bruto) - float(record.ice) - float(record.excento)
            y[record.id] = float(record.amount_total) * 0
            estado = record.com_estadofiscal
            if estado == "V":
                return x
            else:
                return y    

    def get_credito(self, cr, uid, ids, field_name, arg, context=None):
        x={}
        y={}
        print "get_credito"
        for record in self.browse(cr, uid, ids, context=None):
            x[record.id]= (float(record.bruto) - float(record.ice) - float(record.excento)) * float(0.13)
            y[record.id]= 0
            estado = record.com_estadofiscal
            if estado == "V":
                return x
            else:
                return y        

    def get_nit(self, cr, uid, ids, field_name, arg, context=None):
        x={}
        print "get_nit"
        for record in self.browse(cr, uid, ids):
            x[record.id]= int(record.nit)
        return x        

    def _default_cliente(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context):
           partner_name = order.partner_id.name
           print partner_name.encode('utf-8')
         # Now map the country name to the record ID
         # and put this key/value pair to the dictionary
           res[order.id] = partner_name
        return res

    def get_fecha(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context):
           fecha1 = order.date_invoice
           dt = datetime.strptime(order.date_invoice, DEFAULT_SERVER_DATE_FORMAT)
           fecha = datetime.strftime(dt,'%d/%m/%Y')
           print fecha
         # Now map the country name to the record ID
         # and put this key/value pair to the dictionary
           res[order.id] = fecha1
        return res
           
   
   # def get_cliente(self, cr, uid, ids, field_name, arg, context=None):
    #    res = {}
     #   for order in self.browse(cr, uid, ids, context):
      #     partner_name = order.partner_id.name
       #    print partner_name
         # Now map the country name to the record ID
         # and put this key/value pair to the dictionary
        #   res[order.id] = partner_name
        #return res

    _columns = {	 	
                #Datos de la Empresa que emite la factura		 
		'com_separador': fields.char('Separador QR'),
        'com_limite': fields.char('Limite de Eimision'),
        'com_n1': fields.char('n1'),
        'com_n2': fields.char('n2'),
        'com_nombre': fields.char('Empresa'),
        'com_nit': fields.char('NIT EMPRESA'),
		'com_aut1': fields.char('Autorizacion 1'),
		'com_estadofiscal': fields.selection((('V','V'), ('A','A')),
                   'Estado Fiscal',
                    help='V=Valido, A=Anulado'),

		'ice': fields.float('Importe ICE', digits=(15,2)),
		'excento': fields.float('Importe Excento', digits=(15,2)),

                #Datos Calculados de la factura
    'bruto': fields.function(
                            get_bruto,
                            store=True,
                            type='float',
                            string='Importe Bruto'),

    'neto': fields.function(
                            get_neto,
                            store=True,
                            type='float',
                            string='Importe Neto'),
    'debito': fields.function(
                            get_credito,
                            store=True,
                            type='float',
                            string='Debito Fiscal IVA'),
    'cliente_nit': fields.function(
                            get_nit,
                            store=True,
                            type='float',
                            digits=(15,0),
                            string='Nit del Cliente'),
    'cliente': fields.function(
                           _default_cliente,
                               method=True,
                               type='char',
                               string='Cliente'),

    'fecha1': fields.function(
                           get_fecha,
                               method=True,
                               type='char',
                               string='Fecha'),

                }
    _defaults = {	 	
                #Datos por defecto	 
		#NIT DE LA EMPRESA
        'com_nit' : "203444020",

		#AUTORIZACION       

        #NOMBRE DE LA EMPRESA
        'com_nombre' : "PLURAL EDITORES SRL",

        #FECHA LIMITE DE EMISION        

        'com_estadofiscal': "V",
        'com_separador': "|",
        'com_n1': "0",
        'com_n2': "0",


		
	        }		
account_invoice()

class account_invoice_line(osv.Model):
    _inherit = 'account.invoice.line'
    _order = 'invoice_id desc, sequence, id'


    def _subtotal(self, cr, uid, ids, field_name, arg, context=None):
        if not ids: return {}
        res = {}
        for o in self.browse(cr, uid, ids):
         res[o.id] = ((o.quantity * o.price_unit)) - ((o.quantity * o.price_unit) * (o.discount / 100))
        return res 

    def _price_unit_discount(self, cr, uid, ids, field_name, arg, context=None):
        if not ids: return {}
        res = {}
        for o in self.browse(cr, uid, ids):
         res[o.id] = ((o.price_unit)) - ((o.price_unit) * (o.discount / 100))
        return res 

        
    _columns = {   
      
      'subtotal': fields.function(
             _subtotal, 
             method=True, 
             type='float', 
             string='Total'),
      'price_unit_discount': fields.function(
             _price_unit_discount, 
             method=True, 
             type='float', 
             string='Total'),

    }

class account_move(osv.Model):
    
    _inherit = 'account.move'
    _columns = {        
                #Estado para los asientos       
        'asiento_estadofiscal': fields.selection((('V','V'), ('A','A')),
                   'Estado Fiscal del Asiento', 
                    help='V=Valido, A=Anulado'),

               }
    
    _defaults = {       
                #Datos por defecto   
        #NIT DE LA EMPRESA
        'asiento_estadofiscal' : "V",
                }
