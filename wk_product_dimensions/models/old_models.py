# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################


from odoo import models, fields, api, _
from odoo.exceptions import MissingError, UserError, ValidationError
from odoo.tools.safe_eval import safe_eval, test_python_expr

import logging
_logger = logging.getLogger(__name__)
import urllib2
import json
import urllib
from pprint import pprint
from bs4 import BeautifulSoup
import re
# http://www.learndatasci.com/python-finance-part-yahoo-finance-api-pandas-matplotlib/

# view=basic date=Ymd; currency=true format=json and callback=list
class BaseURL(object):
    Google = 'https://finance.google.com/finance/converter'
    Yahoo = 'https://query.yahooapis.com/v1/public/yql'
    Yahoo_USD = 'https://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'
    ECB_EUR= 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    Fixer= 'https://api.fixer.io/latest'

class FetchCurrency(object):
    """docstring for ."""
    def __init__(self, service,base_currency,uri):
        self.service = service
        self.base_currency = base_currency
        self.uri = uri

    @staticmethod
    def fetch_data(uri):
        data =None
        status = False
        messege = ''
        _logger.info("==%r=="%(uri))
        try:
            response = urllib.urlopen(uri)
            status = response.code==200
            data = response.read()
        except Exception as e:
            messege +='%s'%(e)
        return dict(
            data=data,
            status=status,
            messege=messege,

        )

    def get_ecb_uri(self):
        return self.uri.ECB

    def get_google_uri(self,currency_code):
        return "%s?a=1&from=%s&to=%s"%(self.uri.Google,self.base_currency,currency_code)
        # https://finance.google.com/finance/converter?a=1&from=EUR&to=AUD

    def get_fixer_uri(self):
        return'%s?base=%s'%(self.uri.Fixer,self.base_currency)
        # return "https://api.fixer.io/latest?symbols=%s,%s"%(self.base_currency,currency_code)

    def get_yahoo_uri(self,currency_code):
        base_url = '%?'%(self.uri.Yahoo)
        query = {
            'q': 'select * from yahoo.finance.quote where symbol in ("EURAFN")',
            'format': 'json',
            'env': 'store://datatables.org/alltableswithkeys'
        }
        return  base_url + urllib.urlencode(query)

    def fetch_google_rate(self,currency_code):
        rate = None
        uri   = self.get_google_uri(currency_code)
        fetch_res = self.fetch_data(uri)
        if fetch_res.get('status'):
            soup = BeautifulSoup(fetch_res.get('data'), 'html.parser')
            rate = soup.find('span', attrs={'class': 'bld'}).text# "/[^0-9\.]/"
            if rate: rate = re.compile(r'[^\d.,]+').sub('', rate)
        return dict(
            # raw_data= fetch_res,
            rate =rate
        )

    def fetch_fixer_rate(self,currency_code):
        rate = None
        uri   = self.get_fixer_uri()
        fetch_res = self.fetch_data(uri)
        if fetch_res.get('status'):
            data = json.dumps(fetch_res.get('data'))
            raise Warning(data)

            rate = (data.get('rates'))#.get('currency_code')
            raise Warning(json.dumps(rates))
            if rate:pass

        return dict(
            raw_data= fetch_res,
            rate = rate
        )

    def fetch_yahoo_rate(self,currency_code):
        rate = None
        uri   = self.get_yahoo_uri(currency_code)
        fetch_res = self.fetch_data(uri)
        if fetch_res.get('status'):
            quote = json.loads(data)
            pprint(quote)
        return dict(
            raw_data= fetch_res,
            rate = rate
        )

    def fetch_rate(self,currency_code):
        if self.service=='google':
            return self.fetch_google_rate(currency_code=currency_code)
        elif self.service=='yahoo':
            return self.fetch_fixer_rate(currency_code=currency_code)
        elif self.service=='fixer':
            return self.fetch_fixer_rate(currency_code=currency_code)

        # obj = json.loads(content[3:])
        # return obj[0]
        # except Exception as e:
        #     raise

SERVICE = [
    ('yahoo','Yahoo')
]
class WizardCurrencyRate(models.Model):
    _name = "currency.rate.update.wizard"


    DEFAULT_PYTHON_CODE = """# Available variables:
    #  - time, datetime, dateutil, timezone: Python libraries
    #  - env: Odoo Environement
    #  - model: Model of the record on which the action is triggered
    #  - record: Record on which the action is triggered if there is one, otherwise None
    #  - records: Records on which the action is triggered if there is one, otherwise None
    #  - log : log(message), function to log debug information in logging table
    #  - Warning: Warning Exception to use with raise
    # To return an action, assign: action = {...}\n\n\n\n"""

    def get_default_base_currency(self):
        return  self.env['res.currency'].search([('active','=',1)]).filtered(lambda c:c.rate==1)[0]

    service = fields.Selection(
        selection =SERVICE,
        string = 'Service',
        required=1
    )

    service_uri = fields.Selection(
        selection =SERVICE,
        string = 'Service',
        required=1
    )

    code  = fields.Text(
        string='Python Code',
        default=DEFAULT_PYTHON_CODE,
    )
    base_currency_id = fields.Many2one(
        comodel_name = 'res.currency',
        string = 'Currency',
        default = lambda self:self.get_default_base_currency(),
    )

    @api.constrains('code')
    def _check_python_code(self):
        for action in self.filtered('code'):
            msg = test_python_expr(expr=action.code.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)

    @staticmethod
    def fetch_currency_sdk(service,base_currency):
        url=BaseURL()
        return FetchCurrency(service,base_currency,url)

    @api.multi
    def wk_fetch_currency_data(self):
        currencie_ids = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_ids'))
        base_currency =self.base_currency_id.name
        service =self.service
        sdk = self.fetch_currency_sdk(service,base_currency)
        # currencies = currencie_ids.filtered(
        #     lambda c:c.name!=base_currency).mapped(
        #     lambda cr:'%s%s'%(base_currency,cr.name))
        #
        base_currency = base_currency
        currency_pairs = ','.join(base_currency + x.name for x in currencie_ids if base_currency != x.name)
        # raise Warning(currency_pairs)
        #
        # raise Warning(currency_pairs)
        # #
        # yql_base_url = "https://query.yahooapis.com/v1/public/yql"
        # yql_query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("' + currency_pairs + '")'
        # yql_query_url = yql_base_url + "?q=" + yql_query + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        # raise Warning(sdk.fetch_data(yql_query_url))
        #
        for currency  in currencie_ids:
            result = sdk.fetch_rate(currency.name)
            raise Warning(result)
