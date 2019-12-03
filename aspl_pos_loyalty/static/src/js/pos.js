odoo.define('aspl_pos_loyalty.pos', function (require) {
"use strict";

	var gui = require('point_of_sale.gui');
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var PopupWidget = require('point_of_sale.popups');
	var Model = require('web.DataModel');
	var core = require('web.core');
	var DB = require('point_of_sale.DB');
	var utils = require('web.utils');

	var QWeb = core.qweb;
	var _t = core._t;
	var round_di = utils.round_decimals;
	var round_pr = utils.round_precision;

	models.load_fields("res.partner", ['remaining_loyalty_points', 'remaining_loyalty_amount', 'loyalty_points_earned', 'total_remaining_points']);
	models.load_fields("product.product", ['loyalty_point']);
	models.load_fields("pos.category", ['loyalty_point']);

    screens.PaymentScreenWidget.include({
    	renderElement: function() {
    		var self = this;
    		this._super()
    		
    		this.$('.js_redeem_loyalty').click(function(){
    			var order = self.pos.get_order();
    			if(order.get_client()){
    				if(order.get_client().total_remaining_points > 0){
    					self.click_redeem_loyalty();
    				} else {
    					self.gui.show_popup('error',{
    						title: _t("Loyalty Points"),
    						body: _t(order.get_client().name + " have 0 points to redeem."),
    					})
    				}
    			}
            });
    	},
    	click_redeem_loyalty: function(){
    		var order = this.pos.get_order();
    		if(order.get_client()){
    			this.gui.show_popup("redeem_loyalty_points", {payment_self: this});
    		}
    	},
    	payment_input: function(input) {
    		var self = this;
    		var order = this.pos.get_order();
    		if(order.selected_paymentline.get_freeze_line()){
    			return
    		}
    		this._super(input);
    	},
    });

    var RedeemLoyaltyPointsPopup = PopupWidget.extend({
	    template: 'RedeemLoyaltyPointsPopup',
	    show: function(options){
	    	var self = this;
	    	this.payment_self = options.payment_self;
	    	this._super(options);
	    	var order = self.pos.get_order();
	    	var fields = _.find(this.pos.models,function(model){ return model.model === 'res.partner'; }).fields;
	    	new Model('res.partner').call('search_read', [[['id', '=', order.get_client().id]], fields], {}, {async: false})
	    	.then(function(partner){
	    		if(partner.length > 0){
	    			var exist_partner = self.pos.db.get_partner_by_id(order.get_client().id);
	    			_.extend(exist_partner, partner[0]);
	    		}
	    	});
	    	window.document.body.removeEventListener('keypress',this.payment_self.keyboard_handler);
	    	window.document.body.removeEventListener('keydown',this.payment_self.keyboard_keydown_handler);
	    	self.renderElement();
	    	$('.redeem_loyalty_input').focus();
	    },
	    click_confirm: function(){
	    	var self =this;
	    	var order = this.pos.get_order();
	    	var redeem_point_input = $('.redeem_loyalty_input');
	    	if(redeem_point_input.val() && $.isNumeric(redeem_point_input.val()) 
	    			&& Number(redeem_point_input.val()) > 0){
	    		var remaining_loyalty_points = order.get_client().remaining_loyalty_points - order.get_loyalty_redeemed_point();
	    		if(Number(redeem_point_input.val()) <= remaining_loyalty_points){
	    			var amount_to_redeem = (Number(redeem_point_input.val()) * self.pos.loyalty_config.to_amount) / self.pos.loyalty_config.points;
	    			if(amount_to_redeem <= (order.get_due() || order.get_total_with_tax())){
			    		if(self.pos.config.loyalty_journal_id){
				    		var loyalty_cashregister = _.find(self.pos.cashregisters, function(cashregister){
				    			return cashregister.journal_id[0] === self.pos.config.loyalty_journal_id[0] ? cashregister : false;
				    		});
				    		if(loyalty_cashregister){
				    			order.add_paymentline(loyalty_cashregister);
				    			order.selected_paymentline.set_amount(amount_to_redeem);
				    			order.selected_paymentline.set_loyalty_point(Number(redeem_point_input.val()));
				    			order.selected_paymentline.set_freeze_line(true);
				    			self.payment_self.reset_input();
				    			self.payment_self.render_paymentlines();
				    			order.set_loyalty_redeemed_point(Number(order.get_loyalty_redeemed_point()) + Number(redeem_point_input.val()));
				    			order.set_loyalty_redeemed_amount(order.get_loyalty_amount_by_point(order.get_loyalty_redeemed_point()));
				    			this.gui.close_popup();
				    		}
			    		} else {
			    			alert(_t("Please configure Journal for Loyalty in Point of sale configuration."));
			    		}
	    			} else {
	    				alert(_t("Can not redeem more than order due."));
	    			}
	    		} else {
	    			alert(_t("Input must be <= "+ remaining_loyalty_points));
	    		}
	    	} else {
	    		alert(_t("Invalid Input"));
	    	}
	    	
	    },
	    renderElement: function(){
	    	var self = this;
	    	this._super();
	    	var order = self.pos.get_order();
	    	if(self.el.querySelector('.redeem_loyalty_input')){
		    	self.el.querySelector('.redeem_loyalty_input').addEventListener('keyup', function(e){
		    		if($.isNumeric($(this).val())){
		    			var remaining_loyalty_points = order.get_client().remaining_loyalty_points - order.get_loyalty_redeemed_point();
		    			var amount = order.get_loyalty_amount_by_point(Number($(this).val()));
		    			$('.point_to_amount').text(self.format_currency(amount));
		    			if(Number($(this).val()) > remaining_loyalty_points){
		    				alert("Can not redeem more than your remaining points");
		    				$(this).val(0);
		    				$('.point_to_amount').text('0.00');
		    			}
		    			if(amount > (order.get_due() || order.get_total_with_tax())){
		    				alert("Loyalty Amount exceeding Due Amount");
		    				$(this).val(0);
		    				$('.point_to_amount').text('0.00');
		    			}
		    		} else {
		    			$('.point_to_amount').text('0.00');
		    		}
		    	});
	    	}
	    	
	    },
//	    get_loyalty_amount_by_point: function(point){
//	    	return (point * this.pos.loyalty_config.to_amount) / this.pos.loyalty_config.points;
//	    },
	    close: function(){
	    	window.document.body.addEventListener('keypress',this.payment_self.keyboard_handler);
	    	window.document.body.addEventListener('keydown',this.payment_self.keyboard_keydown_handler);
	    },
    });
    gui.define_popup({name:'redeem_loyalty_points', widget: RedeemLoyaltyPointsPopup});

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
    	initialize: function(attributes,options){
        	_super_Order.initialize.apply(this, arguments);
        	this.set({
        		loyalty_redeemed_point: 0.00,
        		loyalty_earned_point: 0.00,
        	})
    	},
    	set_loyalty_redeemed_point: function(val){
    		this.set('loyalty_redeemed_point', Number(val).toFixed(2));
    	},
    	get_loyalty_redeemed_point: function(){
    		return this.get('loyalty_redeemed_point') || 0.00;
    	},
    	set_loyalty_redeemed_amount: function(val){
    		this.set('loyalty_redeemed_amount', val);
    	},
    	get_loyalty_redeemed_amount: function(){
    		return this.get('loyalty_redeemed_amount') || 0.00;
    	},
    	set_loyalty_earned_point: function(val){
    		this.set('loyalty_earned_point', val);
    	},
    	get_loyalty_earned_point: function(){
    		return this.get('loyalty_earned_point') || 0.00;
    	},
    	set_loyalty_earned_amount: function(val){
    		this.set('loyalty_earned_amount', val);
    	},
    	get_loyalty_earned_amount: function(){
    		return this.get('loyalty_earned_amount') || 0.00;
    	},
    	export_as_JSON: function() {
            var self = this;
        	var new_val = {};
            var orders = _super_Order.export_as_JSON.call(this);
            new_val = {
            	loyalty_redeemed_point: this.get_loyalty_redeemed_point() || false,
            	loyalty_redeemed_amount: this.get_loyalty_redeemed_amount() || false,
            	loyalty_earned_point: this.get_loyalty_earned_point() || false,
            	loyalty_earned_amount: this.get_loyalty_earned_amount() || false,
            }
            $.extend(orders, new_val);
            return orders;
    	},
    	remove_paymentline: function(line){
    		this.set_loyalty_redeemed_point(this.get_loyalty_redeemed_point() - line.get_loyalty_point());
    		this.set_loyalty_redeemed_amount(this.get_loyalty_amount_by_point(this.get_loyalty_redeemed_point()));
    		_super_Order.remove_paymentline.apply(this, arguments);
    	},
    	get_total_loyalty_points: function(){
    		var temp = 0.00
    		if(this.get_client()){
	    		temp = Number(this.get_client().total_remaining_points) 
	    				+ Number(this.get_loyalty_earned_point()) 
	    				- Number(this.get_loyalty_redeemed_point())
    		}
    		return temp.toFixed(2)
    	},
    	export_for_printing: function(){
    		var self = this;
    		var orders = _super_Order.export_for_printing.call(this);
    		var new_val = {
    			total_points: this.get_total_loyalty_points() || false,
    			earned_points: this.get_loyalty_earned_point() || false,
    			redeem_points: this.get_loyalty_redeemed_point() || false,
    			client_points: this.get_client() ? this.get_client().total_remaining_points.toFixed(2) : false,
    		};
    		$.extend(orders, new_val);
            return orders;
    	},
    	get_loyalty_amount_by_point: function(point){
	    	return (point * this.pos.loyalty_config.to_amount) / this.pos.loyalty_config.points;
	    },
    });

    var _super_paymentline = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
       initialize: function(attributes, options) {
           var self = this;
           _super_paymentline.initialize.apply(this, arguments);
           this.set({
        		   loyalty_point: 0,
        		   loyalty_amount: 0.00,
           });
        },
        set_loyalty_point: function(points){
        	this.set('loyalty_point', points)
        },
        get_loyalty_point: function(){
        	return this.get('loyalty_point')
        },
        set_loyalty_amount: function(amount){
        	this.set('loyalty_amount', amount)
        },
        get_loyalty_amount: function(){
        	return this.get('loyalty_amount')
        },
        set_freeze_line: function(freeze_line){
        	this.set('freeze_line', freeze_line)
        },
        get_freeze_line: function(){
        	return this.get('freeze_line')
        },
    });

    var _super_posmodel = models.PosModel;
	models.PosModel = models.PosModel.extend({
		load_server_data: function(){
			var self = this;
			var loaded = _super_posmodel.prototype.load_server_data.call(this);
			loaded.then(function(){
				var limit = 1, sort = 'id desc', domain = [], fields = [], offset;
		    	new Model('loyalty.config.settings').call("search_read", 
		    			[domain=domain, fields=fields, offset=0, limit=limit, sort=sort], {}, {async: false})
		    	.then(function(loyalty_config){
		    		if(loyalty_config && loyalty_config[0]){
		    			self.loyalty_config = loyalty_config[0];
		    		}
		    	})
			})
			return loaded
		},
	 });

	screens.OrderWidget.include({
		update_summary: function(){
			var self = this;
			this._super();
	        var order = this.pos.get_order();
	        if (!order.get_orderlines().length) {
	            return;
	        }
	        if(order.get_client()){
		        if(this.pos.loyalty_config && this.pos.loyalty_config.points_based_on == 'product'){
		        	var total_points = this.get_points_from_product();
		        	if(this.el.querySelector('.loyalty_info_cart .value')){
		        		this.el.querySelector('.loyalty_info_cart .value').textContent = total_points;
		        	}
		        	order.set_loyalty_earned_point(total_points);
		        	order.set_loyalty_earned_amount(order.get_loyalty_amount_by_point(total_points));
		        } else if(this.pos.loyalty_config && this.pos.loyalty_config.points_based_on == 'order') {
		        	if(order.get_total_with_tax() >=  this.pos.loyalty_config.minimum_purchase 
		        			&& this.pos.loyalty_config.point_calculation > 0){
		        		var total_points = this._calculate_loyalty_by_order();
		        		if(total_points > 0){
		        			if(this.el.querySelector('.loyalty_info_cart .value')){
				        		this.el.querySelector('.loyalty_info_cart .value').textContent = total_points.toFixed(2);
				        	}
		        			order.set_loyalty_earned_point(total_points.toFixed(2));
		        			order.set_loyalty_earned_amount(order.get_loyalty_amount_by_point(total_points));
		        		}
		        	} else if(order.get_total_with_tax() <  this.pos.loyalty_config.minimum_purchase){
		        		order.set_loyalty_earned_point(0.00);
		        	}
		        }
	        }
		},
		_calculate_loyalty_by_order: function(){
			var order = this.pos.get_order();
			return (order.get_total_with_tax() * this.pos.loyalty_config.point_calculation) / 100
		},
		get_points_from_product: function(){
			var self = this;
			var order = this.pos.get_order();
			var currentOrderline = order.get_orderlines()
			var total_points = 0.00
			_.each(currentOrderline, function(line){
				var line_points = 0.00;
				if(line.get_product().loyalty_point){
					line_points = line.get_product().loyalty_point * line.get_quantity();;
					total_points += line_points;
				} else if(line.get_product().pos_categ_id){
					var cat_point = self._get_points_from_categ(line.get_product().pos_categ_id[0]);
					if (cat_point){
						line_points = cat_point * line.get_quantity();
						total_points += line_points;
					}
				}
//				line.set_line_loyalty_point(line_points);
//				line.set_line_loyalty_amount(self.get_loyalty_amount_by_point(line_points));
			});
			return total_points;
		},
		_get_points_from_categ: function(categ_id){
			var category = this.pos.db.get_category_by_id(categ_id);
			if(category && category.loyalty_point){
				return category.loyalty_point;
			} else if(category.parent_id){
				this._get_points_from_categ(category.parent_id[0]);
			}
			return false;
		},
//		get_loyalty_amount_by_point: function(point){
//	    	return (point * this.pos.loyalty_config.to_amount) / this.pos.loyalty_config.points;
//	    },
	});

	DB.include({
		add_partners: function(partners){
			var self = this;
			for(var i = 0, len = partners.length; i < len; i++){
	            var partner = partners[i];
	            var old_partner = this.partner_by_id[partner.id];
	            if(partners && old_partner && partner.total_remaining_points !== old_partner.total_remaining_points){
	            	old_partner['total_remaining_points'] = partner.total_remaining_points;
	            }
			}
			return this._super(partners);
		},
	});
});