# 🛡️  –  ECHOTRACE - Windows Security 
Created by Jonathan Ehlinger 2025
A modern, lightweight, and interactive desktop app built with Python and PyQt6 to analyze, visualize, and manage your Windows 11 system’s security state — in real time.

---

## 🔍 Key Features

| Category             | Feature Description                                                                 |
|----------------------|--------------------------------------------------------------------------------------|
| **Account Discovery**| Detects logged-in accounts from Chrome, Edge, Firefox, Microsoft, GitHub Desktop    |
| **Saved Data Audit** | Scans saved credentials, autofill data, addresses, cookies                          |
| **Malware Scanner**  | Detects suspicious scripts (keyloggers, background processes) in common directories |
| **Autorun Viewer**   | Lists all startup programs (registry, shell:startup, tasks)                         |
| **Snapshot System**  | Captures full security state (apps, accounts, data) with timestamps                 |
| **Change Tracker**   | Compares system state across dates to detect new apps or data                       |
| **Live Alerts**      | Visual or system tray notifications for new logins, keylogger activity, etc.       |
| **Modern UI**        | Dark/light theme toggle, resizable layout, animated panels, high-DPI ready          |
| **Accessibility**    | Keyboard nav, screen reader support, color contrast options                         |

---

## 🖼️ GUI Preview

_Preview screenshots of each module will be added soon_

---

## 💾 Installation

### Requirements
- Python 3.10+
- Windows 11
- Administrator privileges

### Install via Git

```bash
git clone https://github.com/YOUR-USERNAME/winprotectpy.git
cd winprotectpy
pip install -r requirements.txt
python main.py
