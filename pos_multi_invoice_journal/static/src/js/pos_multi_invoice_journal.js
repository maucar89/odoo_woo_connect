odoo.define('pos_multi_invoice_journal', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var qweb = core.qweb;

    screens.PaymentScreenWidget.include({

        click_invoice_journal: function (journal_id) {
            var order = this.pos.get_order();
            order['invoice_journal_id'] = journal_id;
            $('.journal').removeClass('highlight');
            $('.journal').addClass('lowlight');
            var $journal_selected = $("[data-id='" + journal_id + "']");
            $journal_selected.addClass('highlight');
        },
        render_invoice_journals: function () {
            var self = this;
            var methods = $(qweb.render('journal_list', {widget: this}));
            methods.on('click', '.journal', function () {
                self.click_invoice_journal($(this).data('id'));
            });
            return methods;
        },

        renderElement: function () {
            this._super();
            if (this.pos.config.invoice_journal_ids && this.pos.config.invoice_journal_ids.length > 0 && this.pos.journals) {
                var methods = this.render_invoice_journals();
                methods.appendTo(this.$('.invoice_journals'));
            }
        }
    })

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.invoice_journal_id) {
                this.invoice_journal_id = json.invoice_journal_id;
            }
            return res;
        },
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            if (this.invoice_journal_id) {
                json.invoice_journal_id = this.invoice_journal_id;
            }
            return json;
        }
    })

    models.load_models([
         {
            model: 'account.journal',
            fields: [],
            domain: function (self) {
                return [['id', 'in', self.config.invoice_journal_ids]]
            },
            loaded: function (self, journals) {
                self.journals = journals;
                self.journal_by_id = {};
                for (var i = 0; i < journals.length; i++) {
                    self.journal_by_id[journals[i]['id']] = journals[i];
                }
            }
        }
    ])

});
