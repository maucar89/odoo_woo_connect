# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

from cStringIO import StringIO
import time
import datetime
from openerp import api, fields, models, _
import xlwt
from xlsxwriter.workbook import Workbook
from xlwt import easyxf
import base64
from openerp.exceptions import ValidationError
from datetime import timedelta



class dev_product_movement(models.TransientModel):
    _name = "dev.product.movement"


    warehouse_ids = fields.Many2many('stock.warehouse', string='Almacen')
    location_id = fields.Many2many('stock.location',string='Locacion',required="1")
    product_ids = fields.Many2many('product.product',string='Productos')
    start_date = fields.Date('Fecha Inicial')
    end_date = fields.Date('Fecha Final')


    @api.multi
    def _get_in_move(self,location,product,warehouse):

        move_pool = self.env['stock.move']
        start_date = self.start_date + ' 00:00:00'
        end_date = self.end_date + ' 23:59:59'
        company_id = self.env.user.company_id.id
        query = """select sm.id from stock_move as sm \
                  JOIN product_product as pp ON pp.id = sm.product_id \
                  JOIN stock_picking_type as spt ON spt.id = sm.picking_type_id \
                  where sm.date >= %s and sm.date <= %s and sm.product_id = %s and  \
                  sm.state = %s and sm.location_id = %s and sm.warehouse_id = %s  \
                   and spt.code = %s and sm.company_id = %s
                  """

        params = (start_date, end_date, product.id, 'done', location.id, warehouse.id, 'outgoing', company_id)
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        result = map(lambda x : x['id'], result)
        out_move = move_pool.browse(result)
        query = """select sm.id from stock_move as sm \
                  JOIN product_product as pp ON pp.id = sm.product_id \
                  JOIN stock_picking_type as spt ON spt.id = sm.picking_type_id \
                  where sm.date >= %s and sm.date <= %s and sm.product_id = %s and  \
                  sm.state = %s and sm.location_dest_id = %s and sm.warehouse_id = %s  \
                   and spt.code = %s and sm.company_id = %s
                  """

        params = (start_date, end_date, product.id, 'done', location.id, warehouse.id, 'incoming', company_id)
        self.env.cr.execute(query, params)
        result1 = self.env.cr.dictfetchall()
        result1 = map(lambda x : x['id'], result1)
        in_move = move_pool.browse(result1)


        query = """select sm.id from stock_move as sm \
                  JOIN product_product as pp ON pp.id = sm.product_id \
                  JOIN stock_picking_type as spt ON spt.id = sm.picking_type_id \
                  where sm.date >= %s and sm.date <= %s and sm.product_id = %s and  \
                  sm.state = %s and sm.location_dest_id = %s and spt.warehouse_id = %s  \
                   and spt.code = %s and sm.company_id = %s
                  """
        params = (start_date, end_date, product.id, 'done', location.id, warehouse.id, 'internal', company_id)
        self.env.cr.execute(query, params)
        result1 = self.env.cr.dictfetchall()
        result1 = map(lambda x : x['id'], result1)
        internal_dest_move = move_pool.browse(result1)
        print ("=========",internal_dest_move)

        query = """select sm.id from stock_move as sm \
                  JOIN product_product as pp ON pp.id = sm.product_id \
                  JOIN stock_picking_type as spt ON spt.id = sm.picking_type_id \
                  where sm.date >= %s and sm.date <= %s and sm.product_id = %s and  \
                  sm.state = %s and sm.location_id = %s and spt.warehouse_id = %s  \
                   and spt.code = %s and sm.company_id = %s
                  """

        params = (start_date, end_date, product.id, 'done', location.id, warehouse.id, 'internal', company_id)
        self.env.cr.execute(query, params)
        result1 = self.env.cr.dictfetchall()
        result1 = map(lambda x : x['id'], result1)
        internal_src_move = move_pool.browse(result1)
        print ("=========",internal_src_move)





        return in_move +  out_move + internal_dest_move + internal_src_move



    @api.multi
    def export_product_movement(self):
        picking_ids=[]
#        workbook = xlwt.Workbook()
        filename='Kardex Productos.xls'
        workbook = xlwt.Workbook()
        worksheet=[]
        for l in range(0,len(self.warehouse_ids)):
            worksheet.append(l)
        c = -1
        for warehouse in self.warehouse_ids:
            c+=1
            worksheet[c] = workbook.add_sheet(warehouse.name)
#            filename='Product Movement.xls'
#            worksheet = workbook.add_sheet(warehouse_id.name)
            header_style= easyxf('font:height 200;pattern: pattern solid, fore_color ivory; align: horiz center;font: color black; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")

            main_header_style= easyxf('font:height 300;align: horiz center; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
            text_left = easyxf('font:height 200; align: horiz left;' "borders: top thin,bottom thin")
            text_left_bold = easyxf('font:height 200; align: horiz left;font:bold True;' "borders: top thin,bottom thin")
            text_center = easyxf('font:height 200; align: horiz center;' "borders: top thin,bottom thin")
            text_right = easyxf('font:height 200; align: horiz right;' "borders: top thin,bottom thin")
            header_cus_nubold= easyxf('font:height 200;pattern: pattern solid, fore_color white; align: horiz left;font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
            second_header_cus_nubold= easyxf('font:height 200;pattern: pattern solid, fore_color white; align: horiz center;font: color black; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")


            first_col = worksheet[c].col(0).width = 130 * 50
            second_col = worksheet[c].col(1).width = 150 * 30
            second_col = worksheet[c].col(2).width = 150 * 30
            second_col = worksheet[c].col(3).width = 190 * 30
            second_col = worksheet[c].col(4).width = 150 * 30


            worksheet[c].write_merge(0, 1, 0, 10, 'KARDEX DE PRODUCTOS',main_header_style)

            print_date = 'Impreso por: : '+ str(datetime.date.today().strftime('%d-%m-%Y'))
            start_date = 'Fecha Inicial : '
            if self.start_date:
                start_date_d = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").strftime('%d-%m-%Y')
                start_date += str(start_date_d)
            end_date = 'Fecha Final : '
            if self.end_date:
                end_date_d = datetime.datetime.strptime(self.end_date, "%Y-%m-%d").strftime('%d-%m-%Y')
                end_date +=  str(end_date_d)

            worksheet[c].write_merge(2, 2, 0,2, print_date,header_cus_nubold)
            worksheet[c].write_merge(2, 2, 3,5,start_date ,header_cus_nubold)
            worksheet[c].write_merge(2, 2, 6,10, end_date,header_cus_nubold)



            worksheet[c].write_merge(3, 3, 0,0, 'Codigo Producto',second_header_cus_nubold)
            worksheet[c].write_merge(3, 3, 1,1, 'Comprobante',second_header_cus_nubold)
            worksheet[c].write_merge(3, 3, 2,2, 'Fecha',second_header_cus_nubold)
            worksheet[c].write_merge(3, 3, 3,3, 'Cliente/Proveedor',second_header_cus_nubold)
#
            worksheet[c].write_merge(3, 3, 4,6, 'Inventario Fisico',second_header_cus_nubold)
            worksheet[c].write_merge(3, 3, 7,10, 'Inventario Valorado - Costo',second_header_cus_nubold)
            worksheet[c].write(4,4, 'Ingresos ',second_header_cus_nubold)
            worksheet[c].write(4,5, 'Ventas',second_header_cus_nubold)
            worksheet[c].write(4,6, 'Total',second_header_cus_nubold)
            worksheet[c].write(4,7, 'C/U',second_header_cus_nubold)
            worksheet[c].write(4,8, 'Ingresos ',second_header_cus_nubold)
            worksheet[c].write(4,9, 'Ventas ',second_header_cus_nubold)
            worksheet[c].write(4,10, 'Total  ',second_header_cus_nubold)

            worksheet[c].write(4,0, ' ',second_header_cus_nubold)
            worksheet[c].write(4,1, ' ',second_header_cus_nubold)
            worksheet[c].write(4,2, ' ',second_header_cus_nubold)
            worksheet[c].write(4,3, ' ',second_header_cus_nubold)
#

            if not self.product_ids:
                raise ValidationError("Seleccione un producto !!!")
            i=5
            for location_id in self.location_id:
                for product in self.product_ids:
                    date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
                    date = date - timedelta(days=1)
                    date = date.strftime('%Y-%m-%d')
                    move_ids = self._get_in_move(location_id,product,warehouse)
                    if move_ids:
                        #worksheet[c].write_merge(i, i, 0,9, location_id.name,header_cus_nubold)
                        i+=1
                        product_code = product.default_code
                        worksheet[c].write(i,0,product_code ,header_cus_nubold)
                        worksheet[c].write_merge(i, i, 1,9, product_code +' - ' + product.name  ,header_cus_nubold)
                        i+=1
                        worksheet[c].write(i,0,product_code ,text_left)
                        worksheet[c].write(i,1,'Saldo Anterior' ,text_left)
                        worksheet[c].write(i,2,date ,text_left)
                        worksheet[c].write(i,3,'Saldo Anterior' ,text_left)
                        qty_avb = product.with_context(to_date=date,location_id=location_id.id,warehouse_id= warehouse.id).qty_available
                        worksheet[c].write(i,6, format(qty_avb,'.2f') or 0.00,text_left)
                        fina_qty_avb = qty_avb * product.standard_price
                        worksheet[c].write(i,10, format(fina_qty_avb,'.2f') or 0.00,text_left)
                        i+=1
                        new_qty_avb = qty_avb
                        for move_line in move_ids:
                            quat_value = 0
                            for quant in move_line.quant_ids:
                                quat_value = quant.inventory_value
                            worksheet[c].write(i,0, move_line.product_id.default_code or ' ',text_left)
                            worksheet[c].write(i,1, move_line.picking_id.name or ' ',text_left)
                            worksheet[c].write(i,2, move_line.date ,text_left)
                            in_qty = 0.00
                            out_qty = 0.00
                            partner_id = ''
                            if move_line.picking_id.picking_type_id.code == 'incoming':
                                in_qty = move_line.product_uom_qty
                                new_qty_avb += in_qty
                                partner_id = move_line.picking_id.partner_id.name
                            if move_line.picking_id.picking_type_id.code == 'outgoing':
                                out_qty = move_line.product_uom_qty
                                new_qty_avb -= out_qty
                                partner_id = move_line.partner_id.name
                            is_internal = False
                            if move_line.picking_id.picking_type_id.code == 'internal':
                                is_internal = True
                                if move_line.location_id.id == location_id.id:
                                    out_qty = move_line.product_uom_qty
                                    new_qty_avb -= out_qty
                                    partner_id = move_line.partner_id.name
                                else:
                                    in_qty = move_line.product_uom_qty
                                    new_qty_avb += in_qty
                                    partner_id = move_line.picking_id.partner_id.name

                            worksheet[c].write(i,3, partner_id or ' ',text_left)
                            worksheet[c].write(i,4, format(in_qty,'.2f') or 0.00,text_left)
                            worksheet[c].write(i,5, format(out_qty,'.2f') or 0.00,text_left)
                            worksheet[c].write(i,6, format(new_qty_avb,'.2f') or 0.00,text_left)
                            cu_value = 0
                            received  = 0
                            sales  = 0
                            ending =  0
                            if in_qty > 0:
                                cu_value = quat_value / in_qty
                                received = in_qty * cu_value
                                ending = fina_qty_avb + received
                                fina_qty_avb = ending
    #
                            if out_qty > 0:
                                cu_value = quat_value / out_qty
                                sales = out_qty * cu_value
                                ending = fina_qty_avb - sales
                                fina_qty_avb = ending
#                            if is_internal:
#                                ending = fina_qty_avb
                            worksheet[c].write(i,7, format(cu_value,'.2f') or 0.00,text_left)
                            worksheet[c].write(i,8, format(received,'.2f') or 0.00,text_left)
                            worksheet[c].write(i,9, format(sales,'.2f') or 0.00,text_left)
                            worksheet[c].write(i,10, format(ending,'.2f') or 0.00,text_left)
    #
                            i+=1
                        i+=1
        fp = StringIO()
        workbook.save(fp)
        export_id = self.env['dev.product.movement.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        fp.close()





        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'dev.product.movement.excel',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return True

class dev_product_movement_excel(models.TransientModel):
    _name= "dev.product.movement.excel"

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File')
