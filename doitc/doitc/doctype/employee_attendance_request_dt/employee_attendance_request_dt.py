# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form, getdate, cstr, get_datetime, nowdate
from frappe.utils.data import get_date_str

class EmployeeAttendanceRequestDT(Document):
	
	def on_submit(self):
		self.create_employee_checkin()

	def create_employee_checkin(self):
		employee_checkin_doc = frappe.new_doc("Employee Checkin")
		employee_default_shift = frappe.db.get_value("Employee",self.employee_no,"default_shift")
		if not employee_default_shift:
			frappe.throw("Please set default shift in employee")

		employee_checkin_doc.employee = self.employee_no
		employee_checkin_doc.log_type = self.attendance_type
		employee_checkin_doc.time = get_datetime(get_date_str(self.date) + " " + cstr(self.request_time))
		
		employee_checkin_doc.custom_employee_attendance_request_reference = self.name
		employee_checkin_doc.save(ignore_permissions=True)
		frappe.msgprint(_("Employee Checkin is created <b>{0}</b>").format(get_link_to_form("Employee Checkin",employee_checkin_doc.name)),alert=True)
