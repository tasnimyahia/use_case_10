from odoo import models, fields

class MaxQtyLog(models.Model):
    _name = 'max.qty.log'
    _description = 'Max Quantity'

    user_id = fields.Many2one('res.users', string="User")
    product_id = fields.Many2one('product.template', string="Product")
    attempted_qty = fields.Float("Attempted Qty")
    allowed_qty = fields.Float("Allowed Qty")
    date = fields.Datetime("Date", default=fields.Datetime.now)
    note = fields.Char("Note")