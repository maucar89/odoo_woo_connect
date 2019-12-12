odoo.define('website_customer_order_delivery_date.payment', function(require) {
    "use strict";

    var ajax = require('web.ajax');

    function payment(ev) {
        var $form = $(ev.currentTarget).parents('form');
        var acquirer_id = $(ev.currentTarget).parents('div.oe_sale_acquirer_button').first().data('id');
        if (!acquirer_id) {
            return false;
        }
        ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {}).then(function(data) {
            $form.html(data);
            $form.submit();
        });
    }

    function sleep(milliseconds) {
        var start = new Date().getTime();
        for (var i = 0; i < 1e7; i++) {
            if ((new Date().getTime() - start) > milliseconds) {
                break;
            }
        }
    }

    $(document).ready(function() {
        try {
            $("#delivery_date").datepicker({
                minDate: new Date()
            });
        } catch (e) {}

        var $payment = $("#payment_method");

        $("#payment_method button[type='submit']").bind("click", function(ev) {
            ev.preventDefault();
            ev.stopPropagation();

            var customer_order_delivery_date = $('#delivery_date').val();
            var customer_order_delivery_comment = $('#delivery_comment').val();
            ajax.jsonRpc('/shop/customer_order_delivery', 'call', {
                'delivery_date': customer_order_delivery_date,
                'delivery_comment': customer_order_delivery_comment
            }).done(function(res) {
                payment(ev);
            });
            sleep(1000);
        });
    });

});