from odoo import models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields += ['low_stock_limit', 'max_qty_when_low', 'qty_available']
        return fields
    