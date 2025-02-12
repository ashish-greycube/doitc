// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Permission Request DT', {
	permission_at: function (frm) {
		let start_time = frm.doc.permission_at;
		let end_time = frm.doc.return_at;
		let absent_hrs = get_absent_hours(start_time, end_time);
		frm.set_value('absent_hours', absent_hrs);
	},
	return_at: function (frm) {
		let start_time = frm.doc.permission_at;
		let end_time = frm.doc.return_at;
		let absent_hrs = get_absent_hours(start_time, end_time);
		frm.set_value('absent_hours', absent_hrs);
	},
});

function get_absent_hours(start_time, end_time) {
	console.log(start_time, end_time, "start_time, end_time", typeof start_time, typeof end_time, "typeof start_time, typeof end_time", parseInt(start_time), parseInt(end_time), "parseInt(start_time), parseInt(end_time)", (parseInt(end_time) < parseInt(start_time)), "parseInt(end_time) < parseInt(start_time)", (start_time == end_time), "start_time == end_time", (end_time > start_time), "end_time > start_time");
	if ((parseInt(end_time) < parseInt(start_time)) || (start_time == end_time)) {
		frappe.throw(__("The return time should be after permitted time"))
	}
	if ((start_time && end_time) && (parseInt(end_time) > parseInt(start_time))) {
		console.log("---")
		let absent_hrs = end_time - start_time;
		return absent_hrs;
	}
}
