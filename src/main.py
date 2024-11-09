import threading

from telegram_bot import run_bot_in_thread
from avito_parser import run_parser

# Create threads for each function
thread2 = threading.Thread(target=run_parser)
thread2.start()

run_bot_in_thread()

thread2.join()