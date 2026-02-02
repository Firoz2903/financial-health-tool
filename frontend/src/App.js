import { useState } from "react";
import {
  AreaChart, Area,
  XAxis, YAxis,
  Tooltip, CartesianGrid,
  BarChart, Bar
} from "recharts";

import "./index.css";

export default function App() {

  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [lang, setLang] = useState("en");

  const upload = async () => {
    const f = new FormData();
    f.append("file", file);

    const r = await fetch(`https://financial-health-backend.onrender.com/analyze?lang=${lang}`, {
      method: "POST",
      body: f
    });

    setData(await r.json());
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial", background:"#f6f8fb" }}>

      <h1>📊 Financial Health Dashboard</h1>

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={upload}>Analyze</button>

      <button onClick={() => setLang("en")}>EN</button>
      <button onClick={() => setLang("hi")}>हिंदी</button>

      {data && (
        <>

        {/* ================= SUMMARY ================= */}
        <div className="card">
          <h2>📌 Summary</h2>

          <p>Revenue: ₹{data.revenue}</p>
          <p>Expense: ₹{data.expense}</p>
          <p>Profit: ₹{data.profit}</p>
          <p>Margin: {data.margin}%</p>
          <p>Health Score: {data.health_score}/100</p>

          {/* ⭐ Credit Gauge */}
          <h3>Credit Score</h3>
          <div style={{background:"#eee", borderRadius:20}}>
            <div
              style={{
                width:`${data.credit_score}%`,
                background:"#4CAF50",
                color:"white",
                padding:"8px",
                borderRadius:20,
                textAlign:"center"
              }}
            >
              {data.credit_score}/100
            </div>
          </div>
        </div>


        {/* ================= FORECAST + BENCHMARK ================= */}
        <div className="card">
          <h2>📈 Forecast & Benchmark</h2>
          <p>Next Month Revenue: ₹{data.forecast}</p>
          <p>{data.industry} → {data.benchmark}</p>
        </div>


        {/* ================= RISK ================= */}
        <div className="card">
          <h2>⚠ Risk Level</h2>
          <b>{data.risk_level}</b>
        </div>


        {/* ================= AREA CHART ================= */}
        <div className="card">
          <h2>📊 Revenue vs Expense</h2>

          <AreaChart width={950} height={300} data={data.chart_data}>
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="date"/>
            <YAxis/>
            <Tooltip/>

            <Area
              type="monotone"
              dataKey="revenue"
              stroke="#4CAF50"
              fill="#4CAF50"
            />

            <Area
              type="monotone"
              dataKey="expense"
              stroke="#F44336"
              fill="#F44336"
            />
          </AreaChart>
        </div>


        {/* ================= EXPENSE CATEGORY ================= */}
        {data.expense_categories && (
          <div className="card">
            <h2>📊 Expense Categories</h2>

            <BarChart
              width={700}
              height={300}
              data={Object.entries(data.expense_categories)
                .map(([k,v])=>({name:k,value:v}))}
            >
              <XAxis dataKey="name"/>
              <YAxis/>
              <Tooltip/>
              <Bar dataKey="value" fill="#2196F3"/>
            </BarChart>
          </div>
        )}


        {/* ================= FINANCIAL DETAILS ================= */}
        <div className="card">
          <h2>💼 Financial Details</h2>
          <p>Receivable: ₹{data.receivable}</p>
          <p>Payable: ₹{data.payable}</p>
          <p>Inventory: ₹{data.inventory}</p>
          <p>Total Loan: ₹{data.loan_total}</p>
          <p>GST Collected: ₹{data.gst_collected}</p>
          <p>GST Paid: ₹{data.gst_paid}</p>
        </div>


        {/* ================= SUGGESTIONS ================= */}
        <div className="card">
          <h2>💡 Cost Suggestions</h2>
          {data.suggestions?.map((s,i)=>
            <div key={i}>• {s}</div>
          )}
        </div>


        {/* ================= AI ================= */}
        <div className="card">
          <h2>🤖 AI Insights</h2>
          <p style={{whiteSpace:"pre-line"}}>{data.ai_insights}</p>
        </div>


        {/* ================= EXPORT ================= */}
        <div className="card">
          <button onClick={()=>fetch("http://127.0.0.1:8000/export")}>
            📄 Export PDF Report
          </button>
        </div>

        </>
      )}

    </div>
  );
}
