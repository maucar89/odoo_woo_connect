# -*- coding: utf-8 -*-
# © 2018 Odoo Bolivia - Mauricio Carreño S.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class ImportacionesDatos(models.Model):
    _name = 'importaciones.datos'

    importacion_id = fields.Many2one('purchase.order', string="Datos Import.")
    numero_pfm = fields.Char('Nro PFM', help=u'PFM.')
    concepto = fields.Char('Concepto', help=u'Detalle o motivo de la importacion.')
    fecha_factura_proveedor = fields.Date('Fecha de FAC/PROVEEDOR', help=u'Fecha de facturacion de Proveedor.')
    numero_factura = fields.Char('Nro Factura', help=u'Numero de factura de la compra.')
    monto = fields.Float('Monto $us.', help=u'Monto expresado en dolares.')
    seguro = fields.Float('Seguro', store=True,  help=u'Seguro aplicado de la importacion.')
    credito_vencimiento = fields.Char('Dias crédito', help=u'Dias de crédito para la fecha de vencimiento de la factura.')
    # 'ew_seguro' : fields.float('Seguro', help=u'Seguro aplicado de la importacion.')
    fecha_vencimiento_pago = fields.Date('Fecha Venc Pago', help=u'Fecha de vencimiento del pago.')
    saldo = fields.Float(string="Saldo" ,store=True)
    pagado = fields.Float(string='Pagado', store=True)
    estado = fields.Selection([('Por pagar','Por pagar'),('Pagado','Pagado')], string="Estado", readonly=True)
