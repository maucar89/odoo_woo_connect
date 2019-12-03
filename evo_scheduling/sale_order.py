# -*- coding: utf-8 -*-

from openerp import _, api, fields, models
from datetime import datetime


class sale_order(models.Model):
	_inherit = 'sale.order'
	
	schedule_date = fields.Datetime("Scheduled Date")

	@api.multi
	def action_confirm(self):
		res = super(sale_order, self).action_confirm()
		for so in self:
			if not so.schedule_date:
				so.schedule_date = datetime.now()
		return res


class sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	@api.model
	def create(self, vals):
		res = super(sale_order_line, self).create(vals)
		total_diff = 0.0
		if res.order_id:
			if res.order_id.schedule_date:
				date = datetime.strptime(res.order_id.schedule_date,'%Y-%m-%d %H:%M:%S')
				total_diff = date.date() - datetime.now().date()
				res.customer_lead = float(str(total_diff.days))
			else:
				res.customer_lead = 0.0
		return res


class stock_picking(models.Model):
	_inherit = 'stock.picking'

	schedule_date = fields.Datetime("Scheduled Date")
	
	@api.model
	def create(self, vals):
		so_id = self.env['sale.order'].search([('name', '=', vals['origin'])])
		if so_id:
			if so_id.schedule_date:
				vals.update({'schedule_date':so_id.schedule_date})
			else:
				now = datetime.now()
				vals.update({'schedule_date':now})
		return super(stock_picking, self).create(vals)
