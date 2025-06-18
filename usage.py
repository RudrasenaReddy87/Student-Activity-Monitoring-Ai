import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket

# Configuration
LOG_FILE = "application_log.txt"
KEYSTROKE_LOG = "keystroke_log.txt"
USER_NAME = socket.gethostname() 
EMAIL_ADDRESS = "rudraproje000@gmail.com"
EMAIL_PASSWORD = "yaqkonnbqonrgcxb"  # Use an App Password

# Function to plot application usage
def plot_app_usage():
    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return {}

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()

    if not logs:
        print("No application logs available.")
        return {}

    # Extract app names from the logs and count their occurrences
    app_counts = Counter(log.split(",")[1].strip().replace(".exe", "") for log in logs)

    # Generate a bar chart for app usage frequency
    plt.figure(figsize=(10, 6))
    plt.bar(app_counts.keys(), app_counts.values(), color='skyblue')
    plt.title("Application Usage Frequency")
    plt.xlabel("Applications")
    plt.ylabel("Usage Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("app_usage_report.png")
    plt.close()

    print("✅ Application usage report saved as 'app_usage_report.png'.")
    return app_counts

# Function to train the app prediction model
def train_app_prediction_model():
    # Simulated training data (replace with actual log data for better accuracy)
    # X = [hour_of_day, last_app_index]
    X = np.array([
        [9, 1], [10, 2], [11, 1], [12, 0], [14, 3],
        [15, 0], [16, 1], [18, 2], [20, 0], [21, 1]
    ])

    # Labels (the next app to be opened based on last_app_index)
    y = np.array([1, 0, 3, 2, 0, 1, 2, 3, 0, 1])

    # Create and train the Random Forest model
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

# Predict the next app
def predict_next_app(model, hour, last_app_index, app_mapping):
    # Predict the next app based on current hour and last app index
    prediction = model.predict([[hour, last_app_index]])[0]
    return app_mapping[prediction]

# Function to send an email with attachments and HTML body
def send_email(user_name, predicted_app, most_used_app):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = "recipient@example.com"
    msg['Subject'] = "Student Monitoring System Report"

    # HTML content
    html_content = f'''
    <html>
      <body>
        <h2>Student Monitoring Report</h2>
        <p><strong>User Name:</strong> {user_name}</p>
        <p><strong>Predicted Next App:</strong> {predicted_app}</p>
        <p><strong>Most Used App:</strong> {most_used_app}</p>
      </body>
    </html>
    '''

    msg.attach(MIMEText(html_content, 'html'))

    # Attach log files and report
    for file in [LOG_FILE, KEYSTROKE_LOG, "app_usage_report.png"]:
        if os.path.exists(file):
            with open(file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file)}",
            )
            msg.attach(part)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    print("📧 Email sent successfully.")

if __name__ == "__main__":
    # Step 1: Generate application usage report
    app_counts = plot_app_usage()

    # Step 2: Train the app prediction model
    model = train_app_prediction_model()

    # Define app mapping (index to popular app names without extension)
    app_mapping = {
        0: "Python",
        1: "Notepad",
        2: "Visual Studio Code",
        3: "Google Chrome"
    }

    # Example: Predict next app based on current time and last opened app
    current_hour = 14  # Current hour of the day
    last_app_index = 0  # Assuming last app was 'Python'
    predicted_app = predict_next_app(model, current_hour, last_app_index, app_mapping)

    # Identify the most used app
    most_used_app = max(app_counts, key=app_counts.get, default="Unknown")

    # Step 3: Send email
    send_email(USER_NAME, predicted_app, most_used_app)

    # Print the predicted next app with the popular name
    print(f"🔮 Predicted next app: {predicted_app}")
