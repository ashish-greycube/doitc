# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": "Serial No",
			"fieldname": "serial_no",
			"fieldtype": "Link",
			"options": "Serial No",
			"width": 300
		},
		{
			"label": "Employee No",
			"fieldname": "employee_no",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 300
		},
		{
			"label": "Employee Name",
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 300
		},
		{
			"label": "Item Name",
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 300
		},
		{
			"label": "Conditions",
			"fieldname": "conditions",
			"fieldtype": "Select",
			"options": "\nNew\nUsed",
			"width": 300
		}
	]
	return columns

def get_data(filters):
	conditions = get_conditions(filters)
	serial_no_data = frappe.db.sql("""
						SELECT
							name as serial_no,
							custom_custody_with as employee_no,
							custom_custody_with_name as employee_name,
							item_code as item_name,
							custom_item_condition as conditions
						FROM
							`tabSerial No`
						WHERE 
							docstatus = 0 {0}
					""".format(conditions),as_dict=True)
	return serial_no_data

def get_conditions(filters):
	conditions = ""
	if filters.get("employee"):
		conditions += " AND custom_custody_with = '{0}'".format(filters.get("employee"))
	if filters.get("serial_no"):
		conditions += " AND name = '{0}'".format(filters.get("serial_no"))
	if filters.get("project"):
		conditions += " AND custom_project = '{0}'".format(filters.get("project"))
	return conditions