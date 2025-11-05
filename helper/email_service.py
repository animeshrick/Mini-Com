from django.utils import timezone
import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from helper.helper_log import onion
from order.export_types.order_types.export_order import ExportOrder
from asgiref.sync import sync_to_async


async def send_order_confirmation(user_email: str, user_name: str, order: ExportOrder):
    subject = f"Order Confirmation #{order.id}"
    context = {
        "user_name": user_name,
        "order_id": order.id,
        "items": order.ordered_items,
        "total": order.total_price,
    }

    html_message = await sync_to_async(render_to_string)("emails/order_confirmation.html", context)
    plain_message = strip_tags(html_message)

    # Run send_mail in a separate thread (non-blocking)
    await sync_to_async(send_mail)(
        subject,
        plain_message,
        None,
        [user_email],
        html_message=html_message,
    )

async def send_registration_confirmation(user_email: str):
    subject = "Welcome to Boi-Khata-Dukan"
    context = {}

    html_message = await sync_to_async(render_to_string)("emails/registration_welcome.html", context)
    plain_message = strip_tags(html_message)

    await sync_to_async(send_mail)(
        subject,
        plain_message,
        None,
        [user_email],
        html_message=html_message,
    )

    onion(file="send_registration_confirmation", message=f"user_email:{user_email}, Subject:{subject}, html_message:{html_message}, plain_message={plain_message}")

async def send_keep_alive_email():

    subject = "Live long Boi-Khata-Dukan"

    context = {
        "admin_name": "Onion",
        "admin_email": os.environ.get("EMAIL_HOST_USER"),
        "server_name": "MyApp Server",
        "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%SZ"),
        "status": "OK",
        "message": "Keep-alive ping sent successfully.",
        "status_url": "https://mini-com-ngdx.onrender.com/api/product/all_product?query=kitchen",
    }

    try:
        html_message = await sync_to_async(render_to_string)("emails/keep_alive.html", context)
        plain_message = strip_tags(html_message)

        await sync_to_async(send_mail)(
            subject,
            plain_message,
            None,
            [os.environ.get("EMAIL_HOST_USER")],
            html_message=html_message,
        )

        onion("keep_alive", f"Keep-alive email sent successfully at {context['timestamp']}")

    except Exception as e:
        onion("keep_alive", f"Failed to send keep-alive email: {str(e)}")