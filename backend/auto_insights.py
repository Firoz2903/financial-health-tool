def auto_generate_insights(metrics):

    tips = []

    if metrics["margin"] < 15:
        tips.append("Profit margin is low. Reduce costs immediately.")

    if metrics["risk_level"] == "High":
        tips.append("High financial risk detected. Avoid new loans.")

    if metrics["receivable"] > metrics["payable"]:
        tips.append("Improve collection speed to strengthen cashflow.")

    if not tips:
        tips.append("Financial performance looks healthy.")

    return " ".join(tips)
