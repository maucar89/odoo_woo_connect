# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from openerp import models, fields, api, _
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class pos_order(models.Model):
    _inherit="pos.order"

    total_loyalty_earned_points = fields.Float("Earned Loyalty Points")
    total_loyalty_earned_amount = fields.Float("Earned Loyalty Amount")
    total_loyalty_redeem_points = fields.Float("Redeemed Loyalty Points")
    total_loyalty_redeem_amount = fields.Float("Redeemed Loyalty Amount")

    @api.model
    def _order_fields(self, ui_order):
        res = super(pos_order, self)._order_fields(ui_order)
        res.update({
            'total_loyalty_earned_points': ui_order.get('loyalty_earned_point') or 0.00,
            'total_loyalty_earned_amount': ui_order.get('loyalty_earned_amount') or 0.00,
            'total_loyalty_redeem_points': ui_order.get('loyalty_redeemed_point') or 0.00,
            'total_loyalty_redeem_amount': ui_order.get('loyalty_redeemed_amount') or 0.00,
        })
        return res

    @api.model
    def _process_order(self, order):
        res = super(pos_order, self)._process_order(order)
        if res.session_id.config_id.enable_pos_loyalty and res.partner_id:
            loyalty_setting_id = self.env['loyalty.config.settings'].sudo().search([],order="id desc", limit=1)
            if loyalty_setting_id:
                if loyalty_setting_id.points_based_on and order.get('loyalty_earned_point'):
                    point_vals = {
                        'pos_order_id': res.id,
                        'partner_id': res.partner_id.id,
                        'points': order.get('loyalty_earned_point'),
                        'amount_total': (float(order.get('loyalty_earned_point')) * loyalty_setting_id.to_amount) / loyalty_setting_id.points
                    }
                    loyalty = self.env['loyalty.point'].create(point_vals)
                    if loyalty and res.partner_id.send_loyalty_mail:
                        try:
                            template_id = self.env['ir.model.data'].get_object_reference('aspl_pos_loyalty', 'email_template_pos_loyalty')
                            template_obj = self.env['mail.template'].browse(template_id[1])
                            template_obj.send_mail(loyalty.id,force_send=True, raise_exception=True)
                        except Exception, e:
                            _logger.error('Unable to send email for order %s',e)
                if order.get('loyalty_redeemed_point'):
                    redeemed_vals = {
                        'redeemed_pos_order_id': res.id,
                        'partner_id': res.partner_id.id,
                        'redeemed_amount_total': self._calculate_amount_total_by_points(loyalty_setting_id, order.get('loyalty_redeemed_point')),
                        'redeemed_point': order.get('loyalty_redeemed_point'),
                    }
                    self.env['loyalty.point.redeem'].create(redeemed_vals)
        return res

    def _calculate_amount_total_by_points(self, loyalty_config, points):
        return (float(points) * loyalty_config.to_amount) / loyalty_config.points

    def get_point_from_category(self, categ_id):
        if categ_id.loyalty_point:
            return categ_id.loyalty_point
        elif categ_id.parent_id:
            self.get_point_from_category(categ_id.parent_id)
        return False

    def _calculate_loyalty_points_by_order(self, loyalty_config):
        if loyalty_config.point_calculation:
            earned_points = self.amount_total * loyalty_config.point_calculation / 100
            amount_total = (earned_points * loyalty_config.to_amount) / loyalty_config.points
            return {
                'points': earned_points,
                'amount_total': amount_total
            }
        return False

    @api.multi
    def refund(self):
        res = super(pos_order, self).refund()
        LoyaltyPoints = self.env['loyalty.point']
        refund_order_id = self.browse(res.get('res_id'))
        if refund_order_id:
            LoyaltyPoints.create({
                'pos_order_id': refund_order_id.id,
                'partner_id': self.partner_id.id,
                'points': refund_order_id.total_loyalty_redeem_points,
                'amount_total': refund_order_id.total_loyalty_redeem_amount,
                
            })
            LoyaltyPoints.create({
                'pos_order_id': refund_order_id.id,
                'partner_id': self.partner_id.id,
                'points': refund_order_id.total_loyalty_earned_points * -1,
                'amount_total': refund_order_id.total_loyalty_earned_amount * -1,
                
            })
            refund_order_id.write({
                'total_loyalty_earned_points': refund_order_id.total_loyalty_earned_points * -1,
                'total_loyalty_earned_amount': refund_order_id.total_loyalty_earned_amount * -1,
                'total_loyalty_redeem_points': 0.00,
                'total_loyalty_redeem_amount': 0.00,
            })
        return res


class product_product(models.Model):
    _inherit = "product.product"

    loyalty_point = fields.Integer("Loyalty Point")


class product_category(models.Model):
    _inherit = "pos.category"

    loyalty_point = fields.Integer("Loyalty Point")


class pos_config(models.Model):
    _inherit = "pos.config"

    enable_pos_loyalty = fields.Boolean("Enable Loyalty")
    loyalty_journal_id = fields.Many2one("account.journal","Loyalty Journal")


class loyalty_point(models.Model):
    _name = "loyalty.point"
    _order = 'id desc'
    _rec_name = "pos_order_id"

    pos_order_id =  fields.Many2one("pos.order", string="Order", readonly=1)
    partner_id = fields.Many2one('res.partner', 'Member', readonly=1)
    amount_total = fields.Float('Total Amount', readonly=1)
    date = fields.Datetime('Date', readonly=1, default=datetime.now())
    points = fields.Float('Point', readonly=1)


class loyalty_point(models.Model):
    _name = "loyalty.point.redeem"
    _order = 'id desc'
    _rec_name = "redeemed_pos_order_id"

    redeemed_pos_order_id =  fields.Many2one("pos.order", string="Order")
    partner_id = fields.Many2one('res.partner', 'Member', readonly=1)
    redeemed_amount_total = fields.Float('Redeemed Amount', readonly=1)
    redeemed_date = fields.Datetime('Date', readonly=1, default=datetime.now())
    redeemed_point = fields.Float('Point', readonly=1)


class res_partner(models.Model):
    _inherit="res.partner"

    @api.model
    def loyalty_reminder(self):
        partner_ids = self.search([('email', "!=", False), ('send_loyalty_mail', '=', True)])
        for partner_id in partner_ids.filtered(lambda partner: partner.remaining_loyalty_points > 0):
            try:
                template_id = self.env['ir.model.data'].get_object_reference('aspl_pos_loyalty', 'email_template_loyalty_reminder')
                template_obj = self.env['mail.template'].browse(template_id[1])
                template_obj.send_mail(partner_id.id,force_send=True, raise_exception=True)
            except Exception, e:
                _logger.error('Unable to send email for order %s',e)

    @api.multi
    def _calculate_earned_loyalty_points(self):
        loyalty_point_obj = self.env['loyalty.point']
        for partner in self:
            total_earned_points = 0.00
            for earned_loyalty in loyalty_point_obj.search([('partner_id', '=', partner.id)]):
                total_earned_points += earned_loyalty.points
            partner.loyalty_points_earned = total_earned_points

    @api.multi
    def _calculate_remaining_loyalty(self):
        loyalty_point_obj = self.env['loyalty.point']
        loyalty_point_redeem_obj = self.env['loyalty.point.redeem']
        for partner in self:
            points_earned = 0.00
            amount_earned = 0.00
            points_redeemed = 0.00
            amount_redeemed = 0.00
            for earned_loyalty in loyalty_point_obj.search([('partner_id', '=', partner.id)]):
                points_earned += earned_loyalty.points
                amount_earned += earned_loyalty.amount_total
            for redeemed_loyalty in loyalty_point_redeem_obj.search([('partner_id', '=', partner.id)]):
                points_redeemed += redeemed_loyalty.redeemed_point
                amount_redeemed += redeemed_loyalty.redeemed_amount_total
            partner.remaining_loyalty_points = points_earned - points_redeemed
            partner.remaining_loyalty_amount = amount_earned - amount_redeemed
            partner.total_remaining_points = points_earned - points_redeemed

    loyalty_points_earned = fields.Float(compute=_calculate_earned_loyalty_points)
    remaining_loyalty_points = fields.Float("Remaining Loyalty Points", readonly=1, compute=_calculate_remaining_loyalty)
    remaining_loyalty_amount = fields.Float("Points to Amount", readonly=1, compute=_calculate_remaining_loyalty)
    send_loyalty_mail = fields.Boolean("Send Loyalty Mail", default=True)
    total_remaining_points   = fields.Float("Total Loyalty Points", related='remaining_loyalty_points', readonly=1)


class account_journal(models.Model):
    _inherit="account.journal"

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self._context.get('loyalty_jr'):
            if self._context.get('journal_ids') and \
               self._context.get('journal_ids')[0] and \
               self._context.get('journal_ids')[0][2]:
               args += [['id', 'in', self._context.get('journal_ids')[0][2]]]
            else:
                return False;
        return super(account_journal, self).name_search(name, args=args, operator=operator, limit=limit)
