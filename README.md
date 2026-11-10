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

### Step 3: Open the project folder in PowerShell
Replace the path below with the folder where you extracted or cloned the project:
```
cd C:\Users\YourName\Downloads\expense-tracker
```
Type `dir` to check. You should see `app.py` and `requirements.txt` in the list.

> **Tip:** Open the folder in File Explorer, click the address bar, type `powershell` and press Enter. PowerShell opens directly inside that folder.

### Step 4: Install the required libraries (one time only)
```
python -m pip install -r requirements.txt
```

### Step 5: Start the app
```
python -m streamlit run app.py
```
Your browser opens automatically at **http://localhost:8501**. If Streamlit asks for an email, just press **Enter**.

### Step 6: Stop the app
Go back to PowerShell and press **Ctrl + C**.

To run it again later, you only need Step 3 and Step 5.

---

## 🍎 Mac / Linux
Use `python3` instead of `python`:
```
cd path/to/expense-tracker
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `python is not recognized` | Reinstall Python and tick **Add Python to PATH**, then restart PowerShell. |
| `Repository not found` | Replace `YOUR-USERNAME` with the real GitHub username, or use Option A (ZIP). |
| `Could not open requirements file` / `File does not exist: app.py` | You are in the wrong folder. Use `cd` to enter the project folder (check with `dir`). |
| `No module named streamlit` | Run Step 4 again. |
| Browser did not open | Manually open http://localhost:8501 |
| Port already in use | Run `python -m streamlit run app.py --server.port 8502` |

---

## 💾 Where is my data saved?
Your expenses are saved on your own computer in `expenses.csv` and your settings in `settings.json`. Both files are created automatically in the project folder the first time you add an expense. They are excluded from Git by `.gitignore`, so your personal finances are never uploaded to GitHub.

## 🧰 Tech stack
Python · Streamlit · Pandas · Altair

## 📄 License
Free to use and modify.
