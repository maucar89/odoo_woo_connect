// -*- coding: utf-8 -*-
// © 2016 Pierre Faniel
// © 2016 Niboo SPRL (https://www.niboo.be/)
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

odoo.define('sale_customer_credit_limit.payment', function (require) {
    'use strict';

    var core = require('web.core');
    var payment = require('website_sale.payment');
    var ajax = require('web.ajax');

    var QWeb = core.qweb;

    var CustomerCreditLimit = core.Class.extend({
        init: function ($payment) {
            this.$payment = $payment;
            this.init_listeners();
        },
        init_listeners: function () {
            this.$payment.off("click", 'button[type="submit"], button[name="submit"]');
            this.$payment.on("click", 'button[type="submit"], button[name="submit"]', function (ev) {
                ev.preventDefault();
                ev.stopPropagation();
                var $form = $(ev.currentTarget).parents('form');
                var acquirer = $(ev.currentTarget).parents('div.oe_sale_acquirer_button').first();
                var acquirer_id = acquirer.data('id');
                var acquirer_token = acquirer.attr('data-token'); // !=data
                var params = {'tx_type': acquirer.find('input[name="odoo_save_token"]').is(':checked')?'form_save':'form'};
                if (! acquirer_id) {
                    return false;
                }
                if (acquirer_token) {
                    params.token = acquirer_token;
                }
                $form.off('submit');
                ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', params).then(function (data) {
                    if(data.error){
                        var $modal = $(QWeb.render('sale_customer_credit_limit.modal_error', data.data));
                        $('body').append($modal);
                        $modal.modal('show');
                    } else {
                        // Submit the form from the payment acquirer
                        $(data).appendTo('body').submit();
                    }
                });
                return false;
            });
        },
    });


    // Overwrite existing function to check for credit limit on click
    QWeb.add_template('/sale_customer_credit_limit/static/src/xml/website_sale.xml', function () {
        $(document).ready(function () {
            var $payment = $("#payment_method");
            if (!$($payment.length)) {
                return $.Deferred().reject("DOM doesn't contain '#payment_method'");
            } else {
                new CustomerCreditLimit($payment);
            }
        });
    });
});
