// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Custody Return DT', {
	fetch_custody_details: function (frm) {
		if (frm.is_dirty() == true) {
			frappe.throw({
				message: __("Please save the form to proceed..."),
				indicator: "red",
			});
		}

		frm.clear_table("items")
		frm.call("fetch_custody_details_of_employee").then(r => {
			if (r.message) {
				let employee_details = r.message
				employee_details.forEach(element => {
					let row = frm.add_child("items");
					row.item_name = element.item_code;
					row.item_description = element.description;
					row.serial_no = element.name;
					row.item_condition = element.custom_item_condition;
					// row.note = element.note;
					row.project = element.custom_project
;
				});
				refresh_field("items");
			}
		})
	}
});
