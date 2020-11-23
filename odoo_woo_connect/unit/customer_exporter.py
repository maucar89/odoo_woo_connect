# -*- coding: utf-8 -*-
#
#
#    Techspawn Solutions Pvt. Ltd.
#    Copyright (C) 2016-TODAY Techspawn(<http://www.Techspawn.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import logging
from ..model.api import API
from datetime import datetime
from datetime import timedelta
from . backend_adapter import WpImportExport
from odoo.exceptions import Warning


_logger = logging.getLogger(__name__)


class WpCustomerExport(WpImportExport):

    """ Models for woocommerce customer export """

    def get_api_method(self, method, args):
        """ get api for customer"""
        api_method = None
        if method == 'customer':
            if not args[0]:
                api_method = 'customers'
            else:
                api_method = 'customers/' + str(args[0])
        return api_method

    def get_billing(self, child_ids):
        """ return billing address customer """
        default_billing = []
        if child_ids:
            for billing_id in child_ids:
                if billing_id.type == 'invoice':
                    if billing_id.default_address == True:
                        default_billing.append({
                            # "type": billing_id.type or None,
                            # "name": billing_id.name or None,
                            "first_name": billing_id.first_name or billing_id.display_name.split(',')[1] or '',
                            "last_name": billing_id.last_name or '',
                            "email": billing_id.email or '',
                            "address_1": billing_id.street or '',
                            "address_2": billing_id.street2 or '',
                            "city": billing_id.city or '',
                            "state": billing_id.state_id.code or '',
                            "postcode": billing_id.zip or '',
                            "country": billing_id.country_id.code or '',
                            "phone": billing_id.phone or '',
                            # "mobile": billing_id.mobile or None,
                            # "notes": billing_id.comment or None,
                        })
                    else:
                        default_billing.append({
                            "first_name": billing_id.first_name or billing_id.display_name.split(',')[1] or '',
                            "last_name": billing_id.last_name or '',
                            "company" : billing_id.commercial_company_name or '',
                            "address_1": billing_id.street or '',
                            "address_2": billing_id.street2 or '',
                            "city": billing_id.city or '',
                            "state": billing_id.state_id.code or '',
                            "postcode": billing_id.zip or '',
                            "country": billing_id.country_id.code or '',
                            "email": billing_id.email or '',
                            "phone": billing_id.phone or '',
                            })
        return default_billing


    # def get_shipping_address(self, child_ids):
    #     """ return shipping address customer """
    #     shipping = []
    #     if child_ids:
    #         for shipping_id in child_ids:
    #             if shipping_id.type == 'contact':
    #                 shipping.append({
    #                     "type": shipping_id.type or None,
    #                     "name": shipping_id.name or None,
    #                     "email": shipping_id.email or None,
    #                     "phone": shipping_id.phone or None,
    #                     "mobile": shipping_id.mobile or None,
    #                     "notes": shipping_id.comment or None,
    #                 })
    #
    #             elif shipping_id.type == 'invoice' or shipping_id.type == 'delivery' or shipping_id.type == 'other':
    #                 shipping.append({
    #                     "type": shipping_id.type or '',
    #                     "name": shipping_id.name or '',
    #                     "email": shipping_id.email or '',
    #                     "address_1": shipping_id.street or '',
    #                     "address_2": shipping_id.street2 or '',
    #                     "city": shipping_id.city or '',
    #                     "state": shipping_id.state_id.code or '',
    #                     "postcode": shipping_id.zip or '',
    #                     "country": shipping_id.country_id.code or '',
    #                     "phone": shipping_id.phone or '',
    #                     "mobile": shipping_id.mobile or '',
    #                     "notes": shipping_id.comment or '',
    #                 })
    #     return shipping

    def get_shipping(self, child_ids):
        default_shipping = []
        if child_ids:
            for shipping_id in child_ids:
                if shipping_id.type == "delivery":
                    if shipping_id.default_address == True:
                        default_shipping.append({
                            # "type": shipping_id.type or None,
                            # "name": shipping_id.name or None,
                            # "email": shipping_id.email or None,
                            "first_name": shipping_id.first_name or shipping_id.display_name.split(',')[1] or '',
                            "last_name": shipping_id.last_name or '',
                            "address_1": shipping_id.street or '',
                            "address_2": shipping_id.street2 or '',
                            "city": shipping_id.city or '',
                            "state": shipping_id.state_id.code or '',
                            "postcode": shipping_id.zip or '',
                            "country": shipping_id.country_id.code or '',
                            # "phone": shipping_id.phone or None,
                            # "mobile": shipping_id.mobile or None,
                            # "notes": shipping_id.comment or None,
                        })
                    else:
                        default_shipping.append({
                            # "type": shipping_id.type or None,
                            # "email": shipping_id.email or None,
                            "first_name": shipping_id.first_name or shipping_id.display_name.split(',')[1] or '',
                            "last_name": shipping_id.last_name or '',
                            "address_1": shipping_id.street or '',
                            "address_2": shipping_id.street2 or '',
                            "city": shipping_id.city or '',
                            "state": shipping_id.state_id.code or '',
                            "postcode": shipping_id.zip or '',
                            "country": shipping_id.country_id.code or '',
                        })
                else:
                    for s_address in shipping_id.shipping_ids:
                        default_shipping.append({
                            "first_name": s_address.ship_first_name or shipping_id.display_name.split(',')[1] or '',
                            "last_name": s_address.ship_last_name or '',
                            "address_1": s_address.ship_address1 or '',
                            "address_2": s_address.ship_address2 or '',
                            "city": s_address.ship_city or '',
                            "state": s_address.ship_state.name or '',
                            "postcode": s_address.ship_zip or '',
                            "country": s_address.ship_country.code or '',
                        })

        return default_shipping

    def get_multi(self,child_ids):
        multi = []
        if child_ids:
            for data in child_ids:
                if data.type == 'delivery':
                    data_type = 'shipping'
                    if data.default_address != True:
                        multi.append({
                            "type": data_type or None,
                            "name": data.name or None,
                            "shipping_first_name": data.first_name or None,
                            "shipping_last_name": data.last_name or None,
                            "shipping_company": data.company or None,
                            "email": data.email or None,
                            "shipping_address_1": data.street or None,
                            "shipping_address_2": data.street2 or None,
                            "shipping_city": data.city or None,
                            "shipping_state": data.state_id.code or None,
                            "shipping_postcode": data.zip or None,
                            "shipping_country": data.country_id.code or None,
                            "phone": data.phone or None,
                            "mobile": data.mobile or None,
                            "notes": data.comment or None,
                        })
                if data.type == 'invoice':
                    data_type = 'billing'
                    if data.default_address != True:
                        multi.append({
                            "type": data_type or None,
                            "name": data.name or None,
                            "email": data.email or None,
                            "billing_first_name": data.first_name or None,
                            "billing_last_name": data.last_name or None,
                            "billing_company": data.company or None,
                            "billing_address_1": data.street or None,
                            "billing_address_2": data.street2 or None,
                            "billing_city": data.city or None,
                            "billing_state": data.state_id.code or None,
                            "billing_postcode": data.zip or None,
                            "billing_country": data.country_id.code or None,
                            "billing_phone": data.phone or None,
                            "mobile": data.mobile or None,
                            "notes": data.comment or None,
                        })

        return multi

    def export_customer(self, method, arguments):
        """ Export customer data"""
        bill_flag = False
        inv_flag = False
        _logger.debug("Start calling Woocommerce api %s", method)

        if arguments[1].company_type == 'company':
            company = arguments[1].name
        else:
            company = None

        for data in arguments[1].child_ids:
            if data.type == 'invoice':
                def_bill = self.get_billing(data)
                bill_flag = True
            elif data.type == 'delivery':
                def_ship = self.get_shipping(data)
                inv_flag = True

        if not bill_flag:
            def_bill = self.get_billing(arguments[1])
        if not inv_flag:
            def_ship = self.get_shipping(arguments[1])

        if def_bill == []:
            def_bill = None
        else:
            def_bill = def_bill[0]

        # def_ship = self.get_shipping(arguments[1].child_ids)

        if def_ship == []:
            def_ship = None
        else:
            def_ship = def_ship[0]

        multi_data = self.get_multi(arguments[1].child_ids)
        if multi_data == []:
            multi_data = None
        else:
            multi_data = multi_data

        # result_dict = {
        #     "email": arguments[1].email or '',
        #     "first_name": arguments[1].first_name or arguments[1].name or '',
        #     "last_name": arguments[1].last_name or '',
        #     "username": arguments[1].username or '',
        #     "password": arguments[1].password or 'None',
        #     "company": company or None,
        #     "shipping": {"first_name": arguments[1].first_name or arguments[1].name or '',
        #                 "last_name": arguments[1].last_name or '',
        #                 "company": arguments[1].company or '',
        #                 "address_1": arguments[1].street or '',
        #                 "address_2": arguments[1].street2 or '',
        #                 "city": arguments[1].city or '',
        #                 "state": arguments[1].state_id.code or '',
        #                 "postcode": arguments[1].zip or '',
        #                 "country": arguments[1].country_id.code or '',
        #                 "email": arguments[1].email or '',
        #                 "phone": arguments[1].phone or '',
        #                 },
        #     "billing": {"first_name": arguments[1].first_name or arguments[1].name or '',
        #                 "last_name": arguments[1].last_name or '',
        #                 "company": arguments[1].company or '',
        #                 "address_1": arguments[1].street or '',
        #                 "address_2": arguments[1].street2 or '',
        #                 "city": arguments[1].city or '',
        #                 "state": arguments[1].state_id.code or '',
        #                 "postcode": arguments[1].zip or '',
        #                 "country": arguments[1].country_id.code or '',
        #                 "email": arguments[1].email or '',
        #                 "phone": arguments[1].phone or '',
        #                 },
        # }
        result_dict = {
            "email": arguments[1].email or '',
            "first_name": arguments[1].first_name or arguments[1].name or '',
            "last_name": arguments[1].last_name or '',
            "username": arguments[1].username or arguments[1].name or None,
            # "birthdate": arguments[1].birthdate or '',
            "company": company or '',
            "billing": def_bill or None,
            "shipping": def_ship or None,
            "multi_address": multi_data or None,
        }

        if not arguments[0]:
            result_dict.update({"password": arguments[1].username or 'None', })

        res = self.export(method, result_dict, arguments)
        if res:
            res_dict = res.json()
        else:
            res_dict = res.json()
        return {'status': res.status_code, 'data': res_dict or {}}