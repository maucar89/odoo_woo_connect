import odoo
from odoo import fields,models,api,_
from odoo.exceptions import ValidationError

class PromotionExtend(models.TransientModel):
    
    _name='promotion.extend'
    
    end_date = fields.Date('End Date', help="Ending date of promotion code",required=True)
    
    @api.multi
    def extend_promotion(self):
        '''
            This method use for extend end date of promotion.
        '''
        self = self.with_context(key='promotion_extend')
        promotion=self.env['promotion.method'].browse(self._context.get('active_ids'))
        promotion.write({'date_end':self.end_date})
        return True