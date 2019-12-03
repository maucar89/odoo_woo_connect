# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import tempfile
import binascii
import logging
from datetime import datetime
from odoo.exceptions import Warning
from odoo import models, fields, api, exceptions, _
_logger = logging.getLogger(__name__)
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class account_bank_statement_wizard(models.TransientModel):
    _name= "account.bank.statement.wizard"

    file = fields.Binary('File')
    file_opt = fields.Selection([('excel','Excel'),('csv','CSV')])


    @api.multi
    def import_file(self):
        if not file:
            raise Warning('Please Select File')
        if self.file_opt == 'csv':
            keys = ['date','ref','partner','memo','amount']                     
            data = base64.b64decode(self.file)
            file_input = cStringIO.StringIO(data)
            file_input.seek(0)
            reader_info = []
            reader = csv.reader(file_input, delimiter=',')
 
            try:
                reader_info.extend(reader)
            except Exception:
                raise exceptions.Warning(_("Not a valid file!"))
            values = {}
            for i in range(len(reader_info)):
                field = map(str, reader_info[i])
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        res = self._create_statement_lines(values)
        elif self.file_opt == 'excel':
            fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            for row_no in range(sheet.nrows):
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = (map(lambda row:isinstance(row.value, unicode) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    if not line[0]:
                        raise Warning('Please Provide Date Field Value')
                    a1 = int(float(line[0]))
                    a1_as_datetime = datetime(*xlrd.xldate_as_tuple(a1, workbook.datemode))
                    date_string = a1_as_datetime.date().strftime('%Y-%m-%d')
                    
                    values.update( {'date':date_string,
                                    'ref': line[1],
                                    'partner': line[2],
                                    'memo': line[3],
                                    'amount': line[4],
                                    })
                    res = self._create_statement_lines(values)
                    
        else:
            raise Warning('Please Select File Type')
        self.env['account.bank.statement'].browse(self._context.get('active_id'))._end_balance()
        return res
#
    @api.multi
    def _create_statement_lines(self,val):
        partner_id = self._find_partner(val.get('partner'))
        if not val.get('date'):
            raise Warning('Please Provide Date Field Value')
        if not val.get('memo'):
            raise Warning('Please Provide Memo Field Value')
        aaa = self._cr.execute("insert into account_bank_statement_line (date,ref,partner_id,name,amount,statement_id) values (%s,%s,%s,%s,%s,%s)",(val.get('date'),val.get('ref'), partner_id,val.get('memo'),val.get('amount'),self._context.get('active_id')))
        return True
#
    def _find_partner(self,name):
        partner_id = self.env['res.partner'].search([('name','=',name)])
        if partner_id:
            return partner_id.id
        else:
            return


