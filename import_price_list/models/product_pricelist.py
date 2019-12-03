# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
import base64
import io

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.multi
    def export_pricelist(self):
        res = {}
        op = "file"
        fname = '%s_%s_Comprobantes.csv' % (self.name, op)
        path = '/tmp/' + fname
        # txtFile = open(path, 'wb')
        # txtFile.write(codecs.BOM_UTF8)
        txtFile = io.open(path, 'w', encoding='utf-8')

        # txtFile.write(u"code,name,price" + '\n')
        txtFile.write(u"code,price" + '\n')

        id_tarifa =  self.id
        obj_product_pricelist_item = self.env['product.pricelist.item'].search([('pricelist_id', '=', id_tarifa)])
        for id in obj_product_pricelist_item:
            # Si aplica sobre un producto
            code = ""
            if id.applied_on == '1_product':
                if id.product_tmpl_id.default_code:
                    code = id.product_tmpl_id.default_code
                    nombre = id.product_tmpl_id.name

            if id.applied_on == '0_product_variant':
                if id.product_id.default_code:
                    code = id.product_id.default_code
                    nombre = id.product_id.name

            value_p = id.fixed_price
            if (value_p % 1) == 0 or value_p.is_integer():
                value_p =  int(value_p)

            if not code == '':
                # txtFile.write(str(code) + "," + str(nombre.encode("utf-8")) + "," + str(value_p) + '\n')
                # txtFile.write(u'%s,%s,%s\n' % (code, nombre.encode("utf-8"), value_p))
                txtFile.write(u'%s,%s\n' % (code, value_p))
        txtFile.close()
        data = base64.encodestring(open(path, 'r').read())
        attach_vals = {'name': fname, 'datas': data, 'datas_fname': fname}
        doc_id = self.env['ir.attachment'].create(attach_vals)
        res['type'] = 'ir.actions.act_url'
        res['target'] = 'new'
        res['url'] = "web/content/?model=ir.attachment&id=" + str(
            doc_id.id) + "&filename_field=datas_fname&field=datas&download=true&filename=" + str(doc_id.name)
        return res
