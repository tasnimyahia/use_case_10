
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError


from odoo import models, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_uom_qty')
    def check_max_qty(self):
        for line in self:
            product = line.product_id.product_tmpl_id

            if product.max_qty_per_invoice and line.product_uom_qty > product.max_qty_per_invoice:

                # check if user is manager
                if not self.env.user.has_group("pharmacy_application.manager_group_id"):
                    raise ValidationError("Not allowed you are not a manager !!")
                else:
                    # allow but log
                    self.env['max.qty.log'].create({
                        'user_id': self.env.user.id,
                        'product_id': product.id,
                        'attempted_qty': line.product_uom_qty,
                        'allowed_qty': product.max_qty_per_invoice,
                    })
                    return {
                    'warning': {
                        'title': 'Warning',
                        'message': f'You exceeded max qty ({product.max_qty_per_invoice}) but you are allowed as manager.'
                    }
                }
    @api.constrains('product_uom_qty')
    def check_low_stock_qty(self):
        for line in self:
            product = line.product_id.product_tmpl_id

            # UC-11 فعّال؟
            if not product.low_stock_limit or not product.max_qty_when_low:
                continue

            # جيب المخزون الحالي
            current_stock = line.product_id.qty_available

            # المخزون وصل للحد الأدنى؟
            if current_stock > product.low_stock_limit:
                continue  # مخزون كويس — مفيش قيد

            # المخزون منخفض — هل الكمية بتعدي الحد؟
            if line.product_uom_qty > product.max_qty_when_low:
                # سجّل الحدث
                self.env['max.qty.log'].create({
                    'user_id': self.env.user.id,
                    'product_id': product.id,
                    'attempted_qty': line.product_uom_qty,
                    'allowed_qty': product.max_qty_when_low,
                    'note': f'UC-11: Quantity is LOW({current_stock} current stock)',
                })
                # Soft warning — مش hard block
                # الكاشير يقدر يكمل بعد التحذير
                return {
                    'warning': {
                        'title': _(' Warning - Low Stock!! '),
                        'message': _(
                            'Current Stock for "%s" Low (%d  Medicine).\n'
                            ' The good limit for this stock is     %d unit.\n'
                            ' Do You want to continue !! '
                        ) % (
                            product.name,
                            current_stock,
                            product.max_qty_when_low,
                        ),
                    }
                }