// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Order DT', {
	refresh: function(frm) {
		frm.set_query('account', function () {
			return{
			 filters : {
				is_group : 0,
			  }
			};
		});
	},

	beneficiary_type: function(frm) {
		console.log(frm.doc.beneficiary_type);
		if (frm.doc.beneficiary_type == "Supplier" || frm.doc.beneficiary_type == "Employee"){
			console.log("IN CONDITION")
			frm.set_value("beneficiary_link", frm.doc.beneficiary_type);
		}
	},

	benificiary_name: function(frm) {
		if (frm.doc.beneficiary_type == "Supplier"){
			frappe.db.get_value('Supplier', frm.doc.benificiary_name, ['custom_account_number','custom_bank_name'])
				.then(r => {
				let values = r.message;
				console.log(values.custom_account_number)
				frm.set_value("account_no", values.custom_account_number);
				frm.set_value("bank_name", values.custom_bank_name);
			});
		}
		if (frm.doc.beneficiary_type == "Employee"){
			frappe.db.get_value('Employee', frm.doc.benificiary_name, ['bank_name','iban'])
				.then(r => {
				let values = r.message;
				console.log(values.custom_account_number)
				frm.set_value("account_no", values.iban);
				frm.set_value("bank_name", values.bank_name);
			});
		}
	}
});
