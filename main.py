import webview
import sys
import os
import time
from threading import Thread
from app import app

# This helper function finds the internal path for PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def start_flask():
    # host 0.0.0.0 is sometimes safer for internal app communication
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=False)

if __name__ == '__main__':
    # 1. Start Flask in a background thread
    t = Thread(target=start_flask)
    t.daemon = True
    t.start()

    # 2. WAIT a moment to let the server boot before the window pops up
    time.sleep(1.5) 

    # 3. Launch the window
    webview.create_window('Very Veggie Tracker', 'http://127.0.0.1:5000', width=1000, height=800)
    webview.start()