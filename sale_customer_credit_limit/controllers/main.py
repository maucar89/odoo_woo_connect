# -*- coding: utf-8 -*-
# © 2016 Tobias Zehntner
# © 2016 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import http, _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSaleInherit(WebsiteSale):

    @http.route(['/shop/payment/transaction/<int:acquirer_id>'], type='json',
                auth='public', website=True)
    def payment_transaction(self, acquirer_id, tx_type='form', token=None, **kwargs):

        order = request.website.sale_get_order()
        credit_limit = order.partner_id.credit_limit
        open_credit = order.partner_id.credit
        order_amount = order.amount_total
        wire_transfer_id = request.env.ref('payment.payment_acquirer_transfer')
        exceeded_credit = (open_credit + order_amount) - credit_limit

        if acquirer_id == wire_transfer_id.id \
                and exceeded_credit > 0:
            currency_symbol = order.currency_id.symbol

            return {'error': True,
                    'data': {
                        'window_title': _(
                            'Please choose another payment option'),
                        'credit_limit': '%.2f' % credit_limit,
                        'open_credit': '%.2f' % open_credit,
                        'order_amount': '%.2f' % order_amount,
                        'exceeded_credit': '%.2f' % exceeded_credit,
                        'currency_symbol': currency_symbol,
                        },
                    }

        return super(WebsiteSaleInherit, self).payment_transaction(
                    acquirer_id, tx_type, token, **kwargs)
