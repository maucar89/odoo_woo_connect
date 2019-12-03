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
from odoo import fields, models, api


class LoyaltyConfiguration(models.Model):
    _name = 'loyalty.config.settings'

    @api.model
    def _get_classified_fields(self):
       """ return a dictionary with the fields classified by category::

               {   'default': [('default_foo', 'model', 'foo'), ...],
                   'group':   [('group_bar', [browse_group], browse_implied_group), ...],
                   'module':  [('module_baz', browse_module), ...],
                   'other':   ['other_field', ...],
               }
       """
       IrModule = self.env['ir.module.module']
       ref = self.env.ref

       defaults, groups, modules, others = [], [], [], []
       for name, field in self._fields.iteritems():
           if name.startswith('default_') and hasattr(field, 'default_model'):
               defaults.append((name, field.default_model, name[8:]))
           elif name.startswith('group_') and field.type in ('boolean', 'selection') and \
                   hasattr(field, 'implied_group'):
               field_group_xmlids = getattr(field, 'group', 'base.group_user').split(',')
               field_groups = reduce(add, map(ref, field_group_xmlids))
               groups.append((name, field_groups, ref(field.implied_group)))
           elif name.startswith('module_') and field.type in ('boolean', 'selection'):
               module = IrModule.sudo().search([('name', '=', name[7:])], limit=1)
               modules.append((name, module))
           else:
               others.append(name)
       return {'default': defaults, 'group': groups, 'module': modules, 'other': others}

    
    @api.multi
    def execute(self):
       self.ensure_one()
       if not self.env.user._is_superuser() and not self.env.user.has_group('base.group_system'):
           raise AccessError(_("Only administrators can change the settings"))

       self = self.with_context(active_test=False)
       classified = self._get_classified_fields()

       # default values fields
       IrValues = self.env['ir.values'].sudo()
       for name, model, field in classified['default']:
           IrValues.set_default(model, field, self[name])

       # group fields: modify group / implied groups
       for name, groups, implied_group in classified['group']:
           if self[name]:
               groups.write({'implied_ids': [(4, implied_group.id)]})
           else:
               groups.write({'implied_ids': [(3, implied_group.id)]})
               implied_group.write({'users': [(3, user.id) for user in groups.mapped('users')]})

       # other fields: execute all methods that start with 'set_'
       for method in dir(self):
           if method.startswith('set_'):
               getattr(self, method)()

       # module fields: install/uninstall the selected modules
       to_install = []
       to_uninstall_modules = self.env['ir.module.module']
       lm = len('module_')
       config = self.env['res.config'].next() or {}
       if config.get('type') not in ('ir.actions.act_window_close',):
           return config

       # force client-side reload (update user menu and current view)
       return {
           'type': 'ir.actions.client',
           'tag': 'reload',
       }
    
    @api.model
    def default_get(self,fields):
       obj = self.search([])
       res = super(LoyaltyConfiguration, self).default_get(fields)
       if obj:
           dc = obj.read()[0]
           del dc["write_uid"],dc["id"],dc["__last_update"],dc["create_date"]
           res.update(dc)
       return res

    @api.model
    def create(self, vals):
        obj = self.search([])
        if obj:
            obj[0].write(vals)
        return super(LoyaltyConfiguration,self).create(vals)

    points_based_on = fields.Selection([
        ('product', "Product"),
        ('order', "Order")
    ], string="Points Based On",
        help='Loyalty points calculation can be based on products or order')
    minimum_purchase = fields.Float("Minimum Purchase")
    point_calculation = fields.Float("Point Calculation (%)")
    points = fields.Integer("Points")
    to_amount = fields.Float("To Amount")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: