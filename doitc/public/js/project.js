frappe.ui.form.on('Project', {

    onload_post_render: function (frm) {
        if ((frm.doc.sales_order)) {

            let sales_order_id = frm.doc.sales_order
            frappe.db.get_value('Sales Order', { 'name': sales_order_id }, ['custom_cost_center'])
                .then(records => {
                    let values = records.message;
                    frm.set_value('cost_center', values.custom_cost_center)
                })


            frappe.db.get_list('Sales Order Item', {
                fields: ['item_code', 'qty', 'price_list_rate'],
                filters: {
                    'parent': sales_order_id
                }
            }).then(records => {
                let estimated_cost = 0
                for (let item in records) {
                    let curr_amnt = (records[item].qty * records[item].price_list_rate)
                    estimated_cost += curr_amnt
                }
                frm.set_value('estimated_costing', estimated_cost)
            })


            frappe.db.get_value('Sales Order', { 'name': sales_order_id }, ['custom_cost_center', 'company'])
                .then(records => {
                    let cost_center = records.message.custom_cost_center;
                    let company = records.message.company

                    frappe.call({
                        method: "doitc.api.get_actual_cost",
                        args: {
                            "msg": "Hello",
                            "company": company,
                            "cost_center": cost_center,
                        },
                        callback: function (r) {
                            let total_sales_amount_value = frm.doc.total_sales_amount
                            let actual_cost = r.message
                            frm.set_value('custom_actual_cost', actual_cost);

                            let net_profit = (total_sales_amount_value - actual_cost)
                            frm.set_value('custom_net_profit', net_profit);

                            let profit_percent = (net_profit / total_sales_amount_value) * 100
                            frm.set_value('custom_profit_percentage', profit_percent);
                        }
                    })
                })
        }
    }
});