import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_payment_order(source_name,target_doc = None):
    doc = get_mapped_doc(
        "Payment Request Eqo",
        source_name,
        {
            "Payment Request Eqo": {"doctype" : "Payment Request Eqo", "field_map" : {"total_payment_request_amount": "amount", "cost_center" : "cost_center", "user_remark": "user_remark"} }
        },
        target_doc
    )
    return doc