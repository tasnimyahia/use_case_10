from odoo import api, fields,models,_
from odoo.exceptions import ValidationError

class MedicineFeature(models.Model):
    _inherit="product.template"
    
    max_qty_per_invoice=fields.Integer(string='Max Qty per Invoice',default=0)
    classification=fields.Selection(
        [('is_medicine','Medicine'),
        ('not_medicine','Not Medicine')],
        required=True
        )
    
    is_medicine = fields.Boolean(
        string='Is Medicine',
        compute='_compute_is_medicine',
        store=False,
    )

    low_stock_limit = fields.Integer(
        string='Low Stock Limit',
        default=0,
        help='IT will work when product reach low limit'
    )
    max_qty_when_low = fields.Integer(
        string='Max Qty per Invoice When Low',
        default=0,
        help='Max quantity when stock is low'
    )
    
    @api.depends('classification')
    def _compute_is_medicine(self):
        for rec in self:
            rec.is_medicine = rec.classification == 'is_medicine'
            
    @api.constrains('max_qty_per_invoice')
    def _check_max_qty_per_invoice_positive(self):
        
        for rec in self:
            if rec.max_qty_per_invoice < 0:
                raise ValidationError(
                    _('Max Qty per Invoice cannot be negative for product "%s". '
                    'Use 0 to disable the restriction.') % rec.name
                )
                
    @api.constrains('max_qty_when_low', 'max_qty_per_invoice')
    def _check_uc11_less_than_uc10(self):
        for rec in self:
            if (rec.max_qty_per_invoice > 0
                    and rec.max_qty_when_low > 0
                    and rec.max_qty_when_low > rec.max_qty_per_invoice):
                raise ValidationError(
                    _('Max Qty When Low (UC-11) = %d it must be less than or equal'
                      'Max Qty per Invoice (UC-10) = %d for medicine "%s".')
                    % (rec.max_qty_when_low, rec.max_qty_per_invoice, rec.name)
                )