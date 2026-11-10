# 💰 Personal Expense Tracker

A colourful web app built with **Streamlit** to track, visualise and understand your spending.

## ✨ Features
- Add expenses with date, category, payment method, description and amount
- Dashboard: total, average, top category and month-over-month change
- Monthly budget tracker with progress bar and warnings
- Charts: spending by category, daily spending, monthly trend
- Editable transactions table with search, category filter and delete
- Insights: biggest expense, average per day, projected month-end, weekday and payment-method breakdown
- Download your data as CSV
- Multiple currencies (₹, $, €, £)

---

## 🤔 What happens when you run it?
The app is a Python program. Running it starts a small server on **your own computer**, and your browser shows it as a web page. Nothing is uploaded anywhere, and your data stays on your PC.

---

## 🚀 How to Run (Windows, step by step)

### Step 1: Install Python (one time only)
1. Download Python from https://www.python.org/downloads/
2. Run the installer and **tick "Add Python to PATH"** at the bottom of the first screen.
3. Click **Install Now**.

To check it worked, open **PowerShell** and type:
```
python --version
```
You should see a version number like `Python 3.12.x`.

### Step 2: Download this project
Choose **one** of these two ways.

**Option A: Download ZIP (easiest, no Git needed)**
1. On this GitHub page, click the green **Code** button, then **Download ZIP**.
2. Right-click the ZIP file and choose **Extract All**.

**Option B: Use Git**
```
git clone https://github.com/siddhant16-code/expense-tracker.git
```

### Step 3: Open PowerShell inside the project folder
Open the `expense-tracker` folder in File Explorer, click the **address bar** at the top, type `powershell` and press **Enter**.

Check you're in the right place by typing:
```
dir
```
You should see `app.py` and `requirements.txt` in the list. If you don't, you are in the wrong folder.

> Prefer typing the path? Use `cd C:\Users\YourName\Downloads\expense-tracker` (replace it with your real folder path).

### Step 4: Install the required libraries (one time only)
```
python -m pip install -r requirements.txt
```
Wait until it finishes.

### Step 5: Start the app
```
python -m streamlit run app.py
```
Your browser opens automatically at **http://localhost:8501** and the Expense Tracker appears. If Streamlit asks for an email, just press **Enter**.

### Step 6: Stop the app
Go back to PowerShell and press **Ctrl + C**.

---

## 🔁 Running it again later
Skip the install step. Just open PowerShell in the project folder and run:
```
python -m streamlit run app.py
```

---

## 👥 Want to run this project on another computer?
1. Open https://github.com/siddhant16-code/expense-tracker
2. Click **Code** → **Download ZIP** and extract it.
3. Follow Steps 1, 3, 4 and 5 above.

Or, if you have Git installed:
```
git clone https://github.com/siddhant16-code/expense-tracker.git
cd expense-tracker
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

---

## 🍎 Mac / Linux
Use `python3` instead of `python`:
```
cd path/to/expense-tracker
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

---

## ⚠️ Two things to remember
- **Keep the PowerShell window open** while you use the app. Closing it stops the app.
- Your data is saved in `expenses.csv` the first time you add an expense. The file appears in the project folder automatically and is **not** uploaded to GitHub.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `python is not recognized` | Reinstall Python and tick **Add Python to PATH**, then restart PowerShell. |
| `Repository not found` | Check the username in the link is correct, or use Option A (ZIP). |
| `Could not open requirements file` / `File does not exist: app.py` | You are in the wrong folder. Open PowerShell inside the project folder and check with `dir`. |
| `No module named streamlit` | Run Step 4 again. |
| Browser did not open | Manually open http://localhost:8501 |
| Port already in use | Run `python -m streamlit run app.py --server.port 8502` |

---

## 💾 Where is my data saved?
Your expenses are saved on your own computer in `expenses.csv` and your settings in `settings.json`. Both files are created automatically in the project folder. They are excluded from Git by `.gitignore`, so your personal finances are never uploaded to GitHub.

## 🧰 Tech stack
Python · Streamlit · Pandas · Altair

## 📄 License
Free to use and modify.
