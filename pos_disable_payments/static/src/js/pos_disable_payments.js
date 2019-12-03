// pos_disable_payments js
odoo.define('pos_disable_payments.pos_disable_payments', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    var Model = require('web.DataModel');
    var QWeb = core.qweb;
    var session = require('web.session');

    var _t = core._t;


    var is_allow_payments;
    var is_allow_discount;
    var is_allow_qty;
    var is_edit_price;
    var is_allow_remove_orderline;
    
    
    screens.ScreenWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            var cashier = this.pos.user;
            var cash = this.pos.get_cashier();
            var id = cash['id'];

            (new Model('pos.order')).call('get_cashier_value', [id]).fail(function(unused, event) {}).done(function(output) {

                is_allow_payments = output[0];
                is_allow_qty = output[1];
                is_allow_discount = output[2];
                is_edit_price = output[3];
                is_allow_remove_orderline = output[4];

                if (output[0] == true) {
                    $('.button.pay').show();
                }
                else{
                    $('.button.pay').hide();
                }
                if (output[1] == true) {
                    $('.mode-button.qty.selected-mode').show();
                }
                else{
                    $('.mode-button.qty.selected-mode').hide();
                }
                if (output[2] == true) {
                    $('.mode-button.disc').show();
                }
                else{
                    $('.mode-button.disc').hide();
                }
                if (output[3] == true) {
                    $('.mode-button.price').show();
                }
                else{
                    $('.mode-button.price').hide();
                }
                if (output[4] == true) {
                    $('.input-button.numpad-backspace').show();
                }
                else{
                    $('.input-button.numpad-backspace').hide();
                }

                });
            
        },
    });


    gui.Gui.include({

            select_user: function(options){
                options = options || {};
                var self = this;
                var def  = new $.Deferred();

                var list = [];
                for (var i = 0; i < this.pos.users.length; i++) {
                    var user = this.pos.users[i];
                    if (!options.only_managers || user.role === 'manager') {
                        list.push({
                            'label': user.name,
                            'item':  user,
                        });
                    }
                }

                this.show_popup('selection',{
                    'title': options.title || _t('Select User'),
                    list: list,
                    confirm: function(user){ def.resolve(user); },
                    cancel:  function(){ def.reject(); },
                });

                return def.then(function(user){
                    if (options.security && user !== options.current_user && user.pos_security_pin) {
                        return self.ask_password(user.pos_security_pin).then(function(){
                            return user;
                        });
                    } else {
                        location.reload();
                        return user;
                    }
                });
            },

            // Ask for a password, and checks if it this
            // the same as specified by the function call.
            // returns a deferred that resolves on success,
            // fails on failure.
            ask_password: function(password) {
                var self = this;
                var ret = new $.Deferred();
                if (password) {
                    this.show_popup('password',{
                        'title': _t('Password ?'),
                        confirm: function(pw) {
                            if (pw !== password) {
                                self.show_popup('error',_t('Incorrect Password'));
                                ret.reject();
                            } else {
                                ret.resolve();
                                location.reload();
                            }
                        },
                    });
                } else {
                    ret.resolve();
                }
                return ret;
            },
    });
});

