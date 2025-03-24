import frappe
import datetime
from frappe import _
from frappe.utils import today, add_to_date
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

# Function that fetch actual cost value from profitablity report.
@frappe.whitelist()
def get_actual_cost(company, cost_center, msg):
    from erpnext.accounts.report.general_ledger.general_ledger import execute
    
    from_date = add_to_date(datetime.datetime.now(), months = -13).strftime('%Y-%m-%d')
    
    to_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    account = frappe.db.get_value(
        doctype = "Company", 
        filters = {'name' : company},
        fieldname = ['custom_parent_account_for_actual_cost']
    )

    group_by = "Group by Voucher (Consolidated)"

    include_dimensions = 1

    include_default_book_entries = 1

    filters = frappe._dict({
        'company' : company,
        'account' : [account],
        'from_date': from_date,
        'to_date': to_date,
        'group_by' : group_by,
        'cost_center' : [cost_center],
        'include_dimensions' : include_dimensions,
        'include_default_book_entries' : include_default_book_entries
    })
    
    data = execute(filters)
   
    actual_cost_value = 0
    for d in data[1]:
        if d.get('account') == "'Closing (Opening + Total)'":
            actual_cost_value = d.get('balance')
    return actual_cost_value