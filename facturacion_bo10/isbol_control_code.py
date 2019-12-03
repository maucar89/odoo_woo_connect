# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services (<http://www.serpentcs.com>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#    /usr/lib/python2.7/dist-packages/odoo/addons/
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import openerp.tools
#from openerp.osv import fields,osv
from odoo import models, fields, api, _
from openerp.tools.translate import _
from controlcode import ControlCode
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare


class account_journal(models.Model):

    _inherit = "account.journal"


    fecha_limite = fields.Date('Limite de emision',help = 'La fecha presente en la dosificacion')
        #'autorizacion_dosificacion' : fields.integer('Autorizacion',help = 'Autorizacion presente en la dosificacion')
    autorizacion_dosificacion = fields.Char('Autorizacion',help = 'Autorizacion presente en la dosificacion')
    #'autorizacion_dosificacion' : fields.float('Autorizacion', size=20, digits=(20, 0) ,help = 'Autorizacion presente en la dosificacion')
    llave_dosificacion = fields.Char('Llave',help = 'Llave presente en la dosificacion')
    direccion_sucursal = fields.Text('Direccion Casa Matriz',help = 'Es la direccion, telefonos, ciudad de la Casa Matriz que aparece en las facturas')
    direccion_sucursal_2 = fields.Text('Direccion de la Sucursal',help = 'Es la direccion, telefonos, ciudad de la sucursal que aparece en las facturas')
    actividad_dosificacion = fields.Char('Actividad',help = 'Actividad de contribuyente')
    leyenda_dosificacion = fields.Text('Leyenda de la factura',help = 'Leyenda de la factura')
    leyenda_secundaria = fields.Text('Leyenda de la dosificacion',help = 'Leyenda secundaria de la dosificacion')
    nit_contribuyente = fields.Char('Nit del Contribuyente',help = 'Nit del contribuyente')
    nombre_sucursal = fields.Char('CASA MATRIZ',help = 'Nombre de la sucural, ejemplo CASA MATRIZ o SUCURSAL 8')
    nombre_sucursal_2 = fields.Char('SUCURSAL',help = 'Nombre de la sucural, ejemplo SUCURSAL 8')
    dosificacion = fields.Boolean('Dosificacion',help = 'Se usa el diario como dosificacion para facturas')
    mensaje_factura = fields.Char('Mensaje en Factura',help = 'Mensaje que se imprime en todas las facturas en la parte inferior')
    razon_social = fields.Char('Razon Social',help = 'Razon Social o Nombre Comercial')
    nombre_unipersonal = fields.Char('Nombre Unipersonal',help = 'Nombre Unipersonal')
    titulo = fields.Char('Titulo de la factura',help = 'Ejemplo FACTURA o FACTURA TURISTICA')
    subtitulo = fields.Char('Subtitulo de la factura',help = 'Ejemplo No valido para credito fiscal')
    estado_factura = fields.Char('estado_factura')



   # _defaults = {

    #    'llave_dosificacion' : "0",
     #   'autorizacion_dosificacion' : "0",
      #      }

class account_invoice(models.Model):

    _inherit = "account.invoice"
    _order = 'id desc'

    #    pd_horometro_ini = fields.Float(related='pd_codigo.pv_horas', string='Horometro acutal',)

    nit = fields.Char(related='partner_id.nit', string="NIT",store=True)
    #'nit' : fields.char('NIT',help = 'NIT number', store=True),
    code = fields.Char('Codigo de Control',size=64,help = 'Codigo de control valido para el SIN')
    #'autorizacion': fields.related('journal_id','autorizacion_dosificacion',type="integer", relation="account.journal",string="Autorizacion",store=True,readonly=True),
    autorizacion = fields.Char(related='journal_id.autorizacion_dosificacion', string="Autorizacion",store=True,readonly=True)
    #'autorizacion': fields.related('journal_id','autorizacion_dosificacion',type="float", size=20, digits=(20, 0), relation="account.journal",string="Autorizacion",store=True,readonly=True),
    llave = fields.Char(related='journal_id.llave_dosificacion',string="Llave de la dosificacion",store=True,readonly=True)
    fecha = fields.Date(related='journal_id.fecha_limite',string="Limite de emision",store=True,readonly=True)
    direccion = fields.Text(related='journal_id.direccion_sucursal',string="Direccion de la Casa Matriz",store=True,readonly=True)
    direccion_2 = fields.Text(related='journal_id.direccion_sucursal_2',string="Direccion de la sucursal",store=True,readonly=True)
    actividad = fields.Char(related='journal_id.actividad_dosificacion',string="Actividad del contribuyente",store=True,readonly=True)
    leyenda = fields.Text(related='journal_id.leyenda_dosificacion',string="Leyenda de la factura",store=True,readonly=True)
    leyenda2 = fields.Text(related='journal_id.leyenda_secundaria',string="Leyenda de la dosificacion",store=True,readonly=True)
    nit_empresa = fields.Char(related='journal_id.nit_contribuyente',string="Nit contribuyente",store=True,readonly=True)
    sucursal = fields.Char(related='journal_id.nombre_sucursal',string="Casa Matriz",store=True,readonly=True)
    sucursal_2 = fields.Char(related='journal_id.nombre_sucursal_2',string="Nombre de la sucursal",store=True,readonly=True)
    mensaje = fields.Char(related='journal_id.mensaje_factura',string="Mensaje Opcional",store=True,readonly=True)
    razon = fields.Char(related='journal_id.razon_social',string="Razon Social",store=True,readonly=True)
    unipersonal = fields.Char(related='journal_id.nombre_unipersonal',string="Unipersonal",store=True,readonly=True)
    factura_titulo = fields.Char(related='journal_id.titulo',string="Titulo",store=True,readonly=True)
    factura_subtitulo = fields.Char(related='journal_id.subtitulo',string="Sub Titulo",store=True,readonly=True)
    operador = fields.Char(related='partner_id.res_operador',string="Observaciones",store=True)
    estado_factura = fields.Char('Estado Factura')




 #   def _check_date(self, cr, uid, ids, context=None):
  #      for fecha in self.browse(cr, uid, ids, context=context):
   #         if self.fecha == self.date_invoice:
    #          return True


    _sql_constraints = [
         ('number_uniq', 'Check(1=1)', 'Hola Que hace'),
     #   (_check_date, 'Fecha limite de emision de factura expirada', ['fecha'])
    ]



    @api.multi
    def invoice_validate(self):
        res = super(account_invoice, self).invoice_validate()
        for inv in self:
            dt = datetime.strptime(inv.date_invoice, DEFAULT_SERVER_DATE_FORMAT)
            inv_date = datetime.strftime(dt,'%Y/%m/%d')
            cc = ControlCode(inv.autorizacion, inv.llave)
            cc.set_date(inv_date) \
            .set_nit(int(inv.nit))

            #inv_num = inv.invoice_number
            inv_num = inv.number
            split_invoice = inv_num.split("/")
            int_inv_num = split_invoice[-1:]
            number = int(str(int_inv_num[0]))
#            number = 100

            control_code = cc.generate(number, inv.amount_total_company_signed)
            if not inv_date or not number or not inv.amount_total_company_signed:
                self.write({'code':'No valido para crédito fiscal'})
            else:
                self.write({'code':control_code})
        return res



#    def check_nit(self, cr, uid, ids, context=None):
 #       inv_obj=self.browse(cr, uid, ids, context=context)
  #      if not inv_obj.nit.isdigit() and inv_obj.nit :
   #         raise osv.except_osv(_('Invalid NIT'),_('Please enter a valid NIT'))
    #    if inv_obj.nit and len(inv_obj.nit) >= 31:
     #       raise osv.except_osv(_('Invalid NIT'),_('NIT Takes maximum 30 Digits'))
      #  return True

    #_constraints = [
     #   (check_nit, 'Please enter a valid NIT', ['nit']),
    #]
