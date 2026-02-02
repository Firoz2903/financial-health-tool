def detect_risks(data):

    risks = []

    # Profit check
    if data["profit"] < 0:
        risks.append("Business operating at loss")

    # Margin check (UPDATED KEY)
    if data["margin"] < 10:
        risks.append("Low profitability")

    # Credit risk
    if data["credit_score"] < 50:
        risks.append("Low creditworthiness")

    # Cashflow risk
    if data["payable"] > data["receivable"]:
        risks.append("High outstanding payables")

    if not risks:
        risks.append("Financial position stable")

    return risks
