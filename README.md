# Student-Activity-Monitoring-Ai

# Realtime Student Activity Monitoring with AI – Powered in Computer Labs

🚀 A smart monitoring system for educational labs that tracks student keystrokes, application usage, and unauthorized behavior using Python and AI. Alerts are automatically sent to teachers via email when violations occur.

## 📌 Features
- ⌨️ Keystroke Logging
- 🖥️ Application Usage Monitoring
- 🚫 Unauthorized App Detection
- 🔐 Website Blocking/Unblocking
- 📧 Automated Email Alerts
- 📊 AI-based Activity Prediction (Random Forest)
- 📈 Usage Graph Reports

## 🛠️ Technologies Used
- Python
- Pynput, Psutil
- Matplotlib, Scikit-learn
- Smtplib, Email
- Tkinter GUI

## 📁 Modules Overview
- `main.py`: Runs the full monitoring system
- `lock.py` / `unlock.py`: Blocks or unblocks distracting websites
- `usage.py`: Generates application usage reports and sends email reports
- `Requirements.txt`: Required packages

## 📦 Installation

```bash
pip install -r Requirements.txt
