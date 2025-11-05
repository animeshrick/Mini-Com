import asyncio
import threading
from helper.email_service import send_keep_alive_email
from helper.helper_log import onion


def start_scheduler():
    """Start scheduler after Django is ready."""
    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(scheduler_loop())

    def scheduler_loop():
        return _scheduler_main_loop(1320) # 22 minutes (1320 seconds)

    async def _scheduler_main_loop(interval):
        while True:
            await send_keep_alive_email()
            await asyncio.sleep(interval)

    # Run in background thread
    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()
    onion("keep_alive", "Scheduler started successfully.")
