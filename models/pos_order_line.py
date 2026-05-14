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