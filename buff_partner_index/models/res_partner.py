# -*- coding: utf-8 -*-
# © <2017> <builtforfifty>

from openerp import fields, models, api, _

class Partner(models.Model):
    _inherit = "res.partner"

    index = fields.Char(string='Index ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('X-00000'))
    index_char = fields.Char(size=1, copy=False, readonly=True)

    def apply_sequence(self, vals, sequence, alphabet):
        if len(alphabet) > 0:
            if alphabet.isalpha():
                sequence = "partner.index.{0}".format(alphabet)
            else:
                sequence = "partner.index.na"
        if vals.get('index', _('X-00000')) == _('X-00000') and len(sequence) > 0:
            vals['index'] = self.env['ir.sequence'].next_by_code(sequence) or ''
            vals['index_char'] = alphabet.upper()

        return vals

    @api.model
    def create(self, vals):
        sequence = alphabet = ""
        if vals.get('name'):
            alphabet = vals.get('name')[:1].lower()
        vals = self.apply_sequence(vals, sequence, alphabet)
        return super(Partner,self).create(vals)


    @api.multi
    def write(self, vals):
        sequence = alphabet = ""
        if vals.get('name'):
            alphabet = vals.get('name')[:1].lower()
        else:
            alphabet = self.name[:1].lower()
        if not self.index_char or self.index_char.lower() != alphabet:
            vals = self.apply_sequence(vals, sequence, alphabet)
        return super(Partner,self).write(vals)
