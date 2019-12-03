# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from datetime import timedelta

class ResCompany(models.Model):
    _inherit = "res.company"

    fiscalyear_last_day = fields.Integer(default=31, required=True)
    fiscalyear_last_month = fields.Selection([(1, 'January'), (2, 'February'),
        (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'),
        (11, 'November'), (12, 'December')], default=12, required=True)

    @api.multi
    def compute_fiscalyear_dates(self, date):
        """ Computes the start and end dates of the fiscalyear where the given 'date' belongs to
            @param date: a datetime object
            @returns: a dictionary with date_from and date_to
        """
        self = self[0]
        last_month = self.fiscalyear_last_month
        last_day = self.fiscalyear_last_day
        if (date.month < last_month or (date.month == last_month and date.day <= last_day)):
            date = date.replace(month=last_month, day=last_day)
        else:
            if last_month == 2 and last_day == 29 and (date.year + 1) % 4 != 0:
                date = date.replace(month=last_month, day=28, year=date.year + 1)
            else:
                date = date.replace(month=last_month, day=last_day, year=date.year + 1)
        date_to = date
        date_from = date + timedelta(days=1)
        if date_from.month == 2 and date_from.day == 29:
            date_from = date_from.replace(day=28, year=date_from.year - 1)
        else:
            date_from = date_from.replace(year=date_from.year - 1)
        return {'date_from': date_from, 'date_to': date_to}