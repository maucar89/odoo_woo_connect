# -*- coding: utf-8 -*-
# © 2018 Odoo Bolivia - Mauricio Carreño S.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class ImportacionesDatos(models.Model):

    _name = 'detalle.costos'

    costos_id = fields.Many2one('purchase.order', string="Detalle Costos")
    nombre_costo_importacion = fields.Char('Costo Importacion', required=True)
    monto_costo_importacion_bolivianos = fields.Float('Monto Bs.', help=u'Monto del tipo de costo de importacion en bolivianos.')
    monto_costo_importacion = fields.Float('Monto $us', help=u'Monto del tipo de costo de importacion en dolares.')
    factura_costo_importacion = fields.Boolean('Factura', help=u'Si lleva factura el tipo de costo de improtacion.')
    credito_fiscal_costo_impotacion = fields.Float('Credito Fiscal', help=u'Credito Fiscal del tipo de costo de importacion en dolares.')
    gastos_netos_costo_impotacion = fields.Float('Gastos Netos $us',  help=u'Gastos netos del tipo de costo de importacion en dolares.')
    detalle_costo_importacion = fields.Char('Detalle costo', help=u'Detalle donde puede especificarse algun documento, o nota para la generación del asiento.')
    proveedor_costo = fields.Many2one('res.partner', 'Proveedor', help=u'Proveedor del costo de importacion.')
    fecha_costo = fields.Date('Fecha', help=u'Fecha en que se efectuo el gasto. Esto sirve también para la fecha de los comprobantes')
    pagado = fields.Float('Pagado', help=u'Monto pagado hasta la fecha')
    saldo = fields.Float('Saldo', help=u'Saldo pendiente por pagar a la fecha')
    estado = fields.Selection([('Por pagar','Por pagar'),('Pagado','Pagado')], string="Estado")
