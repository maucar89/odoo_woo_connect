from odoo import models, fields, api, _
from odoo.exceptions import UserError,Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    promotion_id = fields.Many2one("promotion.method", string="Promotion Method",copy=False)
    coupon_code=fields.Char("Coupon Code",help="Add coupon code to apply promotion in sale order",copy=False)
    promo_price=fields.Float(compute="_amount_all",string="Discount",copy=False)
    promo_note = fields.Char("Promotion Notes",help="Display next order coupon code here.",copy=False)
    
    @api.onchange('partner_id','order_line','order_line.product_id')
    def onchange_promotion_order_line(self):
        '''
            This Onchnage use for remove promotion.
        '''
        for order in self:
            if order.promotion_id:
                raise UserError(_("You can not change the order after promotion applied in order.\n If you want to change the order then first remove promotion."))
        return {}        
    
    @api.multi
    def write(self,values):
        res=super(SaleOrder,self).write(values)
        if self._context.get('promotion'):
            res=super(SaleOrder,self).write(values)
        else:
            for line in self.order_line:
                if line.is_promotion==True and line.price_unit==0.0:
                    line.unlink()
        return res
        
    
    @api.depends('order_line.price_total')
    def _amount_all(self):
        '''
            This method use for recalculate untax amount,tax,total and add promo amount to order.
        '''
        super(SaleOrder,self)._amount_all()
        for order in self:
            discount=0.0
            amount_untaxed = promo_price = 0.0
            for line in order.order_line:
                if not line.price_subtotal<0.0:
                    amount_untaxed += line.price_subtotal
                if line.is_promotion:
                    promo_price = line.price_subtotal
                if not line.is_promotion and line.price_subtotal<0.0:
                    discount=discount+line.price_subtotal
            amount_tax=order.amount_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'promo_price': order.pricelist_id.currency_id.round(promo_price),
                'amount_total': amount_untaxed + amount_tax + promo_price + discount
            })       
    
    @api.multi
    def find_promo(self):
        self._promotion_unset()
        if len(self.coupon_code)!=10:
            promotion = self.env['promotion.method'].sudo().search([('coupon_code', '=', self.coupon_code)])
            if promotion:
                self.apply_promotion(promotion)
        elif len(self.coupon_code)==10:
            promotion = self.env['promotion.coupon'].sudo().search([('code','=',self.coupon_code),('partner_id','=',self.partner_id.id),('used','=',False)]).promotion_id
            if promotion:
                self.apply_promotion(promotion)
            else:
                self.message_post(body=("<b>Coupon Code Does not match to any promotion or you are not applicable for this coupon or coupon use limit goen to maximum.</b>"))
        else:
            self.message_post(body=("<b>Coupon Code Does not match to any promotion.</b>"))
    
    @api.multi        
    def unset_promotion(self):  
        self._promotion_unset()  
        self.write({'coupon_code':''})    
    @api.multi
    def _promotion_unset(self):
        '''
            This method use for remove promotion.
        '''
        if len(self.coupon_code)!=10:
            self.write({'promo_note':''})
            self.env['promotion.coupon'].search([('promotion_id','=',self.promotion_id.id),('order_id','=',self.id)]).unlink()
        else:
            coupon=self.env['promotion.coupon'].search([('code','=',self.coupon_code)])
            if coupon.applied_order_id.state not in ['done','sale']:
                coupon.write({'used':False,'applied_order_id':False})
        self.env['sale.order'].search([('id','in',self.ids)]).write({'promotion_id':False,'promo_price':0.0})
        self.env['sale.order.line'].search([('order_id', 'in', self.ids),('is_promotion', '=', True)]).unlink()
        self.env['sale.order.line'].search([('order_id','in', self.ids)]).write({'discount':0.0})
  
    @api.multi
    def apply_promotion(self,promotion):
        '''
            This method use for apply promotion.
        '''
        for order in self:
            
                order.promotion_id=promotion
                order.set_saleorderline()
                if order.order_line:
                    price_unit=promotion.set_promotion(order,promotion,other_promotion=False)
                    if price_unit<0.0:
                        if -(price_unit)<=order.amount_untaxed or promotion.compute_price=='bogo_sale':
                            price=-(price_unit)
                            if promotion.max_promotion_amount!=0.0 and price>=promotion.max_promotion_amount:
                                price_unit=order.update_orderline_promotionprice(price,promotion.max_promotion_amount)
                            if promotion.used_in_next_order and len(order.coupon_code)!=10:
                                coupon = promotion.applied_on_next_order(order)
                            else:
                                res=order._create_promotion_line(promotion, price_unit)
                            order.message_post(body=("<b>Promotion applied successfully</b>"))
                            return True
                        else:
                            if price_unit>0.0 and promotion.max_promotion_amount!=0.0:
                                order.check_max_promotion(promotion)
                                order.message_post(body=("<b>Promotion applied successfully</b>"))
                                return True
                            elif not price_unit > 0.0:
                                order._promotion_unset()
                                order.message_post(body=("<b>Order amount is less than Discount</b>"))
                                return False
                            else:
                                order.message_post(body=("<b>Promotion applied successfully</b>"))
                                return True
                    else:
                        if price_unit>0.0 and promotion.max_promotion_amount!=0.0:
                            order.check_max_promotion(promotion)
                            order.message_post(body=("<b>Promotion applied successfully</b>"))
                            return True
                        elif promotion.used_in_next_order and len(order.coupon_code)!=10:
                            coupon = promotion.applied_on_next_order(order)
                            return True
                        elif not price_unit > 0.0:
                            order._promotion_unset()
                            return False
                        else:
                            order.message_post(body=("<b>Promotion applied successfully</b>"))
                            return True
                else:
                    order._promotion_unset()
                    order.message_post(body=("<b>Order not Contain Promotion Criteria product.</b>"))
        
    def check_max_promotion(self,promotion):
        total=0.0
        for line in self.order_line:
            amount=(line.product_uom_qty*line.price_unit*100)/line.discount
            total +=amount
        if total-self.amount_untaxed>promotion.max_promotion_amount:
            self.order_line.write({'discount':0.0})
            res=self._create_promotion_line(promotion, -(promotion.max_promotion_amount))
    
    def set_saleorderline(self):
            '''
                This method use for merge orderline which contains same product in different line.
            '''
            finalids=[]
            promo=self.promotion_id
            for line in self.order_line:
                count=0.0
                ids=[]
                orderline=self.env['sale.order.line'].search([('order_id','=',self.id),('product_id','=',line.product_id.id),('product_uom','=',line.product_uom.id),('discount','=',line.discount)])
                for ol in orderline:
                    count+=1
                    if count>1:
                        line.write({'product_uom_qty':line.product_uom_qty+ol.product_uom_qty})
                        ids.insert(0, ol.id)
                for id in ids:
                    if id not in finalids:
                        finalids.append(id)
            for id in finalids:
                line=self.env['sale.order.line'].search([('id','=',id)])
                self.promotion_id=False
                line.unlink()
            self.promotion_id=promo
            
    @api.multi
    def action_cancel(self):
        res=super(SaleOrder,self).action_cancel()
        for order in self:
            if order.promotion_id.used_in_next_order:
                coupon=self.env['promotion.coupon'].search([('order_id','=',order.id)])
                coupon.unlink()
            if order.promotion_id:
                order.write({'promotion_id':False,'promo_price':0.0,'coupon_code':''})
                for orderline in order.order_line:
                    if orderline.is_promotion:
                        orderline.unlink()
        return res
    @api.multi
    def action_confirm(self):
        '''
            This method use for reapply promotion and if it not applied then giv pop-message for remove promotion first.
        '''
        for order in self:
            promo = order.promotion_id
            if promo:
                order._promotion_unset()
                order.promotion_id=promo
                promotion=order.promotion_id
                price_unit=promotion.set_promotion(order,promotion,other_promotion=False)
                if price_unit<0.0:
                    if -(price_unit)<=order.amount_untaxed or promotion.compute_price=='bogo_sale':
                        price=-(price_unit)
                        if promotion.max_promotion_amount!=0.0 and price>=promotion.max_promotion_amount:
                            price_unit=order.update_orderline_promotionprice(price,promotion.max_promotion_amount)
                        if promotion.used_in_next_order and len(order.coupon_code)!=10:
                            coupon = promotion.applied_on_next_order(order)
                        else:
                            res=order._create_promotion_line(promotion, price_unit)
                        order.message_post(body=("<b>Promotion applied successfully</b>"))
                    else:
                        if price_unit>0.0 and promotion.max_promotion_amount!=0.0:
                            order.check_max_promotion(promotion)
                        elif not price_unit > 0.0:
                            order._promotion_unset()
                            order.message_post(body=("<b>Order amount is less than Discount</b>"))
                            return False
                        else:
                            order.message_post(body=("<b>Promotion applied successfully</b>"))
                else:
                    if price_unit>0.0 and promotion.max_promotion_amount!=0.0:
                        order.check_max_promotion(promotion)
                    elif promotion.used_in_next_order and len(order.coupon_code)!=10:
                        coupon = promotion.applied_on_next_order(order)
                    elif not price_unit > 0.0:
                        order._promotion_unset()
                        return False
                    else:
                        order.message_post(body=("<b>Promotion applied successfully</b>"))
        res=super(SaleOrder,self).action_confirm()
        return res
        
    
    def _create_promotion_line(self, promotion, price_unit):
        '''
            This method use for add promotionline in order.
        '''
        SaleOrderLine = self.env['sale.order.line']
        # Create the sale order line
        if promotion.bogo_sale_on in ['bxgy']:
            sol=SaleOrderLine.search([('order_id','=',self.id),('promotion_product','=',True)])
            for line in sol:
                qty=line.product_uom_qty
                free_qty=qty/promotion.bxgy_Aproduct_unit
                price_unit=price_unit*int(free_qty)
                line.write({'promotion_product':False})
                name = line.product_id.name_get()[0][1]
                if line.product_id.description_sale:
                    name += '\n' + line.product_id.description_sale
                if line:
                    values = {
                    'order_id': self.id,
                    'name': name,
                    'product_uom_qty': int(free_qty)*promotion.bxgy_Bproduct_unit,
                    'product_uom': line.product_uom.id,
                    'product_id':line.product_id.id,
                    'price_unit': line.price_unit,
                    'tax_id':[(6,0,line.product_id.taxes_id.ids)],
                    'is_promotion': True,
                    'promotion_product':True,
                    }
                    if self.order_line:
                        values['sequence'] = self.order_line[-1].sequence + 1
                    sale_order_line = SaleOrderLine.sudo().create(values)
        elif promotion.bogo_sale_on in ['bogelse']:
            sol=SaleOrderLine.search([('order_id','=',self.id),('promotion_product','=',True)])
            for line in sol:
                qty=line.product_uom_qty
                free_qty=qty/promotion.bogoelse_Aproduct_unit
                price_unit=price_unit*int(free_qty)
                line.write({'promotion_product':False})
                for product in promotion.free_products:
                    name = product.name_get()[0][1]
                    if product.description_sale:
                        name += '\n' + product.description_sale
                    if line:
                        values = {
                        'order_id': self.id,
                        'name': name,
                        'product_uom_qty': int(free_qty)*promotion.bogoelse_Bproduct_unit,
                        'product_uom': product.uom_id.id,
                        'product_id':product.id,
                        'price_unit': product.lst_price,
                        'tax_id':[(6,0,product.taxes_id.ids)],
                        'is_promotion': True,
                        'promotion_product':True,
                        }
                        if self.order_line:
                            values['sequence'] = self.order_line[-1].sequence + 1
                        sale_order_line = SaleOrderLine.sudo().create(values)
        else:
            sol=SaleOrderLine.search([('order_id','=',self.id),('promotion_product','=',True)])
            for line in sol:
                line.write({'promotion_product':False})
        name = promotion.promotion_product_id.name_get()[0][1]
        if promotion.promotion_product_id.description_sale:
            name += '\n' + promotion.free_product.description_sale
        values = {
                'order_id': self.id,
                'name': promotion.name,
                'product_uom_qty': 1,
                'product_uom': promotion.promotion_product_id.uom_id.id,
                'product_id':promotion.promotion_product_id.id,
                'price_unit': price_unit,
                'tax_id':[(6,0,promotion.promotion_product_id.taxes_id.ids)],
                'is_promotion': True,
            }
        if self.order_line:
            values['sequence'] = self.order_line[-1].sequence + 1
        sol = SaleOrderLine.sudo().create(values)
        return sol
        
class SaleorderLine(models.Model):
    _inherit = 'sale.order.line'

    is_promotion = fields.Boolean(string="Is a Promotion", default=False,copy=False)
    promotion_product = fields.Boolean(string="Is a Free Promotion Product",default=False,copy=False)
   
    @api.depends('product_id','product_uom_qty')
    def onchange_promotion_order_line(self):
        promoline=self.env['sale.order.line'].search([('order_id','=',self.order_id.id),('is_promotion','=',True)]).write({'price_unit':0.0,'product_uom_qty':0.0})
        self.order_id.write({'promotion_id':False})
        return {}

class SaleReport(models.Model):

    _inherit = 'sale.report'
    coupon_code = fields.Char("Coupon code")
    
    def _select(self):
        res=super(SaleReport,self)._select()
        res=res+",s.coupon_code as coupon_code"
        return res
    
    def _group_by(self):
        res=super(SaleReport,self)._group_by()
        res=res+",s.coupon_code"
        return res    
    