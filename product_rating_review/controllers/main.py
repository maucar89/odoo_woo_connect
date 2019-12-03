# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_mail.controllers.main import WebsiteMail


class WebsiteMail(WebsiteMail):

    @http.route(['/website_mail/post/json'], type='json', auth='public', website=True)
    def chatter_json(self, res_model='', res_id=None, message='', **kw):
        """get reviews from website products"""
        params = kw.copy()
        msg_data = super(WebsiteMail, self).chatter_json(
            res_model=res_model, res_id=res_id, message=message, **params)
        res_user = request.env['res.users'].search(
            [('name', '=', msg_data.get('author'))])
        product = request.env['product.template'].browse(res_id)
        rating = float(kw.get('rating')) if kw.get('rating') else 0
        # store data from website at product backend
        request.env['customer.review'].sudo().create({
            'customer_id': res_user.id,
            'name': message,
            'date': msg_data.get('date'),
            'email': res_user.partner_id.email,
            'product_id': product.id,
            'rating': rating,
        })
        return msg_data
