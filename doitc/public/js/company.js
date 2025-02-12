frappe.ui.form.on("Company", {
    setup(frm){
        frm.set_query("custom_default_leave_without_pay", function() {
            return {
                filters: {
                    "is_lwp": 1
                }
            };
        });
    }
});