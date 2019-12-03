# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SeqAccountMove(models.Model):
    _inherit = 'account.move'

    seq_name = fields.Char(string="Sequence",readonly=True,default="Nuevo")

    @api.model
    def create(self,vals):
        if vals.get('seq_name', "Nuevo") == "Nuevo":
            vals['seq_name'] = self.env['ir.sequence'].next_by_code('account.move') or "Nuevo"
            res = super(SeqAccountMove, self).create(vals)
            return res
