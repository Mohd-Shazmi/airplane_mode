# Copyright (c) 2024, Shazam and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            "fieldname": "airline",
            "label": "Airline",
            "fieldtype": "Link",
            "options": "Airline"
        },
        {
            "fieldname": "revenue",
            "label": "Revenue",
            "fieldtype": "Currency",
            "options": "AED",
        },
    ]

    # SQL query to get total revenue, but checking ticket count first
    data = frappe.db.sql("""
        SELECT
            airline.name AS airline,  -- Fetch airline name from Airline DocType
            COALESCE(SUM(at.total_amount), 0) AS revenue  -- Sum total_amount, or 0 if no tickets
        FROM
            `tabAirline` airline  -- Start from Airline table
        LEFT JOIN
            `tabAirplane` airplane ON airplane.airline = airline.name  -- Left join with Airplane
        LEFT JOIN
            `tabAirplane Flight` flight ON flight.airplane = airplane.name  -- Left join with Airplane Flight
        LEFT JOIN
            `tabAirplane Ticket` at ON at.flight = flight.name  -- Left join with Airplane Ticket
        GROUP BY
            airline.name  -- Group by airline name
        ORDER BY
            revenue DESC  -- Order by revenue (including 0) in descending order
    """, as_dict=True)

	# Calculate total revenue for all airlines
    total_revenue = sum(x['revenue'] for x in data)

	# Include a summary row for total revenue
    summary = [
        {
			"label": "Total Revenue",
            "value": frappe.format_value(total_revenue, 'Currency'),
            "color": "green"
		}
    ]

    # Creating a chart with the results
    chart = {
        "data": {
            "labels": [x['airline'] for x in data],
            "datasets": [{"values": [x['revenue'] for x in data]}],
        },
        "type": "donut",
    }

    # Return columns, data, message, chart, and no custom filters
    return columns, data, "Revenue Summary", chart, summary



