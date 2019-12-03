# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
import tempfile
import binascii
import xlrd
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
import logging
_logger = logging.getLogger(__name__)
import io
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class gen_mrp(models.TransientModel):
    _name = "gen.mrp"

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'),('xls', 'XLS File')],string='Select',default='csv')
    bom_type = fields.Selection([('normal', 'Normal'),('phantom', 'Phantom')])     


   
    @api.multi
    def find_product_tmpl(self, name):
        product_tmpl_obj = self.env['product.template']
        product_tmpl_search = product_tmpl_obj.search([('name', '=', name)])
        if product_tmpl_search:
            return product_tmpl_search
        else:
            raise Warning(_('Not Valid Product Name "%s"') % name)


    @api.multi
    def make_bom(self, values):
        bom_obj = self.env['mrp.bom']
        product_tmpl_id = False
        bom_search = bom_obj.search([
                ('code', '=', values.get('ref'))
            ])
        if bom_search:

            if  bom_search[0].code == values.get('ref'):
                if bom_search[0].product_tmpl_id.name != values.get('product_tmpl'):
                   raise Warning(_('Found Diffrent value of product for same BOM %s') % values.get('product_tmpl'))
                else:    
                   self.make_bom_line(values, bom_search[0])
                return bom_search
            else:
                raise Warning(_('Found Diffrent value same BOM %s') % values.get('ref'))
        else:
            product_tmpl_id = self.find_product_tmpl(values.get('product_tmpl'))


            bom_id = bom_obj.create({
                'product_tmpl_id' : product_tmpl_id.id,
                'code':values.get('ref'),
                'type':self.bom_type,
                'product_qty': values.get('qty')
            })
            self.make_bom_line(values, bom_id)
 
            return bom_id


    @api.multi
    def make_bom_line(self, values, bom_id):
        product_id = False
        product_obj = self.env['product.product']
        mrp_line_obj = self.env['mrp.bom.line']
        product_search = product_obj.search([('name', '=', values.get('product'))])
        product_uom = self.env['product.uom'].search([('name', '=', values.get('uom'))])
        if product_search:
            product_id = product_search
        else:
            if not product_id:
                product_id = product_obj.create({'name': values.get('product')})
        if not product_uom:
            raise Warning(_(' "%s" Product UOM category is not available.') % values.get('uom'))
        res = mrp_line_obj.create({
            'product_id' : product_id.id,
            'product_qty' : values.get('qty_l'),
            'bom_id' : bom_id.id,
            'product_uom_id':product_uom.id,
            })
        return True



    @api.multi
    def import_csv(self):
        """Load Inventory data from the CSV file."""
        if self.import_option == 'csv':
            keys = ['product_tmpl', 'ref', 'qty', 'product', 'qty_l', 'uom', ]
            csv_data = base64.b64decode(self.file)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            file_reader = []
            csv_reader = csv.reader(data_file, delimiter=',')

            try:
                file_reader.extend(csv_reader)
            except Exception:
                raise exceptions.Warning(_("Invalid file!"))
            values = {}
            for i in range(len(file_reader)):
                field = list(map(str, file_reader[i]))
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        values.update({'type':self.bom_type})
                        res = self.make_bom(values)
                        
                        
        else:
            fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    values.update( {'product_tmpl':line[0],
                                            'ref': line[1],
                                            'qty': line[2],
                                            'product': line[3],
                                            'qty_l': line[4],
                                            'uom': line[5],
                                             'type':self.bom_type
                                               })
                    res = self.make_bom(values)
                 


        return res

