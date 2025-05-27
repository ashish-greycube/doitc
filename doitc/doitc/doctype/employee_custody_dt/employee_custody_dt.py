# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form
from frappe import _

class EmployeeCustodyDT(Document):
	def on_submit(self):
		if len(self.items)>0:
			for item in self.items:
				if item.serial_no:
					serial_no_doc = frappe.get_doc("Serial No", item.serial_no)
					serial_no_doc.custom_custody_with = self.employee_no
					serial_no_doc.custom_project = item.project
					serial_no_doc.add_comment("Comment",text=_("Custody assigned to employee: {0} due to {1}".format(self.employee_name, get_link_to_form("Employee Custody DT",self.name))))
					serial_no_doc.save(ignore_permissions=True)
					frappe.msgprint(_("Custody is updated for Serial No: {0} to Employee: {1}".format(item.serial_no, self.employee_name)), alert=True)

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_serial_no(doctype, txt, searchfield, start, page_len, filters):
	item_name = filters.get("item_name")
	serial_no_list = frappe.db.get_all("Serial No",
									filters={"item_code": item_name, "name": ("like", f"%{txt}%")},
									fields=["name"],as_list=True)
	return serial_no_list
	