from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd

from report_generator import create_report
from financial_engine import compute_metrics
from risk_engine import detect_risks
from ai_insights import generate_ai_insights
from auto_insights import auto_generate_insights


app = FastAPI(title="Financial Health Assessment Tool")


# =============================
# GLOBAL STORAGE (important)
# =============================
last_result = {}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================
# HOME
# =============================
@app.get("/")
def home():
    return {"message": "Backend running successfully 🚀"}


# =============================
# EXPORT PDF
# =============================
@app.get("/export")
def export_report():

    if not last_result:
        return {"error": "Run analysis first before exporting"}

    filename = create_report(last_result)

    return FileResponse(
    filename,
    media_type="application/pdf",
    filename="financial_report.pdf",
    headers={
        "Content-Disposition": "attachment; filename=financial_report.pdf"
    }
)



# =============================
# ANALYZE CSV
# =============================
@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):

    global last_result   # ⭐ VERY IMPORTANT

    # Read CSV
    df = pd.read_csv(file.file)

    if not {"revenue", "expense", "date"}.issubset(df.columns):
        return {"error": "CSV must contain date, revenue, expense columns"}

    # 1️⃣ Compute metrics
    result = compute_metrics(df)

    # 2️⃣ Chart data
    result["chart_data"] = df[["date", "revenue", "expense"]].to_dict(
        orient="records"
    )

    # 3️⃣ Risks
    result["risks"] = detect_risks(result)

    # 4️⃣ AI Insights (Claude → fallback)
    ai_text = generate_ai_insights(result)

    if not ai_text:
        ai_text = auto_generate_insights(result)

    result["ai_insights"] = ai_text

    # 5️⃣ Save globally for export
    last_result = result

    return result
