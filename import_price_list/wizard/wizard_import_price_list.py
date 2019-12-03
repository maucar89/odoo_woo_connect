#-*- coding: utf-8 -*-

import os
import csv
import tempfile
from odoo.exceptions import UserError
from odoo import api, fields, models, _, SUPERUSER_ID


class ImportPriceList(models.TransientModel):
    _name = "wizard.import.price.list"

    file_data = fields.Binary('Archivo', required=True,)
    file_name = fields.Char('File Name')
    name = fields.Char('Nombre Tarifa', required=True)
    aplica_variante = fields.Boolean('Aplicar Variante', default=True)

    def import_button(self):
        if not self.csv_validator(self.file_name):
            raise UserError(_("El archivo debe ser de extension .csv"))
        file_path = tempfile.gettempdir()+'/file.csv'
        data = self.file_data
        f = open(file_path,'wb')
        f.write(data.decode('base64'))
        f.close() 
        archive = csv.DictReader(open(file_path))
        
        product_pricelist_obj = self.env['product.pricelist']
        product_obj = self.env['product.product']
        product_tmpl_obj = self.env['product.template']
        product_pricelist_item_obj = self.env['product.pricelist.item']
        
        archive_lines = []
        for line in archive:
            archive_lines.append(line)
        vals = {
            'name': self.name,
        }
        pricelist_id = product_pricelist_obj.create(vals)
        for line in archive_lines:
            code = str(line.get('code',""))
            if self.aplica_variante:
                product_id = product_obj.search([('default_code','=',code)])
                if not product_id:
                    raise UserError(_("No se encuentra el código:" + code))

            else:
                product_id = product_tmpl_obj.search([('default_code', '=', code)])
                if not product_id:
                    raise UserError(_("No se encuentra el código:" + code))

            price_unit = line.get('price',0.0)
            
            if product_id:
                if self.aplica_variante:
                    var_app = '0_product_variant'
                    vals = {
                        'pricelist_id': pricelist_id.id,
                        'applied_on': var_app,
                        'product_id': product_id.id,
                        'compute_price': 'fixed',
                        'fixed_price': price_unit,
                    }
                else:
                    var_app = '1_product'
                    vals = {
                        'pricelist_id': pricelist_id.id,
                        'applied_on': var_app,
                        'product_tmpl_id': product_id.id,
                        'compute_price': 'fixed',
                        'fixed_price': price_unit,
                    }

                product_pricelist_item_obj.create(vals)
        return {'type': 'ir.actions.act_window_close'}
        
        
    @api.model
    def csv_validator(self, xml_name):
        name, extension = os.path.splitext(xml_name)
        return True if extension == '.csv' else False
        
