# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form
from frappe import _

class EmployeeCustodyReturnDT(Document):
	def on_submit(self):
		if len(self.items) > 0:
			for item in self.items:
				if item.serial_no:
					serial_no_doc = frappe.get_doc("Serial No", item.serial_no)
					serial_no_doc.custom_custody_with = ""
					serial_no_doc.custom_custody_with_name = ""
					serial_no_doc.custom_project = ""
					serial_no_doc.add_comment("Comment", text=_("Custody returned by employee: {0} due to {1}".format(self.employee_name, get_link_to_form("Employee Custody Return DT",self.name))))
					serial_no_doc.save(ignore_permissions=True)
					frappe.msgprint(_("Custody is updated for Serial No: {0} from Employee: {1}".format(item.serial_no, self.employee_name)), alert=True)
	
	@frappe.whitelist()
	def fetch_custody_details_of_employee(self):
		if self.employee_no:
			serial_no_list = frappe.db.sql("""
							SELECT
								name,
								item_code,
								description,
								custom_item_condition,
								custom_project
							FROM
								`tabSerial No`
							WHERE
								custom_custody_with = '{0}'
						""".format(self.employee_no), as_dict=True)
			print("Serial No List: ", serial_no_list)
			# if len(serial_no_list) > 0:
			# 	for item in serial_no_list:
			# 		# employee_custody_list = frappe.db.get_all("Employee Custody DT",
			# 		# 	filters={"employee_no": self.employee_no, "docstatus":1},
			# 		# 	fields=["name", "employee_no", "employee_name"],debug=1)
			# 		employee_custody_list = frappe.db.sql("""
			# 					SELECT
			# 						eci.project
			# 					FROM
			# 						`tabEmployee Custody DT` ec
			# 					INNER JOIN `tabEmployee Custody Item Details DT` eci ON
			# 						ec.name = eci.parent
			# 					WHERE
			# 						ec.employee_no = '{0}' AND eci.serial_no = '{1}' AND eci.item_name = '{2}
			# 						AND ec.docstatus = 1
			# 				""".format(self.employee_no, item.name, item.item_code), as_dict=True)
			# 		if len(employee_custody_list) > 0:
			# 			item.update({"project": employee_custody_list[0].project})
			# 		else :
			# 			employee_custody_transfer_list = frappe.db.sql("""
			# 					SELECT
			# 						ectd.project
			# 					FROM
			# 						`tabEmployee Custody Transfer Details DT` ectd
			# 					WHERE
			# 						ectd.to_employee = '{0}' AND ectd.serial_no = '{1}' AND ectd.item_name = '{2}'
			# 						AND ect.docstatus = 1
			# 				""".format(self.employee_no, item.name, item.item_code), as_dict=True)
			# 			if len(employee_custody_transfer_list) > 0:
			# 				item.update({"project": employee_custody_transfer_list[0].project})

			return serial_no_list
					
