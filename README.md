# ⏱ Circular Timer

> **Petrochemical Engineering – Open Source Software Engineering**
> Final Project | Group 08

![CI](https://github.com/YOUR_USERNAME/circular-timer/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

---

## 👥 Authors

| Name | Role |
|------|------|
| Ben Brahim Houssem Iheb | Developer |
| Draoui Ahcene Borhene | Developer |

**Group:** 08 | **Course:** Open Source Software Engineering

---

## 📌 Overview

A desktop **Circular Timer** application built with Python and Tkinter.  
Features a visual clock face, animated hand, color-coded countdown, and flexible duration selection.

---

## 🔧 Open Source Tools Used

| Tool | Purpose |
|------|---------|
| **Python 3** | Core programming language (open source) |
| **Tkinter** | GUI framework – included with Python stdlib |
| **pytest** | Automated unit testing |
| **GitHub Actions** | CI/CD pipeline |

---

## ✨ Features

- ▶ Start / ⏸ Pause / ⏹ Stop / ↺ Reset
- Duration selector: 30s · 60s · 90s · 120s
- Color-coded countdown: 🟢 → 🟡 → 🔴
- Progress bar
- Animated clock hand & arc
- Sound alert when time is up (Windows)

---

## 📁 Project Structure

```
circular-timer/
├── pr.py                        # Main application
├── requirements.txt             # Dependencies
├── README.md                    # Documentation
├── tests/
│   └── test_timer.py            # Unit tests (pytest)
└── .github/
    └── workflows/
        └── ci.yml               # GitHub Actions CI/CD
```

---

## 🚀 Getting Started

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/circular-timer.git
cd circular-timer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python pr.py

# 4. Run tests
pytest tests/ -v
```

---

## ⚙️ CI/CD

Every push to `main` automatically runs all tests via GitHub Actions.

---

## 📝 License

MIT License
