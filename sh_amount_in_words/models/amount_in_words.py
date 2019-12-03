# -*- coding: utf-8 -*-

# from __future__ import division, unicode_literals
from odoo import models, fields, api
from num2words import num2words

# Language support for num2words
# English = en , French = fr ,Spanish = es , German = de , Lithuanian = lt , Latvian = lv , Polish = pl ,Russian='ru'
# Norwegian = no ,Danish='dk',Portuguese = pt_BR , Arabic = ar ,Italian = it ,Hebrew = he,Indonesian - id
# Turkish -tr,Dutch - nl, Ukrainian - uk ,Slovenian - 

# Thai - th, Czech - cz
 
class ResCurrency(models.Model):
    _inherit= 'res.currency'

    currency_unit_label = fields.Char("Currency Unit")
    currency_subunit_label = fields.Char("Currency Subunit")
    
    amount_separator = fields.Char("Unit/Subunit Separator Text")
    close_financial_text = fields.Char("Close Financial Text")
    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
  
    amount_in_words = fields.Char(compute='amount_word', string='Amount', readonly=True)
    print_to_report = fields.Boolean("Show in Report",default=True)
          
    @api.depends('amount_total')
    def amount_word(self):
    
        language = 'en'    

        list_lang=[['en','en_US'],['en','en_AU'],['en','en_GB'],
            ['fr','fr_BE'],['fr','fr_CA'],['fr','fr_CH'],['fr','fr_FR'],
            ['es','es_ES'],['es','es_AR'],['es','es_BO'],['es','es_CL'],['es','es_CO'],['es','es_CR'],['es','es_DO'],
            ['es','es_EC'],['es','es_GT'],['es','es_MX'],['es','es_PA'],['es','es_PE'],['es','es_PY'],['es','es_UY'],['es','es_VE'],
            ['lt','lt_LT'],['lv','lv_LV'],['no','nb_NO'],['pl','pl_PL'],['ru','ru_RU'],
            ['dk','da_DK'],['pt_BR','pt_BR'],['de','de_DE'],['de','de_CH'],
            ['ar','ar_SY'],['it','it_IT'],['he','he_IL'],['id','id_ID'],['tr','tr_TR'],
            ['nl','nl_NL'],['nl','nl_BE'],['uk','uk_UA'],['sl','sl_SI'],['vi_VN','vi_VN']]            
# ['th','th_TH'],['cz','cs_CZ']        
        cnt = 0           
        for rec in list_lang[cnt:len(list_lang)]:
            if rec[1] == self.partner_id.lang:
                language = rec[0]
            cnt+=1       
            
        amount_str =  str('{:2f}'.format(self.amount_total))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]           

        before_amount_words = num2words(int(before_point_value),lang=language)
        after_amount_words = after_point_value

        amount = before_amount_words
        
           
        if self.currency_id and self.currency_id.amount_separator:
            amount = amount + ' ' + self.currency_id.amount_separator 
        
        amount = amount + ' ' + after_amount_words
             
        if self.currency_id and self.currency_id.currency_subunit_label:
            amount = amount +  self.currency_id.currency_subunit_label
                 
        if self.currency_id and self.currency_id.currency_unit_label:
            amount = amount + ' ' + self.currency_id.currency_unit_label
        
        self.amount_in_words = amount
     
class SaleOrder(models.Model):
    _inherit = 'sale.order'
 
    amount_in_words = fields.Char(compute='amount_word', string='Amount', readonly=True)
    print_to_report = fields.Boolean("Show in Report",default=True)
         
    @api.depends('amount_total')
    def amount_word(self):  
        language = 'en'    

        list_lang=[['en','en_US'],['en','en_AU'],['en','en_GB'],
            ['fr','fr_BE'],['fr','fr_CA',''],['fr','fr_CH'],['fr','fr_FR'],
            ['es','es_ES'],['es','es_AR'],['es','es_BO'],['es','es_CL'],['es','es_CO'],['es','es_CR'],['es','es_DO'],
            ['es','es_EC'],['es','es_GT'],['es','es_MX'],['es','es_PA'],['es','es_PE'],['es','es_PY'],['es','es_UY'],['es','es_VE'],
            ['lt','lt_LT'],['lv','lv_LV'],['no','nb_NO'],['pl','pl_PL'],['ru','ru_RU'],
            ['dk','da_DK'],['pt_BR','pt_BR'],['de','de_DE'],['de','de_CH'],
            ['ar','ar_SY'],['it','it_IT'],['he','he_IL'],['id','id_ID'],['tr','tr_TR'],
            ['nl','nl_NL'],['nl','nl_BE'],['uk','uk_UA'],['sl','sl_SI'],['vi_VN','vi_VN']]            
# ['th','th_TH'],['cz','cs_CZ']        
        cnt = 0           
        for rec in list_lang[cnt:len(list_lang)]:
            if rec[1] == self.partner_id.lang:
                language = rec[0]                
            cnt+=1       
           
        amount_str =  str('{:2f}'.format(self.amount_total))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]

        before_amount_words = num2words(int(before_point_value),lang=language)
        after_amount_words = after_point_value

        amount = before_amount_words
        

        
        if self.currency_id and self.currency_id.amount_separator:
            amount = amount + ' ' + self.currency_id.amount_separator 
            
        amount = amount + ' ' +  after_amount_words
        
        if self.currency_id and self.currency_id.currency_subunit_label:
            amount = amount + self.currency_id.currency_subunit_label
                 
        if self.currency_id and self.currency_id.currency_unit_label:
            amount = amount + ' ' + self.currency_id.currency_unit_label
        
        self.amount_in_words = amount

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    amount_in_words = fields.Char(compute='amount_word', string='Amount', readonly=True)
    print_to_report = fields.Boolean("Show in Report",default=True)
        
    @api.depends('amount_total')
    def amount_word(self):
    
        language = 'en'    

        list_lang=[['en','en_US'],['en','en_AU'],['en','en_GB'],['en','en_IN'],
            ['fr','fr_BE'],['fr','fr_CA'],['fr','fr_CH'],['fr','fr_FR'],
            ['es','es_ES'],['es','es_AR'],['es','es_BO'],['es','es_CL'],['es','es_CO'],['es','es_CR'],['es','es_DO'],
            ['es','es_EC'],['es','es_GT'],['es','es_MX'],['es','es_PA'],['es','es_PE'],['es','es_PY'],['es','es_UY'],['es','es_VE'],            
            ['lt','lt_LT'],['lv','lv_LV'],['no','nb_NO'],['pl','pl_PL'],['ru','ru_RU'],
            ['dk','da_DK'],['pt_BR','pt_BR'],['de','de_DE'],['de','de_CH'],
            ['ar','ar_SY'],['it','it_IT'],['he','he_IL'],['id','id_ID'],['tr','tr_TR'],
            ['nl','nl_NL'],['nl','nl_BE'],['uk','uk_UA'],['sl','sl_SI'],['vi_VN','vi_VN']]
        
#     ['th','th_TH'],['cz','cs_CZ']            
        
        cnt = 0           
        for rec in list_lang[cnt:len(list_lang)]:
            if rec[1] == self.partner_id.lang:
                language = rec[0]
            cnt+=1       
            
        amount_str =  str('{:2f}'.format(self.amount_total))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]
           
        before_amount_words = num2words(int(before_point_value),lang=language)
        after_amount_words = after_point_value

        amount = before_amount_words
        if self.currency_id and self.currency_id.currency_unit_label:
            amount = amount + ' ' + self.currency_id.currency_unit_label 
           
        if self.currency_id and self.currency_id.amount_separator:
            amount = amount + ' ' + self.currency_id.amount_separator 
        
        amount = amount + ' ' + after_amount_words
        
        if self.currency_id and self.currency_id.currency_subunit_label:
            amount = amount + self.currency_id.currency_subunit_label
                 
        if self.currency_id and self.currency_id.currency_unit_label:
            amount = amount + ' ' + self.currency_id.currency_unit_label
        
        self.amount_in_words = amount


# en (English, default)
# ar (Arabic)
# de (German)
# dk (Danish)
# en_GB (English - Great Britain)
# en_IN (English - India)
# es (Spanish)
# es_CO (Spanish - Colombia)
# es_VE (Spanish - Venezuela)
# eu (EURO)
# fr (French)
# fr_CH (French - Switzerland)
# fr_DZ (French - Algeria)
# he (Hebrew)
# id (Indonesian)
# it (Italian)
# lt (Lithuanian)
# lv (Latvian)
# no (Norwegian)
# pl (Polish)
# pt_BR (Brazilian Portuguese)
# sl (Slovene)
# ru (Russian)
# tr (Turkish)
# vn (Vietnamese)
# nl (Dutch)
# uk (Ukrainian)
        
