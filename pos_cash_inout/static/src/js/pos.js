odoo.define('pos_cash_inout.pos_cash_inout', function(require) {
	"use strict";

	var gui = require('point_of_sale.gui');
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var PopupWidget = require('point_of_sale.popups');
	var Model = require('web.DataModel');
	var QWeb = core.qweb;

	var PutMoneyIn = screens.ActionButtonWidget.extend({
		template : 'PutMoneyIn',
		button_click : function() {
			self = this;
			var msg_show_put_money_in = "";
			msg_show_put_money_in += "<div class='container'>" +
										"<div class='sub-container'>" +
											"<table id='tbl_id'>" +
												"<tr>" +
													"<td>Reason</td>" +
													"<td id='td_id'><input id='txt_reason_in_id' type='text' name='txt_reason_in'></td>" +
												"</tr>" +
												"<tr>" +
													"<td>Amount</td>" +
													"<td id='td_id'><input id='txt_amount__in_id' type='text' name='txt_amount_in'></td>" +
												"<tr>" +
											"</table>" +
										"</div>" +
									"</div>"; 
			self.gui.show_popup('put_money_in',{msg_show_put_money_in:msg_show_put_money_in});
		},
	});
	screens.define_action_button({
		'name' : 'putmoneyin',
		'widget' : PutMoneyIn,
	});

	var PutMoneyInPopup = PopupWidget.extend({
	    template: 'PutMoneyInPopup',
	    show: function(options){
	    	this.msg_show_put_money_in = options.msg_show_put_money_in || "";
	    	options = options || {};
	        this._super(options);

	        this.renderElement();
	    },
	    click_confirm: function(){
	    	var self = this;
	    	var name = '';
	    	var amount ='';
	    	name = $('#txt_reason_in_id').val();
	    	amount = $('#txt_amount__in_id').val();
	    	if(name =='' || amount == ''){
	    		alert("Please fill all fields.");
	    	}else if(!$.isNumeric(amount)){
	    		alert("Please input valid amount");
	    		$('#txt_amount__in_id').val('');
	    		$('#txt_amount__in_id').focus();
	    	}else{
	    		var session_id = '';
	    		session_id = posmodel.pos_session.id;
	    		new Model('pos.session').call('put_money_in', [name,amount,session_id]).then(
						function(result) {
							if (result['error']) {
								alert(result['error']);
							}else if (self.pos.config.iface_cashdrawer) {
					            self.pos.proxy.open_cashbox();
							}
						}).fail(function(error, event) {
					if (error.code === -32098) {
						alert("Server closed...");
						event.preventDefault();
					}
				});
	    		this.gui.close_popup();
	    	}
	    },
	    renderElement: function() {
            var self = this;
            this._super();
    	},
	});
	gui.define_popup({name:'put_money_in', widget: PutMoneyInPopup});

	var TakeMoneyOut = screens.ActionButtonWidget.extend({
		template : 'TakeMoneyOut',
		button_click : function() {
			self = this;
			var msg_show_take_money_out = "<div class='container'>" +
										"<div class='sub-container'>" +
											"<table id='tbl_id'>" +
												"<tr>" +
													"<td>Reason</td>" +
													"<td id='td_id'><input id='txt_reason_out_id' type='text' name='txt_reason_in'></td>" +
												"</tr>" +
												"<tr>" +
													"<td>Amount</td>" +
													"<td id='td_id'><input id='txt_amount__out_id' type='text' name='txt_amount_in'></td>" +
												"<tr>" +
											"</table>" +
										"</div>" +
									"</div>"; 
			self.gui.show_popup('take_money_out',{msg_show_take_money_out:msg_show_take_money_out});
		},
	});
	screens.define_action_button({
		'name' : 'takemoneyout',
		'widget' : TakeMoneyOut,
	});

	var TakeMoneyOutPopup = PopupWidget.extend({
	    template: 'TakeMoneyOutPopup',
	    show: function(options){
	    	this.msg_show_take_money_out = options.msg_show_take_money_out || "";
	        options = options || {};
	        this._super(options);

	        this.renderElement();
	    },
	    click_confirm: function(){
	    	var self = this;
	    	var name = '';
	    	var amount ='';
	    	name = $('#txt_reason_out_id').val();
	    	amount = $('#txt_amount__out_id').val();
	    	if(name =='' || amount == ''){
	    		alert("Please fill all fields.");
	    	}else if(!$.isNumeric(amount)){
	    		alert("Please input valid amount");
	    		$('#txt_amount__out_id').val('');
	    		$('#txt_amount__out_id').focus();
	    	}else{
	    		var session_id = '';
	    		session_id = posmodel.pos_session.id;
	    		new Model('pos.session').call('take_money_out', [name,amount,session_id]).then(
						function(result) {
							if (result['error']) {
								alert(result['error']);
							}else if (self.pos.config.iface_cashdrawer) {
					            self.pos.proxy.open_cashbox();
							}
						}).fail(function(error, event) {
					if (error.code === -32098) {
						alert("Server closed...");
						event.preventDefault();
					}
				});
	    		this.gui.close_popup();
	    	}
	    },
	    renderElement: function() {
            var self = this;
            this._super();
    	},
	});
	gui.define_popup({name:'take_money_out', widget: TakeMoneyOutPopup});

});
