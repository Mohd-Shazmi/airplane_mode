import frappe

def send_shop_rent_reminder_email():
    shops_with_tenants = frappe.get_all(
        "Airport Shops",
        filters={
            "airport": "Your Airport Name",  
            "tenant": ["!=", ""]
        },
        fields=["tenant"]
    )
    
    for shop in shops_with_tenants:
        tenant_email = frappe.db.get_value("Shop Tenants", shop.tenant, "email")

        if tenant_email:
            send_email_to_tenant(tenant_email)

def send_email_to_tenant(email):
    subject = "Airport Shop Lease Update"
    message = """
    <h3>Hello,</h3>
    <p>Here is an important update regarding your leased shop.</p>
    """
    
    # Send the email
    frappe.sendmail(
        recipients=[email],
        subject=subject,
        message=message
    )
    
    frappe.log(f"Email sent to {email}")