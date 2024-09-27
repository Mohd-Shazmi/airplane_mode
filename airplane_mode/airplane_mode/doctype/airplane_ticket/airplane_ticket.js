// Copyright (c) 2024, Shazam and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        let d = new frappe.ui.Dialog({
            title: 'Select Seat',
            fields: [
                {
                    label: 'Seat Number',
                    fieldname: 'seat_number',
                    fieldtype: 'Data'
                }
            ],
            size: 'small', // small, large, extra-large 
            primary_action_label: 'Assign',
            primary_action(values) {
                frm.set_value("seat", values.seat_number);
                frm.save();
                d.hide();
            }
        });

        frm.add_custom_button("Assign Seat", () => {
            d.show();
        }, "Actions")

        
 	},

    fetch_geolocation: async (frm) => {
		if (!navigator.geolocation) {
			frappe.msgprint({
				message: __("Geolocation is not supported by your current browser"),
				title: __("Geolocation Error"),
				indicator: "red",
			});
			hide_field(["geolocation"]);
			return;
		}

		frappe.dom.freeze(__("Fetching your geolocation") + "...");

		navigator.geolocation.getCurrentPosition(
			async (position) => {
				frm.set_value("latitude", position.coords.latitude);
				frm.set_value("longitude", position.coords.longitude);

				await frm.call("set_geolocation_from_coordinates");
				frm.dirty();
				frappe.dom.unfreeze();
			},
			(error) => {
				frappe.dom.unfreeze();

				let msg = __("Unable to retrieve your location") + "<br><br>";
				if (error) {
					msg += __("ERROR({0}): {1}", [error.code, error.message]);
				}
				frappe.msgprint({
					message: msg,
					title: __("Geolocation Error"),
					indicator: "red",
				});
			},
		);
    },
});
