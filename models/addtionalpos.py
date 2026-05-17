from odoo import api, models, _
from odoo.exceptions import ValidationError

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    @api.constrains('qty', 'product_id')
    def _check_max_qty_pos(self):
        for line in self:
            limit = line.product_id.product_tmpl_id.max_qty_per_invoice
            if limit > 0 and line.qty > limit:
                raise ValidationError(
                    _(
                        'You cannot sell more than %d units of "%s" in a single invoice.'
                    ) % (limit, line.product_id.display_name)
                )
                
    @api.constrains('qty', 'product_id')
    def _check_low_stock_qty_pos(self):
        for line in self:
            product = line.product_id.product_tmpl_id

            if not product.low_stock_limit or not product.max_qty_when_low:
                continue

            current_stock = line.product_id.qty_available

            if current_stock > product.low_stock_limit:
                continue

            if line.qty > product.max_qty_when_low:
                self.env['max.qty.log'].create({
                    'user_id': self.env.user.id,
                    'product_id': product.id,
                    'attempted_qty': line.qty,
                    'allowed_qty': product.max_qty_when_low,
                    'note': f'UC-11 POS: Low Stock  ({current_stock} avalibale)',
                })
                # POS مش بيدعم warning return — بنسجّل بس ومش بنوقف
                # الحجب الحقيقي بيتعمل من JS