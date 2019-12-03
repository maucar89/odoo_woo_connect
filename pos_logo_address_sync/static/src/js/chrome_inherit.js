odoo.define('pos_logo_address_sync.logo', function (require) {
    "use strict";

    var PosBaseWidget = require('point_of_sale.chrome');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var QWeb = core.qweb;    

    PosBaseWidget.Chrome.include({    
        renderElement: function(){
            var self = this;
            if(self.pos.config){
                if(self.pos.config.logo){
                    this.logo = "data:image/png;base64," + self.pos.config.logo;
                }
            }
            this._super(this);
        },        
    });


    screens.ReceiptScreenWidget.include({
        render_receipt: function () {
            this._super(this);
            var order = this.pos.get_order()
            this.$('.pos-receipt-container').html(QWeb.render('PosTicket',{
                    widget:this,                    
                    order: order,
                    receipt: order.export_for_printing(),
                    orderlines: order.get_orderlines(),
                    paymentlines: order.get_paymentlines(),
                    logo_r : "data:image/png;base64," + this.pos.config.logo,
            }));
        },
    });


});