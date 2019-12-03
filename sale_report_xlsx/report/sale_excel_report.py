# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2018 darkknightapps@gmail.com
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from datetime import datetime

from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class SalesReportXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        report_header = lines and lines[0] or False
        sheet = workbook.add_worksheet('Reporte Ventas')
        format1 = workbook.add_format({
            'font_size': 16,
            'bottom': True,
            'right': True,
            'left': True,
            'top': True,
            'align': 'vcenter',
            'bold': True
        })
        format11 = workbook.add_format({
            'font_size': 12,
            'align': 'center',
            'right': True,
            'left': True,
            'bottom': True,
            'top': True,
            'bold': True
        })
        format3 = workbook.add_format({
            'bottom': True,
            'top': True,
            'font_size': 12
        })
        font_size_10 = workbook.add_format({
            'bottom': True,
            'top': True,
            'right': True,
            'left': True,
            'font_size': 10
        })
        format3.set_align('center')
        format1.set_align('center')
        # Report main header
        sheet.merge_range('A1:Q1', 'Reporte Ventas Sarumadi SRL', format1)
        # Report filter header
        sheet.merge_range('A2:E2', 'Rango de Fechas', format11)
        sheet.merge_range('F2:G2', 'Estado Orden', format11)
        sheet.merge_range('H2:I2', 'Plazo Pago', format11)
        sheet.merge_range('J2:K2', 'Asesor', format11)
        sheet.merge_range('L2:M2', 'Equipo Venta', format11)
        sheet.merge_range('N2:O2', 'Clientes', format11)
        sheet.merge_range('P2:Q2', 'Productos', format11)
        # Report filter values
        date_from = datetime.strptime(report_header.date_from, '%Y-%m-%d').strftime(
            '%d/%m/%Y')
        date_to = datetime.strptime(report_header.date_to, '%Y-%m-%d').strftime(
            '%d/%m/%Y')
        date_range = date_from + '-' + date_to
        customers = ''
        partner_count = 0
        for partner in report_header.partner_ids:
            if partner_count == 0:
                customers += partner.name
            else:
                customers += ',\n' + partner.name
            partner_count += 1
        products = ''
        product_count = 0
        for product in report_header.product_ids:
            if product_count == 0:
                products += product.name
            else:
                products += ',\n' + product.name
            product_count += 1
        sheet.merge_range('A3:E3', date_range or '', format3)
        sheet.merge_range('F3:G3', report_header.order_state or '', format3)
        sheet.merge_range('H3:I3', report_header.payment_term or '', format3)
        sheet.merge_range('J3:K3', report_header.user or '', format3)
        sheet.merge_range('L3:M3', report_header.team or '', format3)
        sheet.merge_range('N3:O3', customers or ' ', format3)
        sheet.merge_range('P3:Q3', products or ' ', format3)

        # Empty row
        sheet.merge_range('A4:Q4', '', format1)
        # Report items header
        sheet.write(4, 0, 'Fecha Orden', format11)
        sheet.write(4, 1, 'Orden #', format11)
        sheet.write(4, 2, 'Cliente', format11)
        sheet.write(4, 3, 'Asesor', format11)
        sheet.write(4, 4, 'Equipo de Venta', format11)
        sheet.write(4, 5, 'Plazo Pago', format11)
        sheet.write(4, 6, 'Estado Orden', format11)
        sheet.write(4, 7, 'Producto', format11)
        sheet.write(4, 8, 'Cantidad', format11)
        sheet.write(4, 9, 'Unidad Medida', format11)
        sheet.write(4, 10, 'Precio Unitario', format11)
        sheet.write(4, 11, 'Impuestos', format11)
        sheet.write(4, 12, 'Total', format11)
        # Totals
        qty_total = 0.00
        price_unit_total = 0.00
        tax_total = 0.00
        amount_total = 0.00
        # Report item values
        item_row_no = 5
        for line in report_header.line_ids:
            sheet.write(item_row_no, 0, line.order_id.date_order or '', font_size_10)
            sheet.write(item_row_no, 1, line.order_id.name or '', font_size_10)
            sheet.write(item_row_no, 2, line.order_id.partner_id.name or '', font_size_10)
            sheet.write(item_row_no,
                        3,
                        line.order_id.user_id and line.order_id.user_id.name or '',
                        font_size_10)
            sheet.write(item_row_no,
                        4,
                        line.order_id.team_id and line.order_id.team_id.name or '',
                        font_size_10)
            sheet.write(item_row_no,
                        5,
                        line.order_id.payment_term_id and line.order_id.payment_term_id.name or '',
                        font_size_10)
            sheet.write(item_row_no, 6, line.order_id.state.capitalize(), font_size_10)
            sheet.write(item_row_no,
                        7,
                        line.product_id and line.product_id.name or line.name or '',
                        font_size_10)
            sheet.write(item_row_no, 8, line.product_uom_qty or 0.00, font_size_10)
            sheet.write(item_row_no,
                        9,
                        line.product_uom and line.product_uom.name or '',
                        font_size_10)
            sheet.write(item_row_no, 10, line.price_unit or 0.00, font_size_10)
            sheet.write(item_row_no, 11, line.price_tax or 0.00, font_size_10)
            sheet.write(item_row_no, 12, line.price_total or 0.00, font_size_10)
            qty_total += line.product_uom_qty
            price_unit_total += line.price_unit
            tax_total += line.price_tax
            amount_total += line.price_total
            item_row_no += 1
        # Report total row
        sheet.write(item_row_no, 0, 'Total: ', format11)
        sheet.write(item_row_no, 1, ' ', format11)
        sheet.write(item_row_no, 2, ' ', format11)
        sheet.write(item_row_no, 3, ' ', format11)
        sheet.write(item_row_no, 4, ' ', format11)
        sheet.write(item_row_no, 5, ' ', format11)
        sheet.write(item_row_no, 6, ' ', format11)
        sheet.write(item_row_no, 7, ' ', format11)
        sheet.write(item_row_no, 8, qty_total, format11)
        sheet.write(item_row_no, 9, ' ', format11)
        sheet.write(item_row_no, 10, price_unit_total, format11)
        sheet.write(item_row_no, 11, tax_total, format11)
        sheet.write(item_row_no, 12, amount_total, format11)

SalesReportXlsx(
    'report.sale_report_xlsx.sale_report_excel_export.xlsx',
    'sale.excel.export.header'
)
