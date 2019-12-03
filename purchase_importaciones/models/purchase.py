# -*- coding: utf-8 -*-
# © 2018 Odoo Bolivia - Mauricio Carreño S.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    importaciones_tipo = fields.Selection((('I','Importacion'),('L','Local')),'Tipo Compra')
    importaciones_tipo_pago = fields.Selection((('C','Crédito'),('E','Efectivo')),'Tipo Pago')
    importaciones_referencia = fields.Char('Referencia Salcedo')
    importaciones_nro_importacion = fields.Char('Nro Importación')
    importaciones_nrocontenedor = fields.Char('Nro de Contenedor')
    importaciones_buque = fields.Char('Nro. del Buque Navegación')
    importaciones_apl_seguro = fields.Char('Nro. Apl Seguro')
    importaciones_peso_bruto = fields.Float('Peso Bruto')
    importaciones_volumen = fields.Float('Volumen m3')
    importaciones_fecha_embarque = fields.Date('Fecha de Embarque')
    importaciones_fecha_llegada_puerto = fields.Date('Fecha llegada puerto')
    importaciones_fecha_salida_puerto = fields.Date('Fecha salida puerto')
    importaciones_fecha_llegada_aduana = fields.Date('Fecha llegada aduana')
    importaciones_fecha_almacen = fields.Date('Fecha Almacén')
    importaciones_dui = fields.Char('Nro. DUI')
    importaciones_canal = fields.Selection((('r','Rojo'),('a','Amarillo'),('v','Verder')),'Estado')
    importaciones_fecha_factura_bolivia = fields.Date('Fecha de BL')
    importaciones_fecha_factura_vencimiento = fields.Date('Fecha de FAC/VENC')
    importaciones_estado = fields.Selection((('a','Altamar'),('pc','Puerto Chile'),('ad','Aduana'),('as','Almacen Salcedo')),'Estado')
    importaciones_forwarder = fields.Many2one("res.partner.forwarder", "Forwarder", oldname="forwarder")
    importaciones_datos_adicionales = fields.One2many('importaciones.datos', 'importacion_id', 'Datos Adicionales')
    importaciones_detalle_costos = fields.One2many('detalle.costos', 'costos_id', 'Detalle Costos')


class ResPartnerForwarder(models.Model):
    _name = 'res.partner.forwarder'
    _description = "Forwarder"

    name = fields.Char(required=True, translate=True)
    codigo = fields.Char(required=True)
