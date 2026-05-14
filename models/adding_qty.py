
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