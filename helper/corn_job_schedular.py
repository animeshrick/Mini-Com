#!/usr/bin/env python3
"""
Email Scheduler with Cron Jobs
Sends emails weekly (every Monday at 9 AM) and every 25 minutes
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import threading
import time
import os

import requests
from dotenv import load_dotenv

from helper.helper_log import onion

load_dotenv()
# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("EMAIL_HOST_USER")
RECIPIENT_EMAIL = os.environ.get("EMAIL_HOST_USER")
SENDER_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


def send_email(subject, body):
    """Send an email with the given subject and body"""
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = RECIPIENT_EMAIL
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Create SMTP session
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        print(f"✓ Email sent successfully at {datetime.now()}")
        print(f"  Subject: {subject}")
        return True

    except Exception as e:
        print(f"✗ Error sending email: {e}")
        return False


def send_weekly_email(RECIPIENT_EMAIL):
    """Send the weekly email"""
    subject = "Weekly Report"
    body = f"""
Hello,

This is your automated weekly email report.

Week ending: {datetime.now().strftime('%Y-%m-%d')}

Best regards,
Automated Email System
    """
    send_email(subject, body, RECIPIENT_EMAIL)


def get_next_monday_9am():
    """Calculate the next Monday at 9:00 AM"""
    now = datetime.now()
    days_ahead = 0 - now.weekday()  # Monday is 0

    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7

    next_monday = now + timedelta(days=days_ahead)
    next_monday = next_monday.replace(hour=9, minute=0, second=0, microsecond=0)

    # If it's Monday but past 9 AM, schedule for next Monday
    if now.weekday() == 0 and now.hour >= 9:
        next_monday += timedelta(days=7)

    return next_monday


def call_render_api():
    """Call the API and print the response"""
    url = "https://mini-com-ngdx.onrender.com/api/product/all_product"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # If JSON, parse and show summary
        data = response.json()
        onion(file="call_render_api",message=f"✅ API call successful at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Data--> {list(data.keys()) if isinstance(data, dict) else 'Non-JSON response'}")

    except Exception as e:
        onion(file="call_render_api_Exception",message=f"❌ Error fetching data: {e}",level="error")
        print("-" * 80)


def run_25min_scheduler():
    """Run the 25-minute interval API scheduler"""
    print("⏰ 25-minute scheduler started")

    while True:
        try:
            call_render_api()
            next_run = datetime.now() + timedelta(minutes=25)
            onion(file="run_25min_scheduler", message=f"Next API call scheduled at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}\n")
            time.sleep(25 * 60)  # Wait 25 minutes
        except Exception as e:
            onion(file="run_25min_scheduler_Exception", message=f"Error in run_25min_scheduler: {e}", level="error")

            time.sleep(60)  # Retry after 1 minute


def run_weekly_scheduler():
    """Run the weekly email scheduler"""
    print("⏰ Weekly scheduler started")
    while True:
        try:
            next_run = get_next_monday_9am()
            wait_seconds = (next_run - datetime.now()).total_seconds()


            # Wait until next Monday at 9 AM
            time.sleep(wait_seconds)

            # Send the email
            send_weekly_email()

        except Exception as e:
            onion(file="run_weekly_scheduler_Exception",message=f"Error in weekly scheduler: {e}",level="error")
            time.sleep(3600)  # Wait 1 hour before retrying


def main():

    # Create and start threads for both schedulers
    thread_25min = threading.Thread(target=run_25min_scheduler, daemon=True)
    thread_weekly = threading.Thread(target=run_weekly_scheduler, daemon=True)

    thread_25min.start()
    thread_weekly.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        onion(file="main_exception_KeyboardInterrupt",message=f"Scheduler stopped by user at ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",level="KeyboardInterrupt")


if __name__ == "__main__":
    main()