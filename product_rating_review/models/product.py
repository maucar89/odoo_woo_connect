# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _count_avg_rating(self):
        #  count average product rating
        reviews = self.rating_get_stats()
        self.review_count = "%.1f" % reviews.get('avg')

    @api.multi
    def action_view_reviews(self):
        self.ensure_one()
        action = self.env.ref('product_rating_review.action_product_reviewer_list')

        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'res_model': action.res_model,
            'domain': [('product_id', '=', self.id)]
        }

    reviewer_line_ids = fields.One2many(
        'customer.review', 'product_id', string="Customer Reviews")
    review_count = fields.Float(
        compute='_count_avg_rating', string='Average Rating')


class CustomerReview(models.Model):
    _name = "customer.review"

    product_id = fields.Many2one('product.template', required=True)
    customer_id = fields.Many2one('res.users', string='Review By', required=True)
    name = fields.Text(string='Comment', required=True)
    rating = fields.Integer(string='Rating')
    date = fields.Datetime(string='Created On')
    email = fields.Char(string='Email', required=True)
