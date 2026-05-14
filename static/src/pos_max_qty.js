/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/store/models";

patch(Orderline.prototype, {

    set_quantity(quantity) {
        const product = this.product;

        if (product.max_qty_per_invoice && quantity > product.max_qty_per_invoice) {

            this.env.services.popup.add({
                title: "Warning",
                body: `Max allowed is ${product.max_qty_per_invoice}`,
            });

            return; // block
        }

        return super.set_quantity(...arguments);
    },

});