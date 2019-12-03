from odoo import api, fields, models, _

class Coupon(models.Model):
    _name="promotion.coupon"
    _rec_name = 'code'
    
    _sql_constraints = [
        ('coupon_code', 'unique(code)', 'Cant be duplicate value for Coupon code field!')]
    
    promotion_id= fields.Many2one('promotion.method','Promotion')
    code = fields.Char("Coupon Code")
    expiry_date = fields.Date('Expiration Date')
    order_id =fields.Many2one('sale.order')
    applied_order_id = fields.Many2one('sale.order')
    partner_id = fields.Many2one('res.partner')
    used = fields.Boolean("Coupon Used Or Not",default=False)
    
    def send_coupon_mail(self):
        template = self.env.ref('promotion_ept.next_order_coupon_email_template')
        mail_id = self.env['mail.template'].browse(template.id).send_mail(self.id)
        self.env['mail.mail'].sudo().search([('id','=',mail_id)]).send()
        