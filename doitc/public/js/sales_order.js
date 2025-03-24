frappe.ui.form.on('Sales Order', {
    setup: function(frm) {
        frm.set_query("custom_cost_center", function() {
            return {
                "filters": {
                    "company": frm.doc.company
                }
            };
        });
    },
})

// Calculating Profit Percent in Sales Order Child Table
frappe.ui.form.on('Sales Order Item', {
    margin_rate_or_amount: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        let price_list_rate_amt = row.price_list_rate;

        setTimeout(() => {
            let margin_rate_amt = row.margin_rate_or_amount;
            let profit_percent = (margin_rate_amt / price_list_rate_amt) * 100
            
            frappe.model.set_value(cdt,cdn,"custom_profit_percent",profit_percent);
        }, 100);
    },

    price_list_rate: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        let price_list_rate_amt = row.price_list_rate;

        setTimeout(() => {
            let margin_rate_amt = row.margin_rate_or_amount;
            let profit_percent = (margin_rate_amt / price_list_rate_amt) * 100
            
            frappe.model.set_value(cdt,cdn,"custom_profit_percent",profit_percent);
        }, 100);
    }
})