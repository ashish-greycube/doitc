// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Custody DT', {
	setup: function(frm) {
		frm.set_query("item_name","items", function() {
			return {
				filters : {
					"custom_is_custody_item": 1
				}
			}
		});
		frm.set_query("serial_no", "items", function (doc, cdt, cdn) {
            let row = locals[cdt][cdn];
            return {
                query: "doitc.doitc.doctype.employee_custody_dt.employee_custody_dt.get_serial_no",
                filters: {
                    item_name: row.item_name
                },
            };
        });
	}
});

frappe.ui.form.on("Employee Custody Item Details DT", {
	serial_no: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn]
		if (row.serial_no) {
			frappe.db.get_value("Serial No", row.serial_no, ["custom_item_condition"]).then(r => {
				if (r.message.custom_item_condition) {
					frappe.model.set_value(cdt, cdn, "item_condition", r.message.custom_item_condition)
				}
			})
		}
	}
})