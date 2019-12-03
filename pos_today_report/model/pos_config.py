# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import datetime
from datetime import timedelta
import pytz
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

class pos_config(models.Model):
    _inherit = 'pos.config'

    @api.multi
    def get_pos_order_today(self):
        today = datetime.strptime(self.convert_utc_tz(datetime.today())[0], DEFAULT_SERVER_DATETIME_FORMAT)
        d_from = self.convert_tz_utc(today.replace(hour=00, minute=00, second=00))
        d_to = self.convert_tz_utc((today + timedelta(days=1)).replace(hour=00, minute=00, second=00))
        return self.env['pos.order'].search([
            ('config_id', '=', self.id),
            ('date_order', '>=', d_from),
            ('date_order', '<=', d_to)
        ])

    @api.multi
    def get_pos_order_yesterday(self):
        today = datetime.strptime(self.convert_utc_tz(datetime.today())[0], DEFAULT_SERVER_DATETIME_FORMAT)
        d_to = self.convert_tz_utc(today.replace(hour=00, minute=00, second=00))
        d_from = self.convert_tz_utc((today - timedelta(days=1)).replace(hour=00, minute=00, second=00))
        return self.env['pos.order'].search([
            ('config_id', '=', self.id),
            ('date_order', '>=', d_from),
            ('date_order', '<=', d_to)
        ])

    @api.multi
    def get_today(self):
        today = datetime.strptime(self.convert_utc_tz(datetime.today())[0],
                                  DEFAULT_SERVER_DATETIME_FORMAT)
        return datetime.strftime(today, "%m/%d/%Y")

    @api.multi
    def get_yesterday(self):
        today = datetime.strptime(self.convert_utc_tz(datetime.today() - timedelta(days=1))[0],
                                  DEFAULT_SERVER_DATETIME_FORMAT)
        return datetime.strftime(today, "%m/%d/%Y")

    @api.one
    def convert_tz_utc(self, dt=None):
        if not dt:
            dt = datetime.today()
        user = self.env['res.users'].browse(self.env.uid)
        if user.tz:
            tz = user.tz
        elif self.env.context.get('tz', False):
            tz = self.env.context['tz']
        if tz:
            utc = pytz.timezone('UTC')
            tz = pytz.timezone(tz)
            tz_timestamp = tz.localize(dt, is_dst=False)
            utc_timestamp = tz_timestamp.astimezone(utc)
            str_dt = datetime.strftime(utc_timestamp, DEFAULT_SERVER_DATETIME_FORMAT)
            return str_dt
        else:
            return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    @api.one
    def convert_utc_tz(self, dt=None):
        if not dt:
            dt = datetime.today()
        user = self.env['res.users'].browse(self.env.uid)
        if user.tz:
            tz = user.tz
        elif self.env.context.get('tz', False):
            tz = self.env.context['tz']
        if tz:
            utc = pytz.timezone('UTC')
            tz = pytz.timezone(tz)
            utc_timestamp = utc.localize(dt, is_dst=False)
            tz_timestamp = utc_timestamp.astimezone(tz)
            str_dt = datetime.strftime(tz_timestamp, DEFAULT_SERVER_DATETIME_FORMAT)
            return str_dt
        else:
            return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)