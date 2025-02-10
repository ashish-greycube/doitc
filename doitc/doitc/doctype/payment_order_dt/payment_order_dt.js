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
	}
});
