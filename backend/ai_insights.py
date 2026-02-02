import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("api_key"))


def generate_ai_insights(metrics):

    prompt = f"""
You are a financial advisor.

Analyze this SME data and give:
1. Financial health summary
2. Risks
3. Cost optimization tips
4. Short actionable advice

DATA:
Revenue: {metrics['revenue']}
Expense: {metrics['expense']}
Profit: {metrics['profit']}
Margin: {metrics['margin']}%
Credit Score: {metrics['credit_score']}
Risk Level: {metrics['risk_level']}
GST Collected: {metrics['gst_collected']}
GST Paid: {metrics['gst_paid']}
Receivable: {metrics['receivable']}
Payable: {metrics['payable']}
"""

    try:
        res = client.messages.create(
            model="claude-3-haiku-20240307",  # cheap + fast
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}]
        )

        return res.content[0].text

    except:
        # fallback if API fails
        return None
