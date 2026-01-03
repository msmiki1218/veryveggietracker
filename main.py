import webview
import sys
import os
from threading import Thread
from app import app

def start_flask():
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=False)

if __name__ == '__main__':
    t = Thread(target=start_flask)
    t.daemon = True
    t.start()

    webview.create_window('Very Veggie Tracker', 'http://127.0.0.1:5000', width=1000, height=800)
    webview.start()