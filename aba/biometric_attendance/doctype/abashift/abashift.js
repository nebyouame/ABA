// Copyright (c) 2024, TTSP and contributors
// For license information, please see license.txt

frappe.ui.form.on("ABAshift", {
	get_attendance: function(frm) {
        console.log(frm.doc)
        frappe.call({
            method: "aba.biometric_attendance.doctype.abashift.api1.update_absent_time_for_employees", 
            args: {
                device: frm.doc.device,
                start_date: frm.doc.start_date,
                end_date: frm.doc.end_date,
                start_time: frm.doc.start_time,
                end_time: frm.doc.end_time,
                time_to_wait: frm.doc.time_to_wait,
                has_exceptional_day: frm.doc.has_exceptional_day,
                e_day: frm.doc.e_day,
                e_start_time: frm.doc.e_start_time,
                e_end_time: frm.doc.e_end_time,
                e_time_to_wait: frm.doc.e_time_to_wait,
            },
            callback: function(r) {
                frappe.msgprint("Absent time set for all employees")
                // frm.set_value('status',r['message'])
            }
        });
	}
});
