import frappe
from frappe.utils import today
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_payment_order(source_name,target_doc = None):
    doc = get_mapped_doc(
        "Payment Request Eqo",
        source_name,
        {
            "Payment Request Eqo": {"doctype" : "Payment Order DT", "field_map" : {"total_payment_request_amount": "amount", "cost_center" : "cost_center", "custom_user_remark": "user_remark","party_no":"employee_no","party_name":"employee_name"} }
        },
        target_doc
    )
    return doc

@frappe.whitelist()
def set_available_permission_balance_every_month_in_employee():
    allocated_permission_balance = frappe.db.get_single_value("HR Settings", "custom_permission_balance_per_month")
    employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])
    for employee in employees:
        emp_doc = frappe.get_doc("Employee", employee.name)
        emp_doc.custom_available_permission_balance = allocated_permission_balance
        emp_doc.add_comment("Comment", "Available Permission Balance is reset to {0} on {1} by system".format(allocated_permission_balance,today()))
        emp_doc.save(ignore_permissions=True)