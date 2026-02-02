import numpy as np


# =========================================================
# HELPER: Normalize value to 0–100
# =========================================================
def normalize(value, min_v, max_v):
    if max_v == min_v:
        return 50
    score = (value - min_v) / (max_v - min_v) * 100
    return max(0, min(100, score))


# =========================================================
# CREDIT SCORE MODEL (Professional weighted scoring)
# =========================================================
def compute_credit_score(df, revenue, expense, profit, margin):

    # Profitability
    margin_score = normalize(margin, 0, 40)

    # Cashflow stability
    cashflow = df["revenue"] - df["expense"]
    stability = 100 - normalize(np.std(cashflow), 0, 20000)
    cash_score = stability

    # Expense efficiency
    expense_ratio = expense / revenue if revenue else 1
    expense_score = 100 - normalize(expense_ratio, 0.3, 1)

    # Growth
    growth = df["revenue"].pct_change().mean() if len(df) > 1 else 0
    growth_score = normalize(growth, -0.2, 0.3)

    # Debt load
    if "emi_amount" in df.columns:
        emi = df["emi_amount"].sum()
        debt_ratio = emi / revenue if revenue else 1
        debt_score = 100 - normalize(debt_ratio, 0, 0.5)
    else:
        debt_score = 80

    score = (
        margin_score * 0.30 +
        cash_score   * 0.25 +
        expense_score* 0.20 +
        growth_score * 0.15 +
        debt_score   * 0.10
    )

    return int(round(score))


# =========================================================
# MAIN FINANCIAL ENGINE
# =========================================================
def compute_metrics(df):

    # ======================
    # BASIC METRICS
    # ======================
    revenue = float(df["revenue"].sum())
    expense = float(df["expense"].sum())
    profit = revenue - expense
    margin = (profit / revenue * 100) if revenue > 0 else 0

    health_score = int(min(max(margin + 50, 0), 100))

    credit_score = compute_credit_score(df, revenue, expense, profit, margin)


    # ======================
    # EXPENSE CATEGORIES
    # ======================
    expense_categories = {}
    if "expense_category" in df.columns:
        expense_categories = (
            df.groupby("expense_category")["expense"]
            .sum()
            .to_dict()
        )


    # ======================
    # RISK LEVEL
    # ======================
    if credit_score >= 80:
        risk_level = "Low"
    elif credit_score >= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"


    # ======================
    # COST SUGGESTIONS
    # ======================
    suggestions = []

    if margin < 20:
        suggestions.append("Reduce unnecessary expenses")

    if expense > revenue * 0.8:
        suggestions.append("High operating costs detected")

    if credit_score < 60:
        suggestions.append("Improve profitability before taking loans")

    if not suggestions:
        suggestions.append("Financial performance looks healthy")


    # ======================
    # FORECASTING (simple)
    # ======================
    forecast = float(round(df["revenue"].mean() * 1.05, 2))


    # ======================
    # INDUSTRY BENCHMARK
    # ======================
    industry = df["industry"].iloc[0] if "industry" in df.columns else "General"

    industry_avg_margin = {
        "Retail": 20,
        "Manufacturing": 25,
        "Services": 30,
        "Logistics": 18,
        "Agriculture": 15,
        "E-commerce": 22
    }

    target = industry_avg_margin.get(industry, 20)

    benchmark = "Above industry average" if margin >= target else "Below industry average"


    # ======================
    # ACCOUNTS RECEIVABLE / PAYABLE
    # ======================
    receivable = 0
    payable = 0

    if "type" in df.columns and "amount" in df.columns:
        receivable = float(df[df["type"] == "receivable"]["amount"].sum())
        payable = float(df[df["type"] == "payable"]["amount"].sum())


    # ======================
    # INVENTORY
    # ======================
    inventory = 0
    if "inventory_closing" in df.columns:
        inventory = float(df["inventory_closing"].iloc[-1])


    # ======================
    # LOANS
    # ======================
    loan_total = 0
    if "loan_amount" in df.columns:
        loan_total = float(df["loan_amount"].max())


    # ======================
    # GST
    # ======================
    gst_collected = 0
    gst_paid = 0

    if "gst_collected" in df.columns:
        gst_collected = float(df["gst_collected"].sum())

    if "gst_paid" in df.columns:
        gst_paid = float(df["gst_paid"].sum())


    # ======================
    # RETURN EVERYTHING
    # ======================
    return {
        "revenue": revenue,
        "expense": expense,
        "profit": profit,
        "margin": round(margin, 2),

        "health_score": health_score,
        "credit_score": credit_score,
        "risk_level": risk_level,

        "forecast": forecast,
        "benchmark": benchmark,
        "industry": industry,

        "expense_categories": expense_categories,
        "suggestions": suggestions,

        "receivable": receivable,
        "payable": payable,
        "inventory": inventory,
        "loan_total": loan_total,

        "gst_collected": gst_collected,
        "gst_paid": gst_paid
    }
