// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Custody Transfer DT', {
	fetch_custody_details: function (frm) {
		if (frm.is_dirty() == true) {
			frappe.throw({
				message: __("Please save the form to proceed..."),
				indicator: "red",
			});
		}

		frm.clear_table("employee_custody_transfer_details_dt")
		frm.call("fetch_custody_details_of_employee").then(r => {
			if (r.message) {
				let employee_details = r.message
				employee_details.forEach(element => {
					let row = frm.add_child("employee_custody_transfer_details_dt");
					row.item_name = element.item_name;
					row.item_description = element.item_description;
					row.serial_no = element.serial_no;
					row.item_condition = element.item_condition;
					row.note = element.note;
					row.project = element.project;
					row.from_employee = element.from_employee;
					row.f_employee_name = element.from_employee_name;
				});
				refresh_field("employee_custody_transfer_details_dt");
			}
		})
	}
});
