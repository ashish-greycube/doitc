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
            ),
            {
                'fieldname' : 'custom_parent_account_for_actual_cost',
                'fieldtype' : 'Link',
                'label' : 'Parent Account For Actual Cost',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'custom_default_leave_without_pay',
                'options' : 'Account'
            },
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
        ],
        
        "Sales Order" : [
            {
                'fieldname' : 'custom_cost_center',
                'fieldtype' : 'Link',
                'options' : 'Cost Center',
                'label' : 'Cost Center',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'delivery_date',
            }
        ],

        "Serial No" : [
            {
                'fieldname' : 'custom_custody_details_section',
                'fieldtype' : 'Section Break',
                'label' : 'Custody Details',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'sales_order',
            },
            {
                'fieldname' : 'custom_custody_with',
                'fieldtype' : 'Link',
                'options' : 'Employee',
                'label' : 'Custody With',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'custom_custody_details_section',
            },
            {
                'fieldname' : 'custom_custody_with_name',
                'fieldtype' : 'Data',
                'label' : 'Custody With Name',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'custom_custody_with',
                'read_only' : 1,
                'fetch_from' : 'custom_custody_with.employee_name',
            },
            {
                'fieldname' : 'custom_custody_details_column_break',
                'fieldtype' : 'Column Break',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'custom_custody_with_name',
            },
            {
                'fieldname' : 'custom_item_condition',
                'fieldtype' : 'Select',
                'options' : '\nNew\nUsed',
                'label' : 'Item Condition',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'custom_custody_details_column_break',
            }
        ],

        "Item" : [
            {
                'fieldname' : 'custom_is_custody_item',
                'fieldtype' : 'Check',
                'label' : 'Is Custody Item',
                'is_system_generated' : 0,
                'is_custom_field' : 1,
                'insert_after' : 'include_item_in_manufacturing',
            }
        ]
    }
    print("Creating custom fields for app Doitc:")
    for dt, fields in custom_fields.items():
        print("*******\n %s: " % dt, [d.get("fieldname") for d in fields])
    create_custom_fields(custom_fields)
