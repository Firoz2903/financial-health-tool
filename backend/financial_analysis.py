def analyze_financials(df):
    total_revenue = float(df["revenue"].sum())
    total_expense = float(df["expense"].sum())
    profit = total_revenue - total_expense

    profit_margin = (
        (profit / total_revenue) * 100 if total_revenue > 0 else 0
    )

    health_score = int(min(max(profit_margin + 50, 0), 100))

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expense": round(total_expense, 2),
        "profit": round(profit, 2),
        "profit_margin": round(profit_margin, 2),
        "financial_health_score": health_score
    }
