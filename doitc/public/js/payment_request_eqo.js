frappe.ui.form.on('Payment Request Eqo', {
    refresh: function (frm) {
        if (!frm.is_new() && frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Create Payment Order'), function () {
                    frm.trigger("make_payment_order");
                });
        }
    },

    make_payment_order(frm) {
        frappe.model.open_mapped_doc({
            method: "doitc.api.make_payment_order",
            frm: frm,
        });
    },
})