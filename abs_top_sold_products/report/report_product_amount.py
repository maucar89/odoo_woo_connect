# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018-Today Ascetic Business Solution <www.asceticbs.com>
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
#################################################################################

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError



class ReportProductsAmount(models.AbstractModel):
    _name = 'report.abs_top_sold_products.report_products_amount'
    
    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        product_records = {}
        sorted_product_records = []
        sales = self.env['sale.order'].search([('state','in',('sale','done')),('date_order','>=',docs.start_date),('date_order','<=',docs.end_date)])
        for s in sales:
            orders = self.env['sale.order.line'].search([('order_id','=',s.id)])
            for order in orders:
                if order.product_id:
                    if order.product_id not in product_records:
                        product_records.update({order.product_id:0})
                    product_records[order.product_id] += order.price_subtotal

        for product_id, price_subtotal in sorted(product_records.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:docs.no_of_products]:
            sorted_product_records.append({'name':product_id.name, 'amount': int(price_subtotal), 'pricelist_id' : product_id.company_id.currency_id })

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'time': time,
            'products': sorted_product_records
        }
        return self.env['report'].render('abs_top_sold_products.report_products_amount', docargs)
