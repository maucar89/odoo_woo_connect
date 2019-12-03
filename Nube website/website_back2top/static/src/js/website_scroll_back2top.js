odoo.define('website_back2top.website_back2top', function(require) {
    "use strict";
    var base = require('web_editor.base');
    var amountScrolled = 300;

    if (!$('.oe_website_sale').length) {
        return $.Deferred().reject("DOM doesn't contain '.oe_website_sale'");
    }

    $('.oe_website_sale').each(function() {
        var oe_website_sale = this;

        $(oe_website_sale).append('<a href="#" class="back-to-top">Back to Top</a>');

        $(window).scroll(function() {
            if ($(window).scrollTop() > amountScrolled) {
                $(oe_website_sale).find('a.back-to-top').fadeIn('slow');
            } else {
                $(oe_website_sale).find('a.back-to-top').fadeOut('slow');
            }
        });

        $(oe_website_sale).on('click', 'a.back-to-top', function() {
            $('body, html').animate({
                scrollTop: 0
            }, 500);
            return false;
        });
    });
});
