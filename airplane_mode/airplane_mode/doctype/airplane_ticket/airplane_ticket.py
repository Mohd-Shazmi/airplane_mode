# Copyright (c) 2024, Shazam and contributors
# For license information, please see license.txt

import random
import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def before_save(self):
		total_add_ons = 0

		for add_on in self.add_ons:
			total_add_ons += add_on.amount

		self.total_amount = self.flight_price + total_add_ons

	def validate(self):
		list = []

		for add_on in self.add_ons:
			if add_on.item not in list:
				list.append(add_on.item)
			else:
				self.add_ons.remove(add_on)
		
		curr_cap = frappe.get_value("Airplane Flight", self.flight, "current_capacity")
		flight = frappe.get_value("Airplane Flight", self.flight, "airplane")
		flight_cap = frappe.get_value("Airplane", flight, "capacity")

		if (curr_cap >= flight_cap):
			frappe.throw("The Flight is full! :(")
		
		seats = curr_cap + 1
		frappe.db.set_value("Airplane Flight", self.flight, "current_capacity", seats)

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("The passenger has not boarded!")

	##def before_insert(self):
	##	randInt = random.randint(0, 100)
	##	randLetter = random.choice("ABCDE")

	##	self.seat = f"{randInt}{randLetter}"

