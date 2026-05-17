/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/store/models";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog, ConfirmDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(Orderline.prototype, {

    async set_quantity(quantity) {
        const product = this.product;

        // ── UC-10: Hard Block ─────────────────────────────────
        if (product.max_qty_per_invoice > 0 
                && quantity > product.max_qty_per_invoice) {

            await this.env.services.dialog.add(AlertDialog, {
                title: _t("Hard Block — UC-10"),
                body: _t(
                    `    You can not sell more than ${product.max_qty_per_invoice} unit `
                    + ` "${product.display_name}" in one order`
                ),
            });

            return; // وقف تماماً
        }

        // ── UC-11: Soft Warning ───────────────────────────────
        const lowStockLimit = product.low_stock_limit || 0;
        const maxQtyWhenLow = product.max_qty_when_low || 0;
        const currentStock  = product.qty_available    || 0;

        if (lowStockLimit > 0
                && maxQtyWhenLow > 0
                && currentStock <= lowStockLimit
                && quantity > maxQtyWhenLow) {

            // Soft — بيسأل الكاشير يكمل ولا لا
            const confirmed = await this.env.services.dialog.add(ConfirmDialog, {
                title: _t("Warning Low Stock!! —   UC-11"),
                body: _t(
                    ` Current stock for "${product.display_name}" `
                    + `Low (${currentStock} avalibale unit ).\n`
                    + ` recommended limit ${maxQtyWhenLow} unit.\n`
                    + `Do YOu want to continue ${quantity} unit ?`
                ),
            });

            if (!confirmed) {
                return; // الكاشير اختار لا
            }
            // الكاشير اختار نعم → يكمل
        }

        return super.set_quantity(...arguments);
        // في POS console
        const product = pos.models['product.product'].getAll()[0]
        console.log(product.low_stock_limit)    // لازم يطلع رقم مش undefined
        console.log(product.max_qty_when_low)   // لازم يطلع رقم مش undefined
        console.log(product.qty_available)      // لازم يطلع رقم مش undefined
    },

});