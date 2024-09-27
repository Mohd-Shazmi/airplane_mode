# Copyright (c) 2024, Shazam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airport(Document):
	def before_save(self):
		total_shops = frappe.db.count("Airport Shops", {"airport": self.name})
		curr_leased = frappe.db.count("Airport Shops", {
            "airport": self.name,
            "tenant": ["!=", ""]
        })
		self.leased = curr_leased
		self.number_of_shops = total_shops
		self.available = self.number_of_shops - self.leased
