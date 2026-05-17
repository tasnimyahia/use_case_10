# في pos_order_line.py
from odoo import api, models, _
from odoo.exceptions import ValidationError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def sync_from_ui(self, orders):
        # UC-10 و UC-11 Check قبل ما الأوردر يتحفظ
        for order in orders:
            for line in order.get('lines', []):
                line_vals = line[2]
                product = self.env['product.product'].browse(
                    line_vals.get('product_id')
                )
                qty = line_vals.get('qty', 0)
                tmpl = product.product_tmpl_id

                # ── UC-10: Hard Block ─────────────────────
                limit = tmpl.max_qty_per_invoice
                if limit > 0 and qty > limit:
                    raise ValidationError(
                    _(
                        'You cannot sell more than %d units of "%s" in a single invoice.'
                    ) % (limit, line.product_id.display_name)
                )

                # ── UC-11: Log ────────────────────────────
                low_limit = tmpl.low_stock_limit
                max_when_low = tmpl.max_qty_when_low
                current_stock = product.qty_available

                if (low_limit > 0
                        and max_when_low > 0
                        and current_stock <= low_limit
                        and qty > max_when_low):
                    self.env['max.qty.log'].create({
                        'user_id': self.env.user.id,
                        'product_id': tmpl.id,
                        'attempted_qty': qty,
                        'allowed_qty': max_when_low,
                        'note': f'UC-11 POS: Low Stock  ({current_stock} avalibale)',
                    })

        return super().sync_from_ui(orders)