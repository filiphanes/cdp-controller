# CDP server
This is simple python http proxy to chromium debugging port and html page, where you can:

- switch tabs
- open new tab
- close tabs

# Run

    chromium --remote-debugging-port=9222 --kiosk example.com
    python3 server.py

Then open 127.0.0.1:8000
