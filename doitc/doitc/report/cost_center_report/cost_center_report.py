# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import cstr, flt

import erpnext
from erpnext.accounts.report.financial_statements import (
    filter_accounts,
    filter_out_zero_value_rows,
)
from erpnext.accounts.report.trial_balance.trial_balance import validate_filters

from erpnext.accounts.report.dimension_wise_accounts_balance_report.dimension_wise_accounts_balance_report import (
    get_dimensions,
    get_columns,
    accumulate_values_into_parents,
    prepare_data,
    format_gl_entries,
)

from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
    get_dimension_with_children,
)


def _set_gl_entries_by_account(dimension_list, filters, account, gl_entries_by_account):
    dimension = frappe.scrub(filters.get("dimension"))
    gl_entry = frappe.qb.DocType("GL Entry")
    gl_entry_account = frappe.qb.DocType("Account")
    query = (
        frappe.qb.from_(gl_entry)
        .inner_join(gl_entry_account)
        .on(gl_entry_account.name == gl_entry.account)
        .select(
            gl_entry.posting_date,
            gl_entry.account,
            gl_entry[dimension],
            gl_entry.debit,
            gl_entry.credit,
            gl_entry.is_opening,
            gl_entry.fiscal_year,
            gl_entry.debit_in_account_currency,
            gl_entry.credit_in_account_currency,
            gl_entry.account_currency,
            gl_entry_account.root_type,
        )
        .where(gl_entry.company == filters.company)
        .where(gl_entry.posting_date >= filters.from_date)
        .where(gl_entry.posting_date <= filters.to_date)
        .where(gl_entry.is_cancelled == 0)
        .where(gl_entry[dimension].isin(dimension_list))
        .orderby(gl_entry.account, gl_entry.posting_date)
    )

    if account:
        query = query.where(gl_entry.account.isin(account))

    if filters.get("include_default_book_entries"):
        default_finance_book = frappe.get_cached_value(
            "Company", filters.company, "default_finance_book"
        )
        query = query.where(gl_entry.finance_book == default_finance_book)

    # filter by dimensions
    accounting_dimensions = get_accounting_dimensions(as_list=False)
    if filters.get("cost_center"):
        accounting_dimensions.append(
            frappe._dict(
                {
                    "label": "Cost Center",
                    "fieldname": "cost_center",
                    "disabled": 0,
                    "document_type": "Cost Center",
                }
            )
        )
    for d in accounting_dimensions:
        if filters.get(d.fieldname):
            values = filters.get(d.fieldname)
            if frappe.get_cached_value("DocType", d.document_type, "is_tree"):
                values = get_dimension_with_children(
                    d.document_type, filters.get(d.fieldname)
                )
            query = query.where(gl_entry[d.fieldname].isin(values))

    gl_entries = query.run(as_dict=True)

    for entry in gl_entries:
        gl_entries_by_account.setdefault(entry.account, []).append(entry)
    print(gl_entries_by_account.get('401011002 - الخصم المسموح به على المبيعات - الخدمات المهنية - D'), "========================")

def _get_columns(dimension_list, filters=None):
    columns = get_columns(dimension_list)
    # hide columns if there is a filter selected for the report dimension
    selected_dim = frappe.scrub(filters.get("dimension"))
    dim_filter = [frappe.scrub(d) for d in filters.get(selected_dim)]
    if dim_filter:
        for c in columns:
            if not c["fieldname"] in dim_filter + [
                "account",
                "account_name",
                "total",
            ]:
                c["hidden"] = 1
    return columns


def execute(filters=None):

    validate_filters(filters)
    dimension_list = get_dimensions(filters)

    if not dimension_list:
        return [], []

    columns = _get_columns(dimension_list, filters)
    data = get_data(filters, dimension_list)
    columns, totals = get_total_row(columns, data, filters)
    
    leaf = frappe.db.sql("""
        SELECT name FROM `tabAccount` WHERE lft = rgt-1
    """, pluck = 'name')
    
    data = [d for d in data if d.get('account') in leaf]
    for d in data:
        d['indent'] = 0

    data.extend(totals)

    return columns, data


def get_data(filters, dimension_list):
    company_currency = erpnext.get_company_currency(filters.company)

    acc = frappe.db.sql(
        """
        select
            name, account_number, parent_account, lft, rgt, root_type,
            report_type, account_name, include_in_gross, account_type, is_group
        from
            `tabAccount`
        where
            company=%s
            order by lft""",
        (filters.company),
        as_dict=True,
    )

    if not acc:
        return None

    accounts, accounts_by_name, parent_children_map = filter_accounts(acc)

    min_lft, max_rgt = frappe.db.sql(
        """select min(lft), max(rgt) from `tabAccount`
        where company=%s""",
        (filters.company),
    )[0]

    account = frappe.db.sql_list(
        """select name from `tabAccount`
        where lft >= %s and rgt <= %s and company = %s and report_type = 'Profit and Loss'""",
        (min_lft, max_rgt, filters.company),
    )

    gl_entries_by_account = {}
    _set_gl_entries_by_account(dimension_list, filters, account, gl_entries_by_account)
    format_gl_entries(
        gl_entries_by_account,
        accounts_by_name,
        dimension_list,
        frappe.scrub(filters.get("dimension")),
    )

    # for _, dic in accounts_by_name.items():
    #     if dic.get("root_type") == "Income":
    #         for k in dic:
    #             if flt(dic[k]) < 0:
    #                 dic[k] = -1 * dic[k]

    accumulate_values_into_parents(accounts, accounts_by_name, dimension_list)
    out = prepare_data(accounts, filters, company_currency, dimension_list)
    out = filter_out_zero_value_rows(out, parent_children_map)

    return out




def get_total_row(columns, data, filters):
    income, expense = {}, {}
    for d in data:
        if d["account_name"] == "401 - الإيرادات":
            income = frappe._dict(d)
            income["account"] = "Total Revenue"
        elif d["account_name"] == "50 - المصاريف وتكلفة الإيرادات":
            expense = frappe._dict(d)
            expense["account"] = "Total Expense"

    pnl_totals = {
        "account": "Profit (Loss)", "indent": 0, "warn_if_negative": 1}

    for d in columns:
        if d.get("options") == "currency" and d.get("fieldtype") == "Currency":
            pnl_totals[d["fieldname"]] = income.get(d["fieldname"], 0) + expense.get(
                d["fieldname"], 0
            )
            if income.get(d["fieldname"], 0) < expense.get(d["fieldname"], 0):
                pnl_totals[d["fieldname"]] = -1 * pnl_totals[d["fieldname"]]
            
            if filters.get('hide_blanks') and not pnl_totals[d["fieldname"]]:
                d['hidden'] = 1

    return columns, [income, expense, pnl_totals]