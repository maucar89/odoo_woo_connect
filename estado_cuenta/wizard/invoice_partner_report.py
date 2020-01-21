# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar
#========For Excel========
from io import BytesIO
import xlwt
from xlwt import easyxf
import base64
# =====================

import itertools
from operator import itemgetter
import operator

class invoice_partner_report(models.TransientModel):
    _name = "invoice.partner.report"

    @api.model
    def _get_from_date(self):
        date = datetime.now()
        month = date.month
        if date.month < 10:
            month = '0'+str(date.month)
        date = str(date.year)+'-'+str(month)+'-01'
        return date

    @api.model
    def _get_to_date(self):
        date = datetime.now()
        m_range = calendar.monthrange(date.year,date.month)
        month = date.month
        if date.month < 10:
            month = '0'+str(date.month)
        date = str(date.year)+'-'+str(month)+'-'+str(m_range[1])
        return date

    _states = [('draft','Borrador'),('open','Abierta'),('paid','Pagada'),('open_paid','Validadas')]
    _filter_by = [('comercial_user','Asesor'),('partner','Cliente'),('partner_category','Categoria')]

    start_date = fields.Date(string='Fecha Inicial', required="1", default=_get_from_date)
    end_date = fields.Date(string='Fecha Final', required="1", default=_get_to_date)
    state  = fields.Selection(_states, string='Estado', default='open', required="1")

    filter_by  = fields.Selection(_filter_by, string='Filtrar por', default='partner', required="1")

    partner_ids = fields.Many2many('res.partner', string='Cliente')
    user_ids = fields.Many2many('res.users', string='Asesor')
    category_ids = fields.Many2many('res.partner.hcategory', string='Categoria de Cliente')
    excel_file = fields.Binary('Excel File')
    inv_type = fields.Selection([('out_invoice','Factura Cliente'),
                                 ('out_refund','Nota Debito'),
                                 ('in_invoice','Factura Proveedor'),
                                 ('in_refund','Nota Credito'),
                                 ('out_invoice_refund','Factura y Nota Clientes'),
                                 ('in_invoice_refund','Factura y Nota Proveedor')], string='Tipo Factura', required="1", default='out_invoice')


    @api.multi
    def get_style(self):
        main_header_style = easyxf('font:height 300;'
                                   'align: horiz center;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin")

        header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz center;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        group_style1 = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz left;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        group_style2 = easyxf('font:height 200;pattern: pattern solid, fore_color ivory;'
                              'align: horiz left;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        right_group_style1 = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz right;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin", num_format_str='0.00')

        right_group_style2= easyxf('font:height 200;pattern: pattern solid, fore_color ivory;'
                              'align: horiz right;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin", num_format_str='0.00')

        text_left = easyxf('font:height 200; align: horiz left;'
                            "borders: top thin,left thin,right thin,bottom thin")

        text_right = easyxf('font:height 200; align: horiz right;'
                            "borders: top thin,left thin,right thin,bottom thin", num_format_str='0.00')

        text_left_bold = easyxf('font:height 200; align: horiz right;font:bold True;'
                                "borders: top thin,left thin,right thin,bottom thin")

        text_right_bold = easyxf('font:height 200; align: horiz right;font:bold True;'
                                 "borders: top thin,left thin,right thin,bottom thin", num_format_str='0.00')
        text_center = easyxf('font:height 200; align: horiz center;'
                             "borders: top thin,left thin,right thin,bottom thin")

        return [main_header_style, group_style1,group_style2, right_group_style1, right_group_style2, header_style, text_left, text_right, text_left_bold, text_right_bold, text_center]

    @api.multi
    def create_excel_header(self,worksheet,main_header_style,header_style,text_left,row):
        worksheet.write_merge(0, 1, 3, 3, 'ESTADO DE CUENTA - CLIENTES SARUMADI', main_header_style)
        row = row

        worksheet.write(2, 0, 'DESDE', text_left)
        date = datetime.strptime(self.start_date, '%Y-%m-%d')
        date = datetime.strftime(date, "%d-%m-%Y")
        worksheet.write(2, 1, date, text_left)
        worksheet.write(3, 0, 'HASTA', text_left)
        date = datetime.strptime(self.end_date, '%Y-%m-%d')
        date = datetime.strftime(date, "%d-%m-%Y")
        worksheet.write(3, 1, date, text_left)

        row += 2
        return worksheet, row

    @api.multi
    def get_invoice(self,partner_id):
        domain = [('date_invoice','>=',self.start_date),('date_invoice','<=',self.end_date),('partner_id','=',partner_id)]
        if self.state == 'draft':
            domain.append(('state','=','draft'))
        elif self.state == 'open':
            domain.append(('state','=','open'))
        elif self.state == 'paid':
            domain.append(('state','=','paid'))
        elif self.state == 'open_paid':
            domain.append(('state','in',['open','paid']))

        if self.inv_type:
            if self.inv_type in ['out_invoice','in_invoice','out_refund','in_refund']:
                domain.append(('type','=',self.inv_type))
            else:
                if self.inv_type == 'out_invoice_refund':
                    domain.append(('type','in',['out_invoice','out_refund']))
                elif self.inv_type == 'in_invoice_refund':
                    domain.append(('type','in',['in_invoice','in_refund']))

        invoice_ids = self.env['account.invoice'].search(domain, order="date_invoice")
        return invoice_ids


    @api.multi
    def get_partners(self):
        if self.filter_by == 'partner':
            if self.partner_ids:
                return self.partner_ids.ids
            else:
                raise ValidationError(_('Por favor seleccione un Cliente !!!'))
        if self.filter_by == 'comercial_user':
            if self.user_ids:
                partner_ids = self.env['res.partner'].search([('user_id','in',self.user_ids.ids)])
                if not partner_ids:
                    raise ValidationError(_('Clientes no encontrados por Asesor !!!'))
                else:
                    return partner_ids.ids
            else:
                raise ValidationError(_('Por favor seleccione un Asesor !!!'))

        if self.filter_by == 'partner_category':
            if self.category_ids:
                partner_ids = []
                for category in self.category_ids:
                    for partner in category.partner_ids:
                        if partner.id not in partner_ids:
                            partner_ids.append(partner.id)
                if not partner_ids:
                    raise ValidationError(_('Clientes no encontrados por Categoria !!!'))
                else:
                    return partner_ids



    @api.multi
    def get_final_partner(self,partner_ids):
        final_partner_ids = []
        for partner_id in partner_ids:
            invoice_ids = self.get_invoice(partner_id)
            if invoice_ids:
                final_partner_ids.append(partner_id)
        return final_partner_ids




    @api.multi
    def get_partner_category(self,partner_id):
        category_ids = self.env['res.partner.hcategory'].search([])
        for category in category_ids:
            for partner in category.partner_ids:
                if partner.id == partner_id.id:
                    return category.name
        return 'Unknown'

    @api.multi
    def set_partner_dic(self,partner_ids):
        partner_ids = self.env['res.partner'].browse(partner_ids)
        partner_dic =[]
        for partner in partner_ids:
            partner_dic.append({
                'partner_id':partner.id,
                'user':partner.user_id and partner.user_id.name or 'Unknown User',
                'reference':partner.ref,
                'category':self.get_partner_category(partner)})

        n_lines=sorted(partner_dic,key=itemgetter('category'))
        groups = itertools.groupby(n_lines, key=operator.itemgetter('category'))
        lines = [{'category':k,'values':[x for x in v]} for k, v in groups]

        for line in lines:
            if line.get('values'):
                n_lines=sorted(line.get('values'),key=itemgetter('user'))
                groups = itertools.groupby(n_lines, key=operator.itemgetter('user'))
                line['values'] = [{'user':k,'values':[x for x in v]} for k, v in groups]

        return lines


    @api.multi
    def create_excel_table(self,worksheet,header_style, group_style1, group_style2, right_group_style1, right_group_style2, text_left, text_right, text_left_bold, text_right_bold,text_center,row):
        row = row + 2
        col=0
        worksheet.write(row,col, 'CATEGORIA CLIENTE', header_style)
        worksheet.write(row,col+1, 'ASESOR', header_style)
        worksheet.write(row,col+2, 'CODIGO', header_style)
        worksheet.write(row,col+3, 'CLIENTE', header_style)
        worksheet.write(row,col+4, 'NOTA', header_style)
        worksheet.write(row,col+5, 'FECHA', header_style)
        worksheet.write(row,col+6, 'FACTURA NRO', header_style)
        worksheet.write(row,col+7, 'IMPORTE', header_style)
        worksheet.write(row,col+8, 'ADEUDADO', header_style)
        worksheet.write(row,col+9, 'FECHA VENCIMIENTO', header_style)
        worksheet.write(row,col+10, 'DIAS DE MORA', header_style)
        row+=1
        partner_ids = self.get_partners()
        partner_ids = self.get_final_partner(partner_ids)
        if partner_ids:
            partner_dic = self.set_partner_dic(partner_ids)
            for dic in partner_dic:
                c_total = c_residual = 0
                worksheet.write_merge(row, row, 0, 10, dic.get('category'), group_style1)
                row+=1
                for val in dic.get('values'):
                    worksheet.write_merge(row, row, 1, 10, val.get('user'), group_style2)
                    row +=1
                    u_total = u_residual = 0
                    for v in val.get('values'):
                        col=2
                        if v.get('reference'):
                            worksheet.write(row,col, v.get('reference'), text_left)
                        col+=1
                        partner_name = self.env['res.partner'].browse(v.get('partner_id')).name
                        worksheet.write_merge(row, row, col, col+7, partner_name, text_left)
                        row+=1
                        invoice_ids = self.get_invoice(v.get('partner_id'))
                        for inv in invoice_ids:
                            col = 4
                            worksheet.write(row,col, inv.origin or '', text_center)
                            if inv.date_invoice:
                                inv_date = datetime.strptime(inv.date_invoice, '%Y-%m-%d')
                                pri_date = datetime.strftime(inv_date, "%d-%m-%Y")
                                worksheet.write(row,col+1, pri_date or '', text_center)
                            worksheet.write(row,col+2, inv.number or '', text_center)
                            u_total += inv.amount_total
                            u_residual += inv.residual
                            worksheet.write(row,col+3, inv.amount_total or 0.0, text_right)
                            worksheet.write(row,col+4, inv.residual or 0.0, text_right)
                            if inv.date_due:

                                due_date = datetime.strptime(inv.date_due, '%Y-%m-%d')
                                cur_date = date.today()
                                delta = due_date.date()-cur_date
                                days = str(delta.days)+ ' DIAS'
                                pri_date = datetime.strftime(due_date, "%d-%m-%Y")

                                worksheet.write(row,col+5, pri_date, text_center)
                                worksheet.write(row,col+6, days, text_center)
                            row+=1

                    worksheet.write_merge(row, row, 4, 6, 'TOTAL DE '+ val.get('user'), right_group_style2)
                    c_total += u_total
                    worksheet.write(row, 7, u_total, right_group_style2)
                    c_residual += u_residual
                    worksheet.write(row, 8, u_residual, right_group_style2)
                    worksheet.write(row, 9, '', right_group_style2)
                    worksheet.write(row, 10, '', right_group_style2)
                    row+=2
                worksheet.write_merge(row, row, 4, 6, 'TOTAL DE '+ dic.get('category'), right_group_style1)
                worksheet.write(row, 7, c_total, right_group_style1)
                worksheet.write(row, 8, c_residual, right_group_style1)
                worksheet.write(row, 9, '', right_group_style1)
                worksheet.write(row, 10, '', right_group_style1)
                row+=2





#        invoice_ids = self.get_invoice()
#        col=0
#        t_sub_total= t_discount= t_discount_bs= t_total = 0
#        count = 0
#        for invoice in invoice_ids:
#            for line in invoice.invoice_line_ids:
#                count += 1
#                worksheet.write(row,col, count, text_center)
#                date = ''
#                if invoice.date_invoice:
#                    date = datetime.strptime(invoice.date_invoice, '%Y-%m-%d')
#                    date = datetime.strftime(date, "%d-%m-%Y")
#                    worksheet.write(row,col+1, date, text_center)
#                worksheet.write(row,col+2, invoice.number or '', text_center)
#                worksheet.write(row,col+3, invoice.state or '', text_center)
#                worksheet.write(row,col+4, invoice.partner_id.name or '', text_left)
#                worksheet.write(row,col+5, line.price_subtotal or '', text_right)
#                t_sub_total += line.price_subtotal
#                discount = 0
#                if line.discount:
#                    discount = ((line.price_unit * line.quantity) * line.discount) / 100
#                    t_discount += discount
#
#                worksheet.write(row,col+6, discount or 0.0, text_right)
#                discount_bs = discount * 6.96
#                t_discount_bs += discount_bs
#                worksheet.write(row,col+7, discount_bs or 0.0, text_right)
#                t_total += line.price_subtotal - discount_bs
#                worksheet.write(row,col+8, line.price_subtotal - discount_bs or '', text_right)
#                row+=1
#
#        if t_sub_total or  t_discount or t_discount_bs or t_total:
#            worksheet.write_merge(row,row, 0, 4, 'TOTAL', text_left_bold)
#            worksheet.write(row,col+5, t_sub_total or 0.0, text_right_bold)
#            worksheet.write(row,col+6, t_discount or 0.0, text_right_bold)
#            worksheet.write(row,col+7, t_discount_bs or 0.0, text_right_bold)
#            worksheet.write(row,col+8, t_total or 0.0, text_right_bold)
#            row+=1
        return worksheet, row


    @api.multi
    def generate_excel(self):
        #====================================
        # Style of Excel Sheet
        excel_style = self.get_style()
        main_header_style = excel_style[0]
        group_style1 = excel_style[1]
        group_style2 = excel_style[2]
        right_group_style1 = excel_style[3]
        right_group_style2 = excel_style[4]
        header_style = excel_style[5]
        text_left = excel_style[6]
        text_right = excel_style[7]
        text_left_bold = excel_style[8]
        text_right_bold = excel_style[9]
        text_center = excel_style[10]
        # ====================================

        # Define Wookbook and add sheet
        workbook = xlwt.Workbook()
        filename = 'Estado de Cuenta.xls'
        worksheet = workbook.add_sheet('Estado de Cuenta')
        for i in range(0,20):
            worksheet.col(i).width = 150 * 30
            if i == 3:
                worksheet.col(i).width = 350 * 30


        # Print Excel Header
        worksheet,row = self.create_excel_header(worksheet,main_header_style,header_style,text_left,3)

        # Print Excel Table
        worksheet,row = self.create_excel_table(worksheet,header_style, group_style1,group_style2, right_group_style1, right_group_style2, text_left,text_right,text_left_bold,text_right_bold,text_center,row)


        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})

        if self.excel_file:
            active_id = self.ids[0]
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=invoice.partner.report&download=true&field=excel_file&id=%s&filename=%s' % (
                    active_id, filename),
                'target': 'new',
            }




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
