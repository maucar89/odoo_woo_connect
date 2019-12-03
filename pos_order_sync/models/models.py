# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import UserError, Warning,ValidationError, RedirectWarning
from datetime import datetime, timedelta
from odoo import SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PosConfig(models.Model):
	_inherit = ['pos.config']
	quotation_print_type = fields.Selection([('pdf','Browser based (Pdf Report)'),('posbox','POSBOX (Xml Report)')],default='pdf', required=True,string="Quotation Print Type")

	@api.one
	def _compute_all_active_session(self):
		all_session_ids = self.env['pos.session'].search([('state', '=', 'opened')]).ids
		self.all_active_session_ids = all_session_ids

	@api.one
	@api.constrains('quotation_print_type','iface_print_via_proxy')
	def check_hardware_connection(self):
		if (self.quotation_print_type == 'posbox'):
			if(self.iface_print_via_proxy == False):
				raise UserError("You can not print Xml receipt. Please check receipt printer in Hardware Proxy / PosBox")

class PosOrder(models.Model):
	_inherit = ['pos.order']
	quote_id = fields.Many2one("pos.quote", string="Related Quote")

	@api.model
	def _order_fields(self, ui_order):
		fields_return = super(PosOrder, self)._order_fields(ui_order)
		fields_return.update({'quote_id': ui_order.get('quote_id', '')})
		return fields_return

	@api.model
	def create(self, vals):
		record = super(PosOrder, self).create(vals)
		if vals.get('quote_id'):
			quote_obj = self.env['pos.quote'].browse(vals['quote_id'])
			quote_obj.write({'state': 'done'})
		return record


class PosQuotes(models.Model):
	_name='pos.quote'

	quote_id = fields.Char('Quote Identifier',readonly=True)
	name = fields.Char("Name")
	user_id = fields.Many2one('res.users', 'Salesman')
	date_order = fields.Datetime('Quote Date', readonly=True, select=True)
	lines = fields.One2many('pos.quote.line', 'quote_id', 'Quote Lines',readonly=True)
	pricelist_id = fields.Many2one(
		'product.pricelist', 'Pricelist',readonly=True)
	partner_id = fields.Many2one('res.partner', 'Customer')
	session_id = fields.Many2one(
		'pos.session', 'From POS Session', select=1, readonly=True)
	note = fields.Text('Internal Notes')
	to_session_id = fields.Many2one('pos.session', 'To POS Session', select=1, readonly=True)
	amount_total = fields.Float(
		string='Total', digits=0, multi='all', readonly=True)
	amount_tax = fields.Float(
		string='Taxes', digits=0, multi='all', readonly=True)
	state = fields.Selection([
		("draft", "Draft"),
		("done", "Done"),
		("cancel", "Cancel")],
		default='draft')
	fiscal_position_id = fields.Many2one(
		'account.fiscal.position', 'Fiscal Position',readonly=True)
	quote_sent = fields.Boolean('Quote sent')

	@api.multi
	def write(self, vals):
		for obj in self:
			if vals.has_key('quote_id'):
				found_ids = self.env['pos.quote'].search(
					[('quote_id', '=', vals['quote_id'])]).ids
				if len(found_ids) > 0:
					raise UserError(
						"Please use some other Quote Id !!!\nThis id has already been used for some other quote.")
		return super(PosQuotes, self).write(vals)
	
	@api.model
	def create(self, vals):
		if vals.get('quote_id') == '' or not vals.get('quote_id'):
			vals['quote_id'] =self.env['ir.sequence'].next_by_code('pos.quote')
		result = super(PosQuotes, self).create(vals)
		return result


	@api.model
	def print_quote(self):
		report_ids = self.env['ir.actions.report.xml'].search([(
			'model', '=', 'pos.quote'), ('report_name', '=', 'pos_order_sync.quote_order_report')]).ids
		return report_ids and report_ids[0] or False

	@api.model
	def search_all_record(self,kwargs):
		results = {}
		record_list = []
		quote_ids = self.search([('quote_id','not in',kwargs['quote_ids']),('state', '=', 'draft'),
			('to_session_id', '=', kwargs['session_id'])]).ids
		quote_objs = self.browse(quote_ids)
		for quote_obj in quote_objs:
			result = {}
			result['status'] = True
			result['quote_obj_id'] = quote_obj.id
			result['quote_id'] = quote_obj.quote_id
			result['pricelist_id'] = quote_obj.pricelist_id.id
			result['note'] = quote_obj.note
			result['amount_total'] = quote_obj.amount_total
			result['amount_tax'] = quote_obj.amount_tax
			result['partner_id'] = [quote_obj.partner_id.id,quote_obj.partner_id.name]
			result['to_session_id'] = quote_obj.to_session_id.id
			result['from_session_id'] = quote_obj.session_id.config_id.display_name
			result['message'] = 'Quote Id does not belong to this POS session .'
			result['line'] = []
			for line in quote_obj.lines:
				orderline = {}
				orderline['product_id'] = line.product_id.id
				orderline['price_unit'] = line.price_unit
				orderline['qty'] = line.qty
				orderline['discount'] = line.discount
				result['line'].append(orderline)
			record_list.append(result)
		results['quote_list'] = record_list
		return results

	@api.model
	def load_quote_history(self,kwargs):
		results = {}
		quote_list =[]
		quote_objs = self.search([('session_id','=',kwargs['session_id'])])
		for quote_obj in quote_objs:
			result = {}
			result['quote_id'] = quote_obj.quote_id
			if quote_obj.partner_id.name:
				result['partner_id'] = quote_obj.partner_id.name
			else :
				result['partner_id'] = '-'
			result['amount_total'] = quote_obj.amount_total
			result['to_session_id'] = quote_obj.to_session_id.config_id.display_name
			result["state"] = quote_obj.state[0].upper() +  quote_obj.state[1:]
			quote_list.append(result)
		results['quote_list'] = quote_list
		return results

	@api.one
	def click_cancel(self):
		self.state = 'cancel'

	@api.model
	def change_state_done(self,kwargs):
		quote_object = self.search([('id','=',kwargs['quote_id'])])
		for quote_obj in quote_object:	
			quote_obj.write({'state':'done'})
		return True

	@api.multi
	@api.depends('quote_id')
	def name_get(self):
		'''Overridden name_get() method for returning the registered number as name'''
		res = []
		for record in self:
			name = str(record.quote_id)
			res.append((record.id, name))
		return res

class PosQuoteLine(models.Model):
	_name = 'pos.quote.line'

	quote_id = fields.Many2one("pos.quote")
	name = fields.Char("Line", default="Quote Line")
	product_id = fields.Many2one('product.product', 'Product', domain=[(
		'sale_ok', '=', True), ('available_in_pos', '=', True)], required=True, change_default=True)
	price_unit = fields.Float(string='Unit Price', digits=0)
	qty = fields.Float('Quantity')
	price_subtotal = fields.Float(digits=0, string='Subtotal w/o Tax')
	price_subtotal_incl = fields.Float(digits=0, string='Subtotal')
	discount = fields.Float('Discount (%)', digits=0)
	tax_ids = fields.Many2many('account.tax', string='Taxes')
	tax_ids_after_fiscal_position = fields.Many2many('account.tax', string='Taxes')
	notice = fields.Char('Discount Notice')

	@api.model
	def create(self, vals):
		if vals.has_key("quote_tax_ids"):
			tax_ids_list = vals['quote_tax_ids']
			vals['tax_ids'] = [(6, 0, tax_ids_list)]
			del vals['quote_tax_ids']
		record = super(PosQuoteLine, self).create(vals)
		return record

