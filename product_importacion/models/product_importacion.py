# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    manufacturer = fields.Many2one('res.partner', 'Manufacturer')
    pro_master = fields.Integer('Master')
    pro_estado = fields.Selection((('n','Nuevo'),('no','Normal'),('p','Promoción'),('d','Descuentos'),('pr','Promocionales'),('di','Discontinuado'),('at','Alta Rotación')),'Estado')
    pro_color = fields.Selection((('v','Verde'),('ro','Rojo')),'Color')
    pro_precio_modificado = fields.Boolean('Precio Modificado')
    pro_secuencia = fields.Integer('Secuencia')
    pro_promedio_anual = fields.Float('Promedio Anual')
    pro_analisis_mexico = fields.Boolean('Analisis Mexico')
    pro_cantidad_empaque = fields.Float('Cantidad de Empaque')
    pro_grado_complejidad = fields.Integer('Grado Complejidad')
    pro_stock_minimo = fields.Float('Stock Minimo')
    pro_stock_maximo = fields.Float('Stock Maximo')
    pro_nombre_corto = fields.Char('Nombre Corto')
    pro_igo = fields.Integer('IGO')
    pro_pu_fob = fields.Float('Precio Unitario FOB Almacenado')
