import frappe
from frappe import _
from frappe.utils import today
import datetime
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
    from erpnext.accounts.report.profitability_analysis.profitability_analysis import execute
    
    based_on = "Cost Center"
    fiscal_year = frappe.db.get_value(
        doctype = "Fiscal Year", 
        filters = {'name' : datetime.datetime.now().strftime('%Y')},
        fieldname = ['name']
    )
    start_date = frappe.db.get_value(
        doctype = "Fiscal Year",
        filters = {'name' : datetime.datetime.now().strftime('%Y')},
        fieldname = ['year_start_date']
    )
    end_date = frappe.db.get_value(
        doctype = "Fiscal Year",
        filters = {'name' : datetime.datetime.now().strftime('%Y')},
        fieldname = ['year_end_date']
    )

    filters = frappe._dict({
        "company" : company,
        "based_on" : based_on,
        "fiscal_year" : fiscal_year,
        "from_date": start_date,
        "to_date": end_date,
    })

    data = execute(filters)

    actual_cost_value = 0
    for d in data[1]:
        if d.get('account') == cost_center:
            actual_cost_value = d.get('expense')

    return actual_cost_value

# Function that makes cost center mandatory at special stage of approval
@frappe.whitelist()
def validate_cost_center(self, method=None):
     if self.workflow_state in ['ينتظار موافقة المدير العام للمبيعات']:
            if self.custom_cost_center==None or self.custom_cost_center=="":
                frappe.throw(_("Please Select Cost Center"))