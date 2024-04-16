// Copyright (c) 2024, TTSP and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Device", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Device", {
	// refresh(frm) {
             
	// },
    get_status: function(frm) {
        frappe.call({
            method: "aba.biometric_attendance.doctype.device.api.device_status", 
            args: {
                userName: frm.doc.user_name,
                password: frm.doc.password,
                ip: frm.doc.ip_address
            },
            callback: function(r) {
                frappe.msgprint(r['message'])
                frm.set_value('status',r['message'])
            }
        });
	}
});
