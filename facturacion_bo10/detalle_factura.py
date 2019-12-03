# -*- coding: utf-8 -*-
# © 2018 Odoo Bolivia - Mauricio Carreño S.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class DetalleFactura(models.Model):

    _name = 'detalle.factura'

    fac_id = fields.Many2one('account.invoice', string="Detalle Facturas")
    fac_proveedor = fields.Many2one('res.partner', 'Proveedor')
    fac_nit = fields.Char('NIT')
    fac_NroFactura = fields.Char('Nro Factura', required=True)
    fac_FechaFactura = fields.Date('Fecha Factura')
    fac_codigocontrol = fields.Char('Codigo de Control')
    fac_creditofiscal = fields.Float('Credito Fiscal')
    fac_importeice = fields.Float('Importe ICE')
    fac_importeneto = fields.Float('Importe Neto')
    fac_importeexcento = fields.Float('Importe Excento')
    fac_importetotal = fields.Float('Importe Total')
    fac_NroAutorizacion = fields.Char('Nro Autorizacion')
