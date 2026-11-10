"""Personal Expense Tracker v2 (web app)
Install:  python -m pip install streamlit pandas
Run:      python -m streamlit run app.py
Data is saved in expenses.csv and settings.json in the same folder.
"""

import calendar
import json
import os
from datetime import date

import altair as alt
import pandas as pd
import streamlit as st

FILE = "expenses.csv"
SETTINGS_FILE = "settings.json"
COLUMNS = ["date", "category", "description", "amount", "payment"]
CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Health", "Entertainment", "Other"]
PAYMENTS = ["Cash", "UPI", "Card", "Bank Transfer", "Other"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PALETTE = ["#6366f1", "#ec4899", "#f59e0b", "#14b8a6", "#8b5cf6", "#22d3ee", "#f43f5e"]


def grad(rgb):
    """Vertical gradient fill for charts, e.g. grad("99,102,241")."""
    return alt.Gradient(
        gradient="linear",
        stops=[alt.GradientStop(color=f"rgba({rgb},0.05)", offset=0),
               alt.GradientStop(color=f"rgba({rgb},0.8)", offset=1)],
        x1=1, x2=1, y1=1, y2=0,
    )

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

st.markdown(
    """
<style>
@keyframes gradientShift { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
@keyframes fadeUp { from {opacity: 0; transform: translateY(16px);} to {opacity: 1; transform: translateY(0);} }

/* Hero banner */
.hero {
    padding: 26px 32px; border-radius: 20px; margin-bottom: 18px; color: white;
    background: linear-gradient(120deg, #6366f1, #8b5cf6, #ec4899, #f59e0b, #6366f1);
    background-size: 300% 300%; animation: gradientShift 12s ease infinite, fadeUp .7s ease;
    box-shadow: 0 10px 30px rgba(139,92,246,0.35);
}
.hero h1 { margin: 0; font-size: 2.4rem; font-weight: 800; color: white; padding: 0; }
.hero p { margin: 4px 0 0 0; opacity: 0.9; font-size: 1rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(99,102,241,0.18), rgba(236,72,153,0.14), rgba(245,158,11,0.10));
    border-right: 1px solid rgba(139,92,246,0.25);
}

/* Metric cards: a different colour for each column */
[data-testid="stMetric"] {
    border-radius: 16px; padding: 16px 20px; animation: fadeUp .7s ease;
    border: 1px solid rgba(128,128,128,0.18); border-left-width: 6px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.10);
    transition: transform .25s ease, box-shadow .25s ease;
}
[data-testid="stMetric"]:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 14px 28px rgba(0,0,0,0.20); }
[data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetric"] { background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(99,102,241,0.05)); border-left-color: #6366f1; }
[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] { background: linear-gradient(135deg, rgba(236,72,153,0.22), rgba(236,72,153,0.05)); border-left-color: #ec4899; }
[data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] { background: linear-gradient(135deg, rgba(245,158,11,0.22), rgba(245,158,11,0.05)); border-left-color: #f59e0b; }
[data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] { background: linear-gradient(135deg, rgba(20,184,166,0.22), rgba(20,184,166,0.05)); border-left-color: #14b8a6; }

/* Buttons */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: linear-gradient(90deg, #6366f1, #ec4899); color: white; border: none;
    border-radius: 12px; font-weight: 600; padding: 0.5rem 1.2rem;
    transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px) scale(1.03); box-shadow: 0 8px 18px rgba(236,72,153,0.4);
    filter: brightness(1.1); color: white; border: none;
}

/* Tabs as colourful pills */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    border-radius: 999px; padding: 8px 20px; font-weight: 600;
    background: rgba(128,128,128,0.12); transition: all .2s ease;
}
.stTabs [data-baseweb="tab"]:hover { background: rgba(139,92,246,0.25); }
.stTabs [aria-selected="true"] { background: linear-gradient(90deg, #6366f1, #ec4899); }
.stTabs [aria-selected="true"] p { color: white !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* Budget progress bar */
[data-testid="stProgress"] div[role="progressbar"] > div,
.stProgress > div > div > div > div {
    background-image: linear-gradient(90deg, #22d3ee, #8b5cf6, #ec4899) !important;
}

/* Section headings and charts */
h3 { background: linear-gradient(90deg, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
[data-testid="stVegaLiteChart"], [data-testid="stDataFrame"] { animation: fadeUp .8s ease; }
</style>
""",
    unsafe_allow_html=True,
)


# ---------- Data helpers ----------
def load_settings():
    settings = {"budget": 0.0, "currency": "₹"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                settings.update(json.load(f))
        except (json.JSONDecodeError, OSError):
            pass
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f)


def load():
    df = pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=COLUMNS)
    if "payment" not in df.columns:
        df["payment"] = "Cash"
    df["payment"] = df["payment"].fillna("Cash")
    df["description"] = df["description"].fillna("")
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"])
    return df[COLUMNS].reset_index(drop=True)


def save(df):
    out = df[COLUMNS].copy()
    out["date"] = pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")
    out.to_csv(FILE, index=False)


# ---------- Load data & settings ----------
df = load()
settings = load_settings()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    currencies = ["₹", "$", "€", "£"]
    cur = st.selectbox(
        "Currency", currencies, index=currencies.index(settings["currency"])
        if settings["currency"] in currencies else 0
    )
    budget = st.number_input(
        "Monthly budget (0 = off)", min_value=0.0, step=500.0, value=float(settings["budget"])
    )
    if cur != settings["currency"] or budget != settings["budget"]:
        settings = {"budget": budget, "currency": cur}
        save_settings(settings)

    st.divider()
    st.header("➕ Add expense")
    with st.form("add_form", clear_on_submit=True):
        day = st.date_input("Date", value=date.today())
        category = st.selectbox("Category", CATEGORIES)
        payment = st.selectbox("Paid with", PAYMENTS)
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")
        submitted = st.form_submit_button("Add expense", use_container_width=True)
    if submitted:
        if amount <= 0:
            st.error("Enter an amount greater than 0.")
        else:
            new_row = pd.DataFrame(
                [{"date": pd.to_datetime(day), "category": category,
                  "description": description, "amount": amount, "payment": payment}]
            )
            df = pd.concat([df, new_row], ignore_index=True)
            save(df)
            st.toast(f"Added {cur}{amount:,.2f} for {category}", icon="✅")


def fmt(x):
    return f"{cur}{x:,.2f}"


# ---------- Header ----------
st.markdown(
    f'<div class="hero"><h1>💰 Expense Tracker</h1>'
    f'<p>{date.today():%A, %d %B %Y} · track it, see it, own it</p></div>',
    unsafe_allow_html=True,
)

if df.empty:
    st.info("No expenses yet. Add your first one from the sidebar 👈")
    st.stop()

df["month"] = df["date"].dt.strftime("%Y-%m")
months = sorted(df["month"].unique(), reverse=True)
options = ["All"] + months
this_month = date.today().strftime("%Y-%m")
choice = st.selectbox(
    "📅 Period", options, index=options.index(this_month) if this_month in options else 0
)
view = (df if choice == "All" else df[df["month"] == choice]).copy()

tab_dash, tab_tx, tab_ins = st.tabs(["📊 Dashboard", "🧾 Transactions", "💡 Insights"])

# ================= DASHBOARD =================
with tab_dash:
    if view.empty:
        st.info("No expenses in this period.")
    else:
        total = view["amount"].sum()
        by_cat = view.groupby("category")["amount"].sum().reset_index()
        top_cat = by_cat.sort_values("amount", ascending=False).iloc[0]

        delta = None
        if choice != "All":
            prev = str(pd.Period(choice, "M") - 1)
            prev_total = df.loc[df["month"] == prev, "amount"].sum()
            if prev_total > 0:
                delta = f"{(total - prev_total) / prev_total:+.0%} vs last month"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total spent", fmt(total), delta, delta_color="inverse")
        c2.metric("Expenses", len(view))
        c3.metric("Average", fmt(view["amount"].mean()))
        c4.metric("Top category", top_cat["category"], fmt(top_cat["amount"]), delta_color="off")

        # Budget tracker
        if settings["budget"] > 0 and choice != "All":
            pct = total / settings["budget"]
            st.progress(min(pct, 1.0), text=f"Budget: {fmt(total)} of {fmt(settings['budget'])} ({pct:.0%})")
            if pct >= 1:
                st.error(f"🚨 Over budget by {fmt(total - settings['budget'])}!")
            elif pct >= 0.8:
                st.warning(f"⚠️ Only {fmt(settings['budget'] - total)} left in your budget.")
            else:
                st.success(f"✅ {fmt(settings['budget'] - total)} left in your budget.")
        elif settings["budget"] > 0:
            st.caption("Pick a month above to see your budget progress.")

        left, right = st.columns(2)
        with left:
            st.subheader("Spending by category")
            donut = (
                alt.Chart(by_cat)
                .mark_arc(innerRadius=70)
                .encode(
                    theta="amount:Q",
                    color=alt.Color("category:N", scale=alt.Scale(range=PALETTE), legend=alt.Legend(title=None)),
                    tooltip=["category", alt.Tooltip("amount:Q", format=",.2f")],
                )
            )
            st.altair_chart(donut, use_container_width=True)
        with right:
            st.subheader("Daily spending")
            daily = view.groupby("date")["amount"].sum().reset_index()
            area = (
                alt.Chart(daily)
                .mark_area(line={"color": "#8b5cf6"}, point={"color": "#ec4899", "filled": True}, interpolate="monotone", color=grad("139,92,246"))
                .encode(
                    x=alt.X("date:T", title=None),
                    y=alt.Y("amount:Q", title=None),
                    tooltip=[alt.Tooltip("date:T"), alt.Tooltip("amount:Q", format=",.2f")],
                )
            )
            st.altair_chart(area, use_container_width=True)

        st.subheader("Monthly trend")
        monthly = df.groupby("month")["amount"].sum().reset_index()
        bars = (
            alt.Chart(monthly)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color=grad("99,102,241"))
            .encode(
                x=alt.X("month:N", title=None),
                y=alt.Y("amount:Q", title=None),
                tooltip=["month", alt.Tooltip("amount:Q", format=",.2f")],
            )
        )
        st.altair_chart(bars, use_container_width=True)

        st.subheader("Recent expenses")
        recent = view.sort_values("date", ascending=False).head(5)[COLUMNS].copy()
        recent["date"] = recent["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(recent, use_container_width=True, hide_index=True)

# ================= TRANSACTIONS =================
with tab_tx:
    f1, f2 = st.columns([2, 1])
    search = f1.text_input("🔍 Search description", "")
    cat_options = sorted(set(CATEGORIES) | set(df["category"]))
    cats = f2.multiselect("Category", cat_options)

    tx = view.copy()
    if search:
        tx = tx[tx["description"].str.contains(search, case=False, na=False)]
    if cats:
        tx = tx[tx["category"].isin(cats)]
    tx = tx.sort_values("date", ascending=False)

    st.caption(f"{len(tx)} expense(s) · total {fmt(tx['amount'].sum())}. "
               "Edit cells directly or tick **Delete**, then press Save.")

    edit_df = tx[COLUMNS].copy()
    edit_df["delete"] = False
    edited = st.data_editor(
        edit_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "category": st.column_config.SelectboxColumn("Category", options=cat_options),
            "description": st.column_config.TextColumn("Description"),
            "amount": st.column_config.NumberColumn("Amount", min_value=0.0, format="%.2f"),
            "payment": st.column_config.SelectboxColumn("Paid with", options=PAYMENTS),
            "delete": st.column_config.CheckboxColumn("Delete"),
        },
    )

    b1, b2, _ = st.columns([1, 1, 3])
    if b1.button("💾 Save changes", type="primary"):
        drop_idx = edited.index[edited["delete"]]
        keep = edited.drop(index=drop_idx).drop(columns="delete")
        df.loc[keep.index, COLUMNS] = keep[COLUMNS]
        df = df.drop(index=drop_idx)
        save(df)
        st.rerun()

    csv_out = tx[COLUMNS].assign(date=tx["date"].dt.strftime("%Y-%m-%d")).to_csv(index=False)
    b2.download_button("⬇️ Download CSV", csv_out, "expenses.csv", "text/csv")

# ================= INSIGHTS =================
with tab_ins:
    if view.empty:
        st.info("No expenses in this period.")
    else:
        total = view["amount"].sum()
        days_span = (view["date"].max() - view["date"].min()).days + 1
        biggest = view.loc[view["amount"].idxmax()]

        i1, i2, i3 = st.columns(3)
        i1.metric("Biggest expense", fmt(biggest["amount"]), biggest["description"] or biggest["category"], delta_color="off")
        i2.metric("Average per day", fmt(total / days_span))
        if choice == this_month:
            days_in_month = calendar.monthrange(date.today().year, date.today().month)[1]
            projected = total / date.today().day * days_in_month
            i3.metric("Projected month-end", fmt(projected))
        else:
            i3.metric("Active days", view["date"].nunique())

        w, p = st.columns(2)
        with w:
            st.subheader("Spending by weekday")
            view["weekday"] = view["date"].dt.day_name()
            wd = view.groupby("weekday")["amount"].sum().reset_index()
            st.altair_chart(
                alt.Chart(wd).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color=grad("236,72,153")).encode(
                    x=alt.X("weekday:N", sort=WEEKDAYS, title=None),
                    y=alt.Y("amount:Q", title=None),
                    tooltip=["weekday", alt.Tooltip("amount:Q", format=",.2f")],
                ),
                use_container_width=True,
            )
        with p:
            st.subheader("Payment methods")
            pm = view.groupby("payment")["amount"].sum().reset_index()
            st.altair_chart(
                alt.Chart(pm).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
                    y=alt.Y("payment:N", sort="-x", title=None),
                    x=alt.X("amount:Q", title=None),
                    color=alt.Color("payment:N", scale=alt.Scale(range=PALETTE), legend=None),
                    tooltip=["payment", alt.Tooltip("amount:Q", format=",.2f")],
                ),
                use_container_width=True,
            )

        st.subheader("Category share")
        share = view.groupby("category")["amount"].sum().sort_values(ascending=False)
        share_df = pd.DataFrame({
            "Category": share.index,
            "Spent": [fmt(x) for x in share.values],
            "Share": [f"{x / total:.0%}" for x in share.values],
        })
        st.dataframe(share_df, use_container_width=True, hide_index=True)
