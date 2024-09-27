# Copyright (c) 2024, Shazam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, now


class ShiftTime(Document):
	def before_save(self):
		self.end_time = add_to_date(self.start_time, hours=self.duration_of_shift)
