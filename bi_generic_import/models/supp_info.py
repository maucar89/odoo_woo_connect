# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
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
import tempfile
import binascii
import logging
from odoo.exceptions import Warning
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)
try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')

class gen_suppinfo(models.TransientModel):
    _name = "gen.suppinfo"

    file = fields.Binary('File')
    create_link_option = fields.Selection([('create', 'Create product template if not available'),('link', 'Link with available product template')],string='Product Option',default='link')


    @api.multi
    def import_fle(self):
        fp = tempfile.NamedTemporaryFile(delete = False,suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        values = {}
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        for row_no in range(sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = (map(lambda row:isinstance(row.value, unicode) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                values.update( {'vendor':line[0],
                                'product': line[1],
                                'delivery_time': line[2],
                                'quantity': line[3],
                                'price': line[4],
                                'create_link_option':self.create_link_option,
                                })
                res = self._create_product_suppinfo(values)
                        
        return res

    @api.multi
    def _create_product_suppinfo(self,val):
        name = self._find_vendor(val.get('vendor'))
        product_tmpl_id = self._find_product_template(val.get('product'),val.get('create_link_option'))
        res = self.env['product.supplierinfo'].create({
                                                       'name':name,
                                                       'product_tmpl_id':product_tmpl_id,
                                                       'product_name': self.env['product.template'].browse(product_tmpl_id).name,
                                                       'min_qty': int(float(val.get('quantity'))),
                                                       'price': val.get('price'),
                                                       'delay': int(float(val.get('delivery_time')))
                                                       })
        print "===========================res",res
        return res



    @api.multi
    def _find_vendor(self,name):
        partner_search = self.env['res.partner'].search([('name','=',name),('supplier','=',True)])
        if not partner_search:
            raise Warning (_("%s Vendor Not Found") % name)
        return partner_search.id

    @api.multi
    def _find_product_template(self,product,create_opt):
        product_tmpl_search = self.env['product.template'].search([('name','=',product)])
        if not product_tmpl_search:
            if create_opt == 'create':
                product_id = self.env['product.template'].create({'name':product})
                product_tmpl_search = product_id
            else:
                raise Warning (_(" You have selected Link product template with existing product but %s Product template does not exist") % product)
        return product_tmpl_search.id

