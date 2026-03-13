"""
Customer Churn Analytics — Main Analysis
PHOENIX Group Operational Controlling Analytics Project
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import json
import os

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Generate data inline if CSV not present
def generate_data(n=2000):
    import random
    from datetime import datetime, timedelta
    random.seed(42); np.random.seed(42)
    regions = ["Baden-Württemberg","Bavaria","NRW","Hesse","Saxony","Hamburg","Berlin"]
    segments = ["Independent Pharmacy","Chain Pharmacy","Hospital Pharmacy","Online Pharmacy"]
    data = []
    for i in range(n):
        late_payments = random.randint(0,12)
        support_tickets = random.randint(0,20)
        last_order_days_ago = random.randint(1,90)
        nps_score = random.randint(1,10)
        monthly_order_value = round(np.random.lognormal(8.5,0.8),2)
        order_frequency = random.randint(2,30)
        churn_score = 0
        if late_payments > 6: churn_score += 2
        if support_tickets > 12: churn_score += 2
        if last_order_days_ago > 45: churn_score += 3
        if nps_score < 5: churn_score += 2
        if monthly_order_value < 2000: churn_score += 1
        if order_frequency < 5: churn_score += 1
        churn_score += random.randint(-2,2)
        data.append({
            "customer_id": f"CUST{str(i+1).zfill(5)}",
            "region": random.choice(regions),
            "segment": random.choice(segments),
            "monthly_order_value_eur": monthly_order_value,
            "order_frequency_per_month": order_frequency,
            "late_payments_last_12m": late_payments,
            "support_tickets_last_6m": support_tickets,
            "discount_rate": round(random.uniform(0.02,0.18),3),
            "last_order_days_ago": last_order_days_ago,
            "nps_score": nps_score,
            "product_categories_ordered": random.randint(1,8),
            "churned": 1 if churn_score >= 5 else 0
        })
    return pd.DataFrame(data)

df = generate_data()
df.to_csv("data/customers_raw.csv", index=False)

# Encode categoricals
le_region = LabelEncoder()
le_segment = LabelEncoder()
df["region_enc"] = le_region.fit_transform(df["region"])
df["segment_enc"] = le_segment.fit_transform(df["segment"])

features = ["monthly_order_value_eur","order_frequency_per_month","late_payments_last_12m",
            "support_tickets_last_6m","discount_rate","last_order_days_ago",
            "nps_score","product_categories_ordered","region_enc","segment_enc"]

X = df[features]
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])

# Feature importance
importance_df = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

# Churn by region
churn_region = df.groupby("region").agg(
    total=("churned","count"),
    churned=("churned","sum"),
    avg_value=("monthly_order_value_eur","mean")
).reset_index()
churn_region["churn_rate"] = (churn_region["churned"] / churn_region["total"] * 100).round(1)

# Churn by segment
churn_segment = df.groupby("segment").agg(
    total=("churned","count"),
    churned=("churned","sum"),
    avg_value=("monthly_order_value_eur","mean")
).reset_index()
churn_segment["churn_rate"] = (churn_segment["churned"] / churn_segment["total"] * 100).round(1)

# Risk tiers
df["risk_tier"] = "Low Risk"
df.loc[(df["late_payments_last_12m"] > 6) & (df["nps_score"] < 5), "risk_tier"] = "Critical"
df.loc[(df["late_payments_last_12m"] > 3) | (df["last_order_days_ago"] > 45), "risk_tier"] = "High Risk"
risk_summary = df[df["churned"]==0].groupby("risk_tier").agg(
    customers=("customer_id","count"),
    revenue_at_risk=("monthly_order_value_eur","sum")
).reset_index()

# Save outputs
churn_region.to_csv("outputs/churn_by_region.csv", index=False)
churn_segment.to_csv("outputs/churn_by_segment.csv", index=False)
importance_df.to_csv("outputs/feature_importance.csv", index=False)
risk_summary.to_csv("outputs/risk_tiers.csv", index=False)

print(f"Model AUC: {auc:.3f}")
print(f"Churn rate: {df['churned'].mean():.1%}")
print(classification_report(y_test, y_pred))

# Generate HTML dashboard
total_customers = len(df)
churn_count = df["churned"].sum()
churn_rate = df["churned"].mean() * 100
revenue_at_risk = df[df["churned"]==1]["monthly_order_value_eur"].sum()
avg_value = df["monthly_order_value_eur"].mean()

region_rows = "".join([
    f"<tr><td>{r['region']}</td><td>{r['total']}</td><td>{r['churn_rate']}%</td><td>€{r['avg_value']:,.0f}</td></tr>"
    for _, r in churn_region.iterrows()
])

segment_rows = "".join([
    f"<tr><td>{r['segment']}</td><td>{r['total']}</td><td>{r['churn_rate']}%</td><td>€{r['avg_value']:,.0f}</td></tr>"
    for _, r in churn_segment.iterrows()
])

feature_rows = "".join([
    f"<tr><td>{r['feature']}</td><td><div style='background:#6D28D9;height:16px;width:{r['importance']*400:.0f}px;border-radius:3px'></div></td><td>{r['importance']:.3f}</td></tr>"
    for _, r in importance_df.head(6).iterrows()
])

risk_rows = "".join([
    f"<tr><td>{r['risk_tier']}</td><td>{r['customers']}</td><td>€{r['revenue_at_risk']:,.0f}</td></tr>"
    for _, r in risk_summary.iterrows()
])

html = f"""<!DOCTYPE html>
<html><head><meta charset='UTF-8'>
<title>Customer Churn Analytics — PHOENIX Group</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',sans-serif}}
body{{background:#F5F3FF;color:#1A1A1A}}
.header{{background:#1E1B2E;color:white;padding:28px 36px}}
.header h1{{font-size:22px;font-weight:700}}
.header p{{color:#A78BFA;font-size:13px;margin-top:4px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:24px 36px}}
.kpi{{background:white;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.08)}}
.kpi .val{{font-size:28px;font-weight:700;color:#6D28D9}}
.kpi .lbl{{font-size:12px;color:#6B7280;margin-top:4px}}
.section{{padding:0 36px 24px}}
.section h2{{font-size:14px;font-weight:700;color:#3B0764;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;border-bottom:2px solid #6D28D9;padding-bottom:6px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.card{{background:white;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.08)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;padding:8px 10px;background:#F5F3FF;color:#5B21B6;font-weight:600}}
td{{padding:8px 10px;border-bottom:1px solid #F3F4F6}}
tr:last-child td{{border-bottom:none}}
.auc{{background:#EDE9FE;border-radius:8px;padding:12px 20px;margin-bottom:16px;font-size:13px;color:#5B21B6;font-weight:600}}
</style></head><body>
<div class='header'>
  <h1>Customer Churn Analytics Dashboard</h1>
  <p>PHOENIX Group · Operational Controlling Analytics · MSc Project ECE Paris 2025–2026</p>
</div>
<div class='kpis'>
  <div class='kpi'><div class='val'>{total_customers:,}</div><div class='lbl'>Total Customers</div></div>
  <div class='kpi'><div class='val'>{churn_count:,}</div><div class='lbl'>Churned Customers</div></div>
  <div class='kpi'><div class='val'>{churn_rate:.1f}%</div><div class='lbl'>Overall Churn Rate</div></div>
  <div class='kpi'><div class='val'>€{revenue_at_risk:,.0f}</div><div class='lbl'>Monthly Revenue at Risk</div></div>
</div>
<div class='section'>
  <h2>Model Performance</h2>
  <div class='auc'>Random Forest Classifier · AUC Score: {auc:.3f} · Trained on 1,600 customers · Validated on 400</div>
</div>
<div class='section'>
  <div class='grid2'>
    <div class='card'>
      <h2>Churn by Region</h2>
      <table><tr><th>Region</th><th>Customers</th><th>Churn Rate</th><th>Avg Value</th></tr>{region_rows}</table>
    </div>
    <div class='card'>
      <h2>Churn by Segment</h2>
      <table><tr><th>Segment</th><th>Customers</th><th>Churn Rate</th><th>Avg Value</th></tr>{segment_rows}</table>
    </div>
  </div>
</div>
<div class='section'>
  <div class='grid2'>
    <div class='card'>
      <h2>Top Churn Predictors</h2>
      <table><tr><th>Feature</th><th>Importance</th><th>Score</th></tr>{feature_rows}</table>
    </div>
    <div class='card'>
      <h2>Revenue at Risk by Tier</h2>
      <table><tr><th>Risk Tier</th><th>Customers</th><th>Monthly Revenue</th></tr>{risk_rows}</table>
    </div>
  </div>
</div>
</body></html>"""

with open("outputs/churn_dashboard.html", "w") as f:
    f.write(html)

print("Dashboard saved to outputs/churn_dashboard.html")
