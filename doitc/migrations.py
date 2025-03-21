import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_migrations():
    create_custom_fields_in_core_doctype()

def create_custom_fields_in_core_doctype():
    custom_fields = {
        "Employee Checkin": [
            dict(
                fieldname="custom_employee_attendance_request_reference",
                label="Employee Attendance Request Reference",
                fieldtype="Link",
                options="Employee Attendance Request DT",
                insert_after="skip_auto_attendance",
                is_custom_field=1,
                is_system_generated=0, 
                translatable=0,
                no_copy=1
            )
        ],

        "Company": [
            dict(
                fieldname="custom_default_leave_without_pay",
                label="Default Leave Without Pay",
                fieldtype="Link",
                options="Leave Type",
                insert_after="parent_company",
                is_custom_field=1,
                is_system_generated=0, 
                translatable=0,
                no_copy=1
            )
        ],

        "HR Settings": [
            dict(
                fieldname="custom_permission_balance_per_month",
                label="Permission Balance Per Month",
                fieldtype="Int",
                insert_after="retirement_age",
                description="In Hrs",
                is_custom_field=1,
                is_system_generated=0, 
                translatable=0,
                no_copy=1
            )
        ],

        "Employee": [
            dict(
                fieldname="custom_available_permission_balance",
                label="Available Permission Balance",
                fieldtype="Int",
                insert_after="employee_name",
                description="In Hrs",
                is_custom_field=1,
                is_system_generated=0, 
                translatable=0,
                no_copy=1
            )
        ],

        "Project" : [
            {
                'fieldname' : 'custom_actual_cost',
                'fieldtype' : 'Currency',
                'label' : 'Actual Cost',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'estimated_costing'
            },
            {
                'fieldname' : 'custom_net_profit',
                'fieldtype' : 'Float',
                'label' : 'Net Profit',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'custom_actual_cost'
            },
            {
                'fieldname' : 'custom_profit_percentage',
                'fieldtype' : 'Percent',
                'label' : 'Profit Percentage',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'custom_net_profit'
            }
        ],
        "Sales Order Item" : [
            {
                'fieldname' : 'custom_profit_percent',
                'fieldtype' : 'Percent',
                'label' : 'Profit (%)',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'net_amount'
            }
        ],
        "Purchase Order" : [
            {
                'fieldname' : 'custom_po_type',
                'fieldtype' : 'Link',
                'options' : 'PO Type DT',
                'label' : 'PO Type',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'schedule_date',
            }
        ]
    }
    print("Creating custom fields for app Doitc:")
    for dt, fields in custom_fields.items():
        print("*******\n %s: " % dt, [d.get("fieldname") for d in fields])
    create_custom_fields(custom_fields)
