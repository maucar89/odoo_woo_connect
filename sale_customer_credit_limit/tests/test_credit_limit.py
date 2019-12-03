# -*- coding: utf-8 -*-
# © 2017 Tobias Zehntner
# © 2017 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
import random
import string

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import exceptions
from odoo.tests.common import TransactionCase

USE_EXISTING_RECS = True
_logger = logging.getLogger(__name__)


class TestCreditLimit(TransactionCase):
    def setUp(self):
        super(TestCreditLimit, self).setUp()

        self.admin = self.env.user
        self.company = self.admin.company_id

        # Make sure employee is no Sales manager
        self.employee = self.get_employee(self.company, None)
        self.employee.user_id.write({'groups_id': [
            (3, self.ref('sales_team.group_sale_manager'))]})
        self.employee.user_id.write({'groups_id': [
            (4, self.ref('sales_team.group_sale_salesman'))]})

        self.manager = self.get_manager(self.employee)
        self.customer = self.get_credit_free_customer(
            [self.employee.user_id.partner_id.id,
             self.manager.user_id.partner_id.id])
        self.product = self.get_product()
        self.sale_order = self.create_sale_order(self.company.currency_id)

        # In the setup, the customer should have no credit
        self.assertEqual(self.customer.credit, 0,
                         'Customer: %s' % self.customer)

    def tearDown(self):
        if USE_EXISTING_RECS:
            # If test used random existing data, give more info
            data = {'Employee': self.employee,
                    'Company': self.company,
                    'Manager': self.manager,
                    'Customer': self.customer,
                    'Product': self.product}
            _logger.info('Data that was used for this test: %s' % data)

    ### TESTS ###
    def test_default_credit_limit(self):
        """
        Test Credit Limit: Check if default credit limit is set
        """
        amount = 300
        settings = self.env['sale.config.settings'].search([], limit=1)
        settings.default_credit_limit = amount
        new_partner = self.create_partner()
        self.assertEqual(new_partner.credit_limit, amount)

    def test_no_credit(self):
        """
        Test Credit Limit: Customer has no credit -> SO should be confirmed
        """
        # SO should be confirmed
        self.sale_order.sudo(self.employee.user_id.id).action_confirm()
        self.assertEqual(self.sale_order.state, 'sale',
                         'Employee: %s' % self.employee)

    def test_no_overdue_credit(self):
        """
        Test Credit Limit: Customer has no overdue credit -> SO should be confirmed
        """
        amount = 300
        self.customer.credit_limit = 200
        currency = self.company.currency_id
        normal_invoice = self.create_invoice(self.product,
                                             self.customer,
                                             currency, amount)
        # Credit limit should be set
        self.assertEqual(self.customer.credit_limit, 200)
        # Customer should have credit
        self.assertEqual(self.customer.credit, amount)

        # Since credit is not overdue, SO should be confirmed
        self.sale_order.sudo(self.employee.user_id.id).action_confirm()
        self.assertEqual(self.sale_order.state, 'sale',
                         'Employee: %s' % self.employee)

    def test_overdue_by_no_payment_term_defined(self):
        """
        Test Credit Limit: No payment terms on invoice -> overdue immediate
        """
        amount = 300
        credit_limit = self.customer.credit_limit = 200
        currency = self.company.currency_id

        # Create invoice from yesterday with no payment terms
        # -> due immediate hence overdue
        overdue_invoice = self.create_invoice(self.product,
                                              self.customer,
                                              currency, amount, False, False)
        # Credit limit should be set
        self.assertEqual(self.customer.credit_limit, 200)
        # Customer should have credit
        self.assertEqual(self.customer.credit, amount)

        wizard_vals = self.sale_order.sudo(
            self.employee.user_id.id).action_confirm()

        # Since credit is overdue, SO should not be confirmed
        self.assertEqual(self.sale_order.state, 'draft',
                         'Employee: %s' % self.employee)

    def test_overdue_credit_employee(self):
        """
        Test Credit Limit: Exceed credit approval flow
        """
        amount = 300
        credit_limit = self.customer.credit_limit = 200
        currency = self.company.currency_id
        overdue_invoice = self.create_invoice(self.product,
                                              self.customer,
                                              currency, amount, True)
        # Credit limit should be set
        self.assertEqual(self.customer.credit_limit, 200)
        # Customer should have credit
        self.assertEqual(self.customer.credit, amount)

        wizard_vals = self.sale_order.sudo(
            self.employee.user_id.id).action_confirm()

        # Since credit is overdue, SO should not be confirmed
        self.assertEqual(self.sale_order.state, 'draft',
                         'Employee: %s' % self.employee)

        context = wizard_vals['context']
        context['active_id'] = self.sale_order.id
        context['active_model'] = 'sale.order'
        wizard = self.env['sale.customer.credit.limit.wizard'].with_context(
            context).create({})
        exceeded_credit = self.sale_order.amount_total + amount - credit_limit

        # Wizard should show the correct exceeded credit
        self.assertEqual(wizard.exceeded_credit, exceeded_credit)

        wizard.sudo(self.employee.user_id.id).action_exceed_limit()

        # Sale Order should be in approve state
        self.assertEqual(self.sale_order.state, 'approve',
                         'Employee: %s' % self.employee)

        subject = '%s needs approval' % self.sale_order.name
        manager = 'approval by %s' % self.manager.name
        exceeded_credit_str = '%.2f' % exceeded_credit
        credit = '<span style="color: red">%s %s</span>' % (
            exceeded_credit_str, self.company.currency_id.symbol)
        search_values = [('subject', 'like', subject),
                         ('body', 'like', manager),
                         ('body', 'like', credit)]
        messages = self.env['mail.message'].search(search_values)

        # Check if message to manager has been sent
        self.assertEqual(len(messages), 1)

        # Check employee can't approve SO
        with self.assertRaises(exceptions.ValidationError):
            self.sale_order.sudo(self.employee.user_id.id).action_approve()

        # Check employee can set it back to draft
        self.sale_order.sudo(self.employee.user_id.id).action_draft()
        self.assertEqual(self.sale_order.state, 'draft',
                         'Employee: %s' % self.employee)

        # Re-send for approval
        self.sale_order.sudo(self.employee.user_id.id).action_confirm()
        wizard.sudo(self.employee.user_id.id).action_exceed_limit()
        self.assertEqual(self.sale_order.state, 'approve')

        # Check that manager can approve SO
        self.sale_order.sudo(self.manager.user_id.id).action_approve()
        self.assertEqual(self.sale_order.state, 'sale',
                         'Manager: %s' % self.manager)

    def test_overdue_credit_manager(self):
        """
        Test Credit Limit: Manager can exceed credit directly
        """
        amount = 300
        credit_limit = self.customer.credit_limit = 200
        currency = self.company.currency_id
        overdue_invoice = self.create_invoice(self.product,
                                              self.customer,
                                              currency, amount, True)
        # Credit limit should be set
        self.assertEqual(self.customer.credit_limit, 200)
        # Customer should have credit
        self.assertEqual(self.customer.credit, amount)

        wizard_vals = self.sale_order.sudo(
            self.manager.user_id.id).action_confirm()

        # Since credit is overdue, SO should not be confirmed
        self.assertEqual(self.sale_order.state, 'draft',
                         'Manager: %s' % self.manager)

        context = wizard_vals['context']
        context['active_id'] = self.sale_order.id
        context['active_model'] = 'sale.order'
        wizard = self.env['sale.customer.credit.limit.wizard'].with_context(
            context).create({})
        exceeded_credit = self.sale_order.amount_total + amount - credit_limit

        # Wizard should show the correct exceeded credit
        self.assertEqual(wizard.exceeded_credit, exceeded_credit)

        wizard.sudo(self.manager.user_id.id).action_exceed_limit()

        # Sale Order should be directly in Sale state
        self.assertEqual(self.sale_order.state, 'sale',
                         'Manager: %s' % self.manager)

    def test_multi_currency(self):
        """
        Test Credit Limit: Multi currency
        """
        amount = 5000
        credit_limit = self.customer.credit_limit = 100
        company_currency = self.company.currency_id
        invoice_currency = self.get_currency([company_currency.id])
        order_currency = self.get_currency(
            [company_currency.id, invoice_currency.id])
        overdue_invoice = self.create_invoice(self.product,
                                              self.customer,
                                              invoice_currency, amount, True)
        sale_order_2 = self.create_sale_order(order_currency)

        wizard_vals = sale_order_2.sudo(
            self.employee.user_id.id).action_confirm()

        # Since credit is overdue, SO should not be confirmed
        self.assertEqual(sale_order_2.state, 'draft',
                         'Employee: %s' % self.employee)

        context = wizard_vals['context']
        context['active_id'] = sale_order_2.id
        context['active_model'] = 'sale.order'
        wizard = self.env['sale.customer.credit.limit.wizard'].with_context(
            context).create({})

        order_amount_computed = order_currency.compute(
            sale_order_2.amount_total,
            company_currency)
        invoice_amount_computed = invoice_currency.compute(
            overdue_invoice.residual,
            company_currency)

        exceeded_credit = order_amount_computed \
                          + invoice_amount_computed - credit_limit

        # Wizard should show the correctly computed exceeded credit
        self.assertEqual(wizard.exceeded_credit, exceeded_credit,
                         'Company Currency: %s; Invoice Currency: %s; '
                         'Order Currency: %s;' % (
                             company_currency.name, invoice_currency.name,
                             order_currency.name))

    ### SETUP CREATE RECORDS ###

    def create_company(self):
        currency = self.get_currency()
        name = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(6))
        partner = self.env['res.partner'].create({'name': name})
        company = self.env['res.company'].create({'name': name,
                                                  'currency_id': currency.id,
                                                  'partner_id': partner.id,
                                                  'manufacturing_lead': 5.0,
                                                  })
        return company

    def create_product(self):
        ProductProduct = self.env['product.product']
        uom = self.env['product.uom'].search([], limit=1)
        name = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(6))
        vals = {
            'name': name,
            'type': 'consu',
            'uom_id': uom.id,
            'uom_po_id': uom.id,
            'list_price': 1000,
            'sale_ok': True,
            'company_id': self.company.id,
        }
        return ProductProduct.create(vals)

    def create_warehouse(self):
        Warehouse = self.env['stock.warehouse']
        name = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(6))
        code = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(3))
        return Warehouse.create({'name': name,
                                 'code': code,
                                 'company_id': self.company.id})

    def create_sale_order(self, currency):
        SaleOrder = self.env['sale.order']
        line_vals = {
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': 2000,
        }
        order_vals = {
            'partner_id': self.customer.id,
            'user_id': self.employee.user_id.id,
            'date_order': date.today(),
            'order_line': [(0, 0, line_vals)],
            'picking_policy': 'direct',
            'warehouse_id': self.get_warehouse().id,
            'company_id': self.company.id,
            'pricelist_id': self.get_pricelist(currency).id,
        }
        sale_order = SaleOrder.sudo(self.employee.user_id.id).create(order_vals)
        return sale_order

    def create_pricelist(self, currency):
        name = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(6))
        return self.env['product.pricelist'].create({
            'name': name,
            'company_id': self.company.id,
            'currency_id': currency.id})

    def create_user(self, name):
        user = self.env['res.users'].create({'name': name,
                                             'login': '%s@test.com' % name,
                                             'email': '%s@test.com' % name,
                                             'company_ids': [
                                                 (4, self.company.id)],
                                             'company_id': self.company.id})
        user.write({'groups_id': [
            (4, self.ref('sales_team.group_sale_salesman'))]})
        return user

    def create_employee(self, user):
        HREmployee = self.env['hr.employee']
        return HREmployee.create({'name': user.name,
                                  'user_id': user.id,
                                  'company_id': self.company.id})

    def create_partner(self):
        ResPartner = self.env['res.partner']
        name = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(6))
        return ResPartner.create({'name': name})

    def create_invoice(self, product, partner, currency, amount,
                       overdue=False, with_payment_terms=True):
        account_revenue = self.env['account.account'].search([(
            'user_type_id', '=', self.env.ref(
                'account.data_account_type_revenue').id)], limit=1)
        payment_terms = self.env.ref('account.account_payment_term_15days')

        invoice = self.env['account.invoice'].create({
            'partner_id': partner.id,
            'reference_type': 'none',
            'name': "Supplier Invoice",
            'type': "out_invoice",
            'account_id': partner.property_account_receivable_id.id,
            'date_invoice': date.today() - relativedelta(days=1) if not overdue
            else date.today() - relativedelta(months=3),
            'payment_term_id': payment_terms.id if with_payment_terms
            else False,
            'currency_id': currency.id,
        })
        self.env['account.invoice.line'].create({
            'product_id': product.id,
            'quantity': 1,
            'price_unit': amount,
            'invoice_id': invoice.id,
            'name': 'something',
            'account_id': account_revenue.id,
        })
        invoice.action_invoice_open()
        return invoice

    ### SETUP GET RECORDS FROM DATABASE ###

    def get_company(self):
        if USE_EXISTING_RECS:
            ResCompany = self.env['res.company']
            company_ids = ResCompany.search([])
            return company_ids[random.randint(0, len(company_ids) - 1)]
        else:
            return self.create_company()

    def get_parents(self, emp):
        parents = []
        if emp.parent_id:
            parents.append(emp.parent_id)
            parents.extend(self.get_parents(emp.parent_id))
        return parents

    def get_employee(self, company, ignore_ids=None):
        HREmployee = self.env['hr.employee']
        if ignore_ids:
            parents = self.get_parents(HREmployee.browse(ignore_ids))
            ignore_ids.extend([parent.id for parent in parents])
        else:
            ignore_ids = []
        employee_ids = HREmployee.search([
            ('id', 'not in', ignore_ids),
            ('parent_id', 'not in', ignore_ids),
            ('user_id', '!=', False),
            ('user_id', '!=', 1),
            ('company_id', '=', company.id)])
        if employee_ids and USE_EXISTING_RECS:
            return employee_ids[random.randint(0, len(employee_ids) - 1)]
        else:
            name = ''.join(
                random.choice(string.ascii_lowercase) for _ in range(6))
            return self.create_employee(self.create_user(name))

    def get_manager(self, employee):
        if employee.parent_id:
            return employee.parent_id
        else:
            manager = self.get_employee(self.company, [employee.id])
            employee.parent_id = manager
            return manager

    def get_customer(self, ignore_ids=None, domain=None):
        ResPartner = self.env['res.partner']
        if ignore_ids is None:
            ignore_ids = []
        if domain is None:
            domain = []
        domain.extend([
            ('id', 'not in', ignore_ids),
            ('customer', '=', True),
            ('is_company', '=', True),
            ('company_id', '=', self.company.id)])
        customer_ids = ResPartner.search(domain)
        if customer_ids and USE_EXISTING_RECS:
            return customer_ids[random.randint(0, len(customer_ids) - 1)]
        else:
            customer = self.create_partner()
            customer.write({'customer': True,
                            'company_id': self.company.id,
                            'is_company': True})
            return customer

    def get_credit_free_customer(self, ignore_ids=None):
        return self.get_customer(ignore_ids, [('credit', '=', 0)])

    def get_product(self, ignore_ids=None):
        ProductProduct = self.env['product.product']
        if ignore_ids is None:
            ignore_ids = []
        product_ids = ProductProduct.search([
            ('id', 'not in', ignore_ids),
            ('list_price', '>', 0),
            ('sale_ok', '=', True)
        ])
        if product_ids and USE_EXISTING_RECS:
            return product_ids[random.randint(0, len(product_ids) - 1)]
        else:
            return self.create_product()

    def get_currency(self, ignore_ids=None):
        ResCurrency = self.env['res.currency']
        if ignore_ids is None:
            ignore_ids = []
        currency_ids = ResCurrency.search([
            ('id', 'not in', ignore_ids), ])
        if currency_ids:
            return currency_ids[random.randint(0, len(currency_ids) - 1)]
        else:
            inactive_ids = ResCurrency.search([
                ('id', 'not in', ignore_ids),
                ('active', '=', False)
            ])
            return inactive_ids[random.randint(0, len(inactive_ids) - 1)]

    def get_warehouse(self):
        warehouse = self.env['stock.warehouse'].search([
            ('company_id', '=', self.company.id)], limit=1)
        if warehouse and USE_EXISTING_RECS:
            return warehouse
        else:
            return self.create_warehouse()

    def get_pricelist(self, currency):
        pricelist = self.env['product.pricelist'].search(
            [('currency_id', '=', currency.id)], limit=1)
        if pricelist and USE_EXISTING_RECS:
            return pricelist
        else:
            return self.create_pricelist(currency)
