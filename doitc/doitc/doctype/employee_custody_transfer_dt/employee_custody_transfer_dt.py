# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form
from frappe import _

class EmployeeCustodyTransferDT(Document):
	# def validate(self):
	def on_submit(self):
		if len(self.employee_custody_transfer_details_dt)>0:
			for item in self.employee_custody_transfer_details_dt:
				if item.serial_no:
					serial_no_doc = frappe.get_doc("Serial No", item.serial_no)
					serial_no_doc.custom_custody_with = item.to_employee
					serial_no_doc.custom_custody_with_name = item.t_employee_name
					serial_no_doc.add_comment("Comment",text=_("Custody transferred to employee: {0} due to {1}".format(item.t_employee_name, get_link_to_form("Employee Custody Transfer DT",self.name))))
					serial_no_doc.save(ignore_permissions=True)
					frappe.msgprint(_("Custoday is updated for Serial No: {0} to Employee: {1}".format(item.serial_no, item.t_employee_name)),alert=True)
	@frappe.whitelist()
	def fetch_custody_details_of_employee(self):
		if self.employee_no:
			employee_custody_list = frappe.db.sql("""
								SELECT
									ec.employee_no as from_employee,
									ec.employee_name as from_employee_name,
									eci.item_name,
									eci.item_description,
									eci.serial_no,
									eci.item_condition,
									eci.note,
									eci.project
								FROM
									`tabEmployee Custody DT` ec
								INNER JOIN `tabEmployee Custody Item Details DT` eci ON
									ec.name = eci.parent
								WHERE
									ec.employee_no = '{0}'
									AND ec.docstatus = 1
							""".format(self.employee_no),as_dict=True)
			print("Employee Custody List: ", employee_custody_list)
			return employee_custody_list
