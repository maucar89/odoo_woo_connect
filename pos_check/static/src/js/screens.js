odoo.define('pos_check.screens', function (require) {
"use strict";

var screens = require('point_of_sale.screens');

screens.PaymentScreenWidget.include({
    show_popup_check_info: function(options) {
        var self = this;
        window.document.body.removeEventListener('keypress', self.keyboard_handler);
        window.document.body.removeEventListener('keydown', self.keyboard_keydown_handler);
        this.gui.show_popup('check-info-input',{
            data: options.data,
            config_check: options.config_check,
            validate_info: function(infos){
                this.$('input').removeClass('error');
                this.$('select').removeClass('error');
                if(this.options.config_check.bank_required && !infos.check_bank_id) {
                    this.$('select[name=check_bank_id]').addClass('error');
                    this.$('select[name=check_bank_id]').focus();
                    return false;
                }
                if(this.options.config_check.bank_acc_required && !infos.check_bank_acc) {
                    this.$('input[name=check_bank_acc]').addClass('error');
                    this.$('input[name=check_bank_acc]').focus();
                    return false;
                }
                if(!infos.check_number) {
                    this.$('input[name=check_number]').addClass('error');
                    this.$('input[name=check_number]').focus();
                    return false;
                }
                if(this.options.config_check.owner_required && !infos.check_owner) {
                    this.$('input[name=check_owner]').addClass('error');
                    this.$('input[name=check_owner]').focus();
                    return false;
                }
                return true;
            },
            confirm: function(infos){
                options.confirm.call(self, infos);
                self.reset_input();
                self.render_paymentlines();
                window.document.body.addEventListener('keypress', self.keyboard_handler);
                window.document.body.addEventListener('keydown', self.keyboard_keydown_handler);
            },
            cancel: function(){
                window.document.body.addEventListener('keypress', self.keyboard_handler);
                window.document.body.addEventListener('keydown', self.keyboard_keydown_handler);
            },
        });
    },
    click_paymentmethods: function(id) {
        var self = this;
        var cashregister = null;
        for ( var i = 0; i < this.pos.cashregisters.length; i++ ) {
            if ( this.pos.cashregisters[i].journal_id[0] === id ){
                cashregister = this.pos.cashregisters[i];
                break;
            }
        }
        if (cashregister.journal.check_info_required) {
            this.show_popup_check_info({
                config_check: {
                    'bank_visible': cashregister.journal.check_bank_name_visible,
                    'bank_required': cashregister.journal.check_bank_name_required,
                    'bank_acc_visible': cashregister.journal.check_bank_acc_visible,
                    'bank_acc_required': cashregister.journal.check_bank_acc_required,
                    'owner_visible': cashregister.journal.check_owner_visible,
                    'owner_required': cashregister.journal.check_owner_required
                },
                data: {},
                confirm: function(infos) {
                    //merge infos to new paymentline
                    self.pos.get_order().add_paymentline_with_check(cashregister, infos);
                },
            });
        }
        else {
            this._super(id);
        }
    },

    click_numpad: function(button) {
        var paymentlines = this.pos.get_order().get_paymentlines();
        var open_paymentline = false;

        for (var i = 0; i < paymentlines.length; i++) {
            if (! paymentlines[i].paid) {
                open_paymentline = true;
            }
        }

        if (! open_paymentline) {
            var cashregister = null;
            for ( var i = 0; i < this.pos.cashregisters.length; i++ ) {
                if (!this.pos.cashregisters[i].journal.check_info_required){
                    cashregister = this.pos.cashregisters[i];
                    break;
                }
            }
            this.pos.get_order().add_paymentline(cashregister);
            this.render_paymentlines();
        }

        this.payment_input(button.data('action'));
    },

    click_check_info_paymentline: function(cid){
        var self = this;
        var lines = this.pos.get_order().get_paymentlines();
        for ( var i = 0; i < lines.length; i++ ) {
            if (lines[i].cid === cid) {
                var cashregister = lines[i].cashregister;
                this.show_popup_check_info({
                    config_check: {
                        'bank_visible': cashregister.journal.check_bank_name_visible,
                        'bank_required': cashregister.journal.check_bank_name_required,
                        'bank_acc_visible': cashregister.journal.check_bank_acc_visible,
                        'bank_acc_required': cashregister.journal.check_bank_acc_required,
                        'owner_visible': cashregister.journal.check_owner_visible,
                        'owner_required': cashregister.journal.check_owner_required
                    },
                    data: lines[i],
                    confirm: function(infos) {
                        //merge infos to updated paymentline
                        self.pos.get_order().update_paymentline_with_check(lines[i], infos);
                    },
                });
                return;
            }
        }
    },

    render_paymentlines: function() {
        var self = this;
        this._super();
        var lines = this.$('.paymentlines-container table.paymentlines');
        lines.on('click','.check-info-button', function(){
            self.click_check_info_paymentline($(this).data('cid'));
        });
    }

});

return screens;
});
