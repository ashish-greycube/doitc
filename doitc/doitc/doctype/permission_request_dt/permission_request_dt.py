# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class PermissionRequestDT(Document):
	def validate(self):
		self.get_balance()

	def get_balance(self):
		# Get Employe No from Current Document
		emp_no = self.employee_no

		# Get Current Employee Data from the Employee Table
		doc = frappe.get_doc("Employee", emp_no)

		# Getting Current Available Permission Balance of that Employee
		cur_balance = doc.custom_available_permission_balance

		# Calculating Absent Hours
		absent_hrs = self.absent_hours

		if cur_balance < absent_hrs:
			frappe.throw(_("Your available permission balance is less than the current absent hours"))

		# Calculating Remaining Balance
		remaining_balance = cur_balance - absent_hrs
	
		# Updating the APB in Employee
		doc.custom_available_permission_balance = remaining_balance
		doc.save()

		# Displaying the message of Changes
		frappe.msgprint("Available Permission Balance is deducted in employee {0}".format(emp_no))

