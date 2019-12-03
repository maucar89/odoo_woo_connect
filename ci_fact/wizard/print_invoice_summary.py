# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 BroadTech IT Solutions Pvt Ltd
#    (<http://broadtech-innovations.com>).
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

from odoo import models, fields, api, _
import xlwt
from cStringIO import StringIO
import base64
from xlwt import easyxf
import datetime

class PrintInvoiceSummary(models.TransientModel):
    _name = "print.invoice.summary"

    @api.model
    def _get_from_date(self):
        company = self.env.user.company_id
        current_date = datetime.date.today()
        from_date = company.compute_fiscalyear_dates(current_date)['date_from']
        return from_date

    from_date = fields.Date(string='Desde',default=_get_from_date)
    to_date = fields.Date(string='Hasta',default=datetime.date.today())
    invoice_summary_file = fields.Binary('Reporte Facturas - CI')
    file_name = fields.Char('Nombre Archivo')
    invoice_report_printed = fields.Boolean('Reporte de Facturas')
    invoice_status = fields.Selection([('all', 'All'), ('paid', 'Paid'),('un_paid', 'Unpaid')], string='Invoice Status')


    @api.multi
    def action_print_invoice_summary(self):
        workbook = xlwt.Workbook()
        amount_tot = 0
        column_heading_style = easyxf('font:height 200;font:bold True;')
        worksheet = workbook.add_sheet('Invoice Summary')
        worksheet.write(2, 3, self.env.user.company_id.name, easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(4, 2, self.from_date, easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(4, 3, 'To',easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(4, 4, self.to_date,easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(6, 0, _('Nro Factura'), column_heading_style)
        worksheet.write(6, 1, _('Cliente'), column_heading_style)
        worksheet.write(6, 2, _('Fecha'), column_heading_style)
        worksheet.write(6, 3, _('Monto total'), column_heading_style)
        worksheet.write(6, 4, _('Moneda Fact'), column_heading_style)
        worksheet.write(6, 5, _('Diario'), column_heading_style)

        worksheet.col(0).width = 5000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 8000

        worksheet2 = workbook.add_sheet('Reporte de Facturas por Cliente')
        worksheet2.write(1, 0, _('Cliente'), column_heading_style)
        worksheet2.write(1, 1, _('Monto Pagado'), column_heading_style)
        worksheet2.write(1, 2, _('Moneda Fact'), easyxf('font:height 200;font:bold True;align: horiz left;'))
        worksheet2.write(1, 3, _('Moneda Compañia (' + str(self.env.user.company_id.currency_id.name) + ')'), easyxf('font:height 200;font:bold True;align: horiz left;'))
        worksheet2.col(0).width = 5000
        worksheet2.col(1).width = 5000
        worksheet2.col(2).width = 4000
        worksheet2.col(3).width = 8000

        row = 7
        customer_row = 2
        for wizard in self:
            customer_payment_data = {}
            heading =  'Reporte de Factura - CI'
            worksheet.write_merge(0, 0, 0, 5, heading, easyxf('font:height 210; align: horiz center;pattern: pattern solid, fore_color black; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            heading =  'Reporte de facturas por cliente'
            worksheet2.write_merge(0, 0, 0, 3, heading, easyxf('font:height 200; align: horiz center;pattern: pattern solid, fore_color black; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            if wizard.invoice_status == 'all':
                invoice_objs = self.env['account.invoice'].search([('date_invoice','>=',wizard.from_date),
                                                               ('date_invoice','<=',wizard.to_date),
                                                               ('type','=','out_invoice'),
                                                               ('state','not in',['draft','cancel'])])
            elif wizard.invoice_status == 'paid':
                invoice_objs = self.env['account.invoice'].search([('date_invoice','>=',wizard.from_date),
                                                               ('date_invoice','<=',wizard.to_date),
                                                               ('state','=','paid'),('type','=','out_invoice')])
            else:
                invoice_objs = self.env['account.invoice'].search([('date_invoice','>=',wizard.from_date),
                                                               ('date_invoice','<=',wizard.to_date),
                                                               ('state','=','open'),('type','=','out_invoice')])
            for invoice in invoice_objs:
                amount = 0
                for journal_item in invoice.move_id.line_ids:
                    amount += journal_item.debit
                worksheet.write(row, 0, invoice.number)
                worksheet.write(row, 1, invoice.partner_id.name)
                worksheet.write(row, 2, invoice.date_invoice)
                worksheet.write(row, 3, invoice.amount_total)
                worksheet.write(row, 4, invoice.journal_id)
                worksheet.write(row, 5, amount)
                amount_tot += amount
                row += 1
                key = u'_'.join((invoice.partner_id.name, invoice.currency_id.name)).encode('utf-8')
                key = unicode(key, 'utf-8')
                if key not in customer_payment_data:
                    customer_payment_data.update({key: {'amount_total': invoice.amount_total, 'amount_company_currency': amount}})
                else:
                    paid_amount_data = customer_payment_data[key]['amount_total'] + invoice.amount_total
                    amount_currency = customer_payment_data[key]['amount_company_currency'] + amount
                    customer_payment_data.update({key: {'amount_total': paid_amount_data, 'amount_company_currency': amount_currency}})
            worksheet.write(row+2, 5, amount_tot, column_heading_style)

            for customer in customer_payment_data:
                worksheet2.write(customer_row, 0, customer.split('_')[0])
                worksheet2.write(customer_row, 1, customer_payment_data[customer]['amount_total'])
                worksheet2.write(customer_row, 2, customer.split('_')[1])
                worksheet2.write(customer_row, 3, customer_payment_data[customer]['amount_company_currency'])
                customer_row += 1


            fp = StringIO()
            workbook.save(fp)
            excel_file = base64.encodestring(fp.getvalue())
            wizard.invoice_summary_file = excel_file
            wizard.file_name = 'Invoice Summary Report.xls'
            wizard.invoice_report_printed = True
            fp.close()
            return {
                    'view_mode': 'form',
                    'res_id': wizard.id,
                    'res_model': 'print.invoice.summary',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self.env.context,
                    'target': 'new',
                       }


 # vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
