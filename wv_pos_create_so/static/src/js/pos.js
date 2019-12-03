odoo.define('wv_pos_create_so.wv_pos_create_so', function (require) {
"use strict";

	var module = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var PosPopWidget = require('point_of_sale.popups');
    var core = require('web.core');
    var Model = require('web.DataModel');
    var QWeb = core.qweb;
    var _t = core._t;

    var _super_order = module.Order.prototype;
    module.Order = module.Order.extend({
        initialize: function() {
            _super_order.initialize.apply(this,arguments);
            this.wv_note = "";
            this.order_ref = "";
            this.save_to_db();
        },
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.wv_note = this.wv_note;
            return json;
        },
        export_for_printing:function() {
            var json = _super_order.export_for_printing.apply(this,arguments);
            json.wv_note = this.wv_note;
            json.order_ref = this.order_ref;
            return json
        },
        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this,arguments);
            this.wv_note = json.wv_note;
            this.order_ref = json.order_ref;
        },
    });

    var SaleOrderBillScreenWidget = screens.ReceiptScreenWidget.extend({
	    template: 'SaleOrderBillScreenWidget',
		    click_next: function(){
		    	var order = self.pos.get_order();
		    	order.finalize();
		        this.gui.show_screen('products');
		    },
		    click_back: function(){
		        this.gui.show_screen('products');
		    },
		    render_receipt: function(){
		        this._super();
		        this.$('.receipt-paymentlines').remove();
		        this.$('.receipt-change').remove();
		    },
		    print_web: function(){
		        window.print();
		    },
	});
	gui.define_screen({name:'saleOrderbill', widget: SaleOrderBillScreenWidget});


    var CreateSaleOrderPopupWidget = PosPopWidget.extend({
    template: 'CreateSaleOrderPopupWidget',
	    print_xml: function(){
	        var order = this.pos.get('selectedOrder');
	        if(order.get_orderlines().length > 0){
	            var receipt = order.export_for_printing();
	            receipt.bill = true;
	            this.pos.proxy.print_receipt(QWeb.render('SaleOrderBillReceipt',{
	                receipt: receipt, widget: this, pos: this.pos, order: order,
	            }));
	        }
	    },
        renderElement: function(){
            this._super(); 
            var self = this;
            $(".print_quotation_bill").click(function(){
                var order = self.pos.get('selectedOrder');
                if(order.get_client() != null){
	                order.wv_note = $(".wv_note").val();

	                if (!self.pos.config.iface_print_via_proxy) {
	                	self.save_order2();
	                } else {
	                    self.save_order();
	                    self.print_xml();
	                }
	                self.click_cancel();
	            }
	            else{
	            	alert("Customer is required for sale order. Please select customer first !!!!");
	            }
            }); 
            $(".save_quotation_bill").click(function(){
            	var order = self.pos.get('selectedOrder');
            	if(order.get_client() != null){
	            	order.wv_note = $(".wv_note").val();
	            	self.save_order();
	            }
	            else{
	            	alert("Customer is required for sale order. Please select customer first !!!!");
	            }
            });
        },
        save_order:function(){
        	self = this;
			var order = self.pos.get_order();
			var data = order.export_as_JSON();
	        new Model('sale.order').call('create_new_quotation',[data]).then(function(quotation_data){
		            order.finalize();
		            self.gui.show_popup('create-CompleteSaleOrder-popup',{'order_ref':quotation_data['result']});
		        },function(err,event){
		            event.preventDefault();
		            self.gui.show_popup('error',{
		                'title': _t('Error: Could not Save Changes'),
		                'body': _t('Your Internet connection is probably down.'),
		            });
		        });
        },
        save_order2:function(){
        	self = this;
			var order = self.pos.get_order();
			var data = order.export_as_JSON();
	        new Model('sale.order').call('create_new_quotation',[data]).then(function(quotation_data){
	        		order.order_ref = quotation_data['result'];
	                self.gui.show_screen('saleOrderbill');
		        },function(err,event){
		            event.preventDefault();
		            self.gui.show_popup('error',{
		                'title': _t('Error: Could not Save Changes'),
		                'body': _t('Your Internet connection is probably down.'),
		            });
		        });
        },
        show: function(options){
            this.options = options || {};
            var self = this;
            this._super(options); 
            this.renderElement();
        },
    });

    gui.define_popup({
        'name': 'create-saleorder-popup', 
        'widget': CreateSaleOrderPopupWidget,
    });

	var CreateCompleteSaleOrderPopupWidget = PosPopWidget.extend({
    	template: 'CreateCompleteSaleOrderPopupWidget',
        show: function(options){
            this.options = options || {};
            var self = this;
            this._super(options); 
            this.renderElement();
        },
    });

    gui.define_popup({
        'name': 'create-CompleteSaleOrder-popup', 
        'widget': CreateCompleteSaleOrderPopupWidget,
    });

    var CreateSaleOrderButton = screens.ActionButtonWidget.extend({
        template: 'CreateSaleOrderButton',
        button_click: function(){
        	if(this.pos.get_order().get_orderlines().length === 0){
        		alert("Please add some products!!!");
        	}
        	else{
    			this.gui.show_popup('create-saleorder-popup');
        	}
        },
    });

    screens.define_action_button({
        'name': 'Create Sale Order',
        'widget': CreateSaleOrderButton,
        'condition': function(){
            return this.pos.config.allow_create_sale_order;
        },
    });
    
});
