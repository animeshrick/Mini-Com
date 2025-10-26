from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from order.export_types.order_types.export_order import ExportOrder


def send_order_confirmation(user_email:str, user_name: str, order: ExportOrder):
    subject = f"Order Confirmation #{order.id}"
    context = {
        "user_name": user_name,
        "order_id": order.id,
        "items": order.ordered_items,
        "total": order.total_price,
    }

    # Render HTML email from template
    html_message = render_to_string("emails/order_confirmation.html", context)
    plain_message = strip_tags(html_message)

    # Now, if you pass None for from_email, Django will automatically fall back to your
    # DEFAULT_FROM_EMAIL value from settings.py
    send_mail(
        subject,
        plain_message,
        None,
        [user_email],
        html_message=html_message,
    )
