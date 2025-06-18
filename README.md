# Student-Activity-Monitoring-Ai

# Realtime Student Activity Monitoring with AI – Powered in Computer Labs

🚀 A smart and AI-enhanced Python system for monitoring student activity in computer labs. It tracks keystrokes, application usage, and unauthorized software behavior in real-time. The system automatically generates reports and sends alerts via email to educators, helping maintain a productive and focused digital learning environment.

---

## 📌 Project Description

This project uses Python-based automation and machine learning to monitor and analyze students' digital activity on lab systems. It focuses on:
- Capturing keystrokes
- Logging and visualizing application usage
- Detecting and reporting unauthorized activities
- Predicting the next likely application to be used using a machine learning model
- Sending email alerts with logs and visual reports to the class teacher

> 🧠 Ideal for maintaining discipline, preventing digital distractions, and ensuring responsible use of lab systems.

---

## 🎯 Key Features

✅ Keystroke logging  
✅ Application usage tracking and visualization  
✅ Blocking/unblocking distracting websites  
✅ RandomForest-based app usage prediction  
✅ Automated email alerts with logs and reports  
✅ Detailed documentation & presentation attached

---

## 🧠 AI Module

A `RandomForestClassifier` model is trained on synthetic application usage data:
- Features: Hour of the day and last used application index
- Target: Next likely application to be used
- Used for intelligent predictions and behavior pattern analysis

---

## 🧾 File Overview

| File Name               | Purpose |
|------------------------|---------|
| `main.py`              | Starts the keystroke logger and app monitor |
| `lock.py`              | Blocks access to specific distracting websites |
| `unlock.py`            | Unblocks websites for normal browsing |
| `usage.py`             | Generates usage report + trains ML model + sends email |
| `Requirements.txt`     | Required Python packages |
| `tempCodeRunnerFile.py`| Temp file used during testing |
---

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/student-activity-monitoring-ai.git
cd student-activity-monitoring-ai
```

2. Install required packages:
```bash
pip install -r Requirements.txt
```

> 💡 Admin privileges may be needed to block/unblock websites.

---

## ⚙️ How to Run

### ▶️ Run Full Monitoring System
```bash
python main.py
```

### 📊 Generate Usage Report + Predict Next App + Send Email
```bash
python usage.py
```

---

## 🧠 Machine Learning - App Prediction

- Uses a simulated dataset to predict which app the student might use next.
- Helps identify productivity trends and patterns.
- Built using `sklearn.ensemble.RandomForestClassifier`.

---

## 📤 Email Alerts

The system emails the class teacher:
- Application log (`application_log.txt`)
- Keystroke log (`keystroke_log.txt`)
- Usage graph (`app_usage_report.png`)
- Predicted next app & most used app

Make sure to configure your **Gmail App Password** in `usage.py` securely.

---

## 🖥️ Screenshots & Reports

Reports are saved as:
- `app_usage_report.png`: Graphical visualization
- HTML email with structured report

---

## 📁 Directory Structure

```
student-activity-monitoring-ai/
├── main.py
├── lock.py
├── unlock.py
├── usage.py
├── tempCodeRunnerFile.py
├── Requirements.txt
├── README.md
├── .gitignore
└── logs/
    ├── application_log.txt
    └── keystroke_log.txt
```

---

## 👨‍💻 Team Members

- **B. Rudrasena Reddy** (21G01A0513)  
- **K. Saiekshitha** (21G01A0539)  
- **K. Kalyan Choudary** (21G01A0548)  
- **M. Sai Venkat** (21G01A0551)  

Under the Guidance of:  
**Dr. B. Rama Ganesh, M.Tech, Ph.D, PDF.**  
Head of Department, CSE – SVPCET, Puttur

---

## 🏫 College

**Sri Venkatesa Perumal College of Engineering & Technology (SVPCET)**  
Puttur, Chittoor District, Andhra Pradesh

---

## 📚 Documentation

For detailed module explanations, UML diagrams, feature list, datasets, and literature survey, refer:
- 📄 `Project_documentation.pdf`
- 📊 `BatchA 12.pptx`
- For above files contact me via gmail. 

---

## 📄 License

This project is for academic use only. For commercial or deployment-related queries, please contact the authors.

My Gmail ID : b.rudrasenareedy@gmail.com
