# 🧪 Aloha Browser Smoke & Functional Test Framework

This project provides an automated testing framework for **Aloha Browser (Windows Desktop)**, focusing on **smoke and functional testing** scenarios such as **tab handling**, **startup behavior**, and **UI interaction**.  

---

## ✨ Key Features

- ✅ Automated startup of Aloha Browser with remote debugging enabled  
- 🌐 Playwright CDP connection for web context automation (tabs, navigation, screenshots)  
- 🖱 Pywinauto integration for desktop-level interaction and validation  
- 🧭 Smoke tests verifying core tab open/close/focus flows  
- 📝 Structured logging per test for easy debugging  
- 📸 Automatic screenshot capture on failure with HTML reporting support

---

## ⚡ Setup & Installation

### 1. Allow PowerShell Execution (if needed)

- set the variables in conftest.py

- set execution script policy if needed
```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```
- Run
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt



.\run_test.ps1
```

---

## View reports
Open report/