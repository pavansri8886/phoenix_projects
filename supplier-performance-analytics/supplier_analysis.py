"""
Supplier Performance & Negotiation Analytics
PHOENIX Group Operational Controlling Analytics Project
Supplier scorecard supporting commercial team negotiation strategies
"""

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

random.seed(42)
np.random.seed(42)

N_SUPPLIERS = 40
N_ORDERS = 3000

categories = ["Prescription Drugs","OTC Medication","Medical Devices","Vaccines","Specialty Pharma"]
countries = ["Germany","Netherlands","Switzerland","France","Italy","Denmark","Belgium"]

def generate_suppliers():
    data = []
    for i in range(N_SUPPLIERS):
        base_reliability = random.uniform(0.6, 0.98)
        data.append({
            "supplier_id": f"SUP{str(i+1).zfill(3)}",
            "supplier_name": f"PharmaSupplier {chr(65+i%26)}{i//26 if i>=26 else ''}",
            "country": random.choice(countries),
            "category": random.choice(categories),
            "contract_value_eur": round(np.random.lognormal(12, 0.8)),
            "payment_terms_days": random.choice([30, 45, 60, 90]),
            "base_reliability": base_reliability,
            "years_active": random.randint(1, 15),
            "iso_certified": random.choice([True, True, True, False]),
        })
    return pd.DataFrame(data)

def generate_orders(suppliers_df):
    records = []
    base_date = datetime(2024, 1, 1)
    for i in range(N_ORDERS):
        supplier = suppliers_df.sample(1).iloc[0]
        order_date = base_date + timedelta(days=random.randint(0, 365))
        promised_days = random.randint(3, 21)
        reliability = supplier["base_reliability"]
        on_time = random.random() < reliability
        actual_days = promised_days if on_time else promised_days + random.randint(1, 14)
        quantity = random.randint(100, 5000)
        unit_price = round(np.random.lognormal(3.2, 0.9), 2)
        quality_pass = random.random() < (reliability * 1.02)
        defect_rate = round(random.uniform(0, 0.08) if not quality_pass else random.uniform(0, 0.02), 4)
        records.append({
            "order_id": f"ORD{str(i+1).zfill(5)}",
            "supplier_id": supplier["supplier_id"],
            "supplier_name": supplier["supplier_name"],
            "category": supplier["category"],
            "country": supplier["country"],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "promised_delivery_days": promised_days,
            "actual_delivery_days": actual_days,
            "on_time_delivery": int(on_time),
            "quantity_ordered": quantity,
            "unit_price_eur": unit_price,
            "order_value_eur": round(quantity * unit_price, 2),
            "quality_pass": int(quality_pass),
            "defect_rate": defect_rate,
            "invoice_accuracy": int(random.random() < 0.92),
        })
    return pd.DataFrame(records)

suppliers = generate_suppliers()
orders = generate_orders(suppliers)
suppliers.to_csv("data/suppliers.csv", index=False)
orders.to_csv("data/orders.csv", index=False)

# Scorecard calculation
scorecard = orders.groupby(["supplier_id","supplier_name","category","country"]).agg(
    total_orders=("order_id","count"),
    on_time_rate=("on_time_delivery","mean"),
    quality_pass_rate=("quality_pass","mean"),
    avg_delay_days=("actual_delivery_days","mean"),
    avg_defect_rate=("defect_rate","mean"),
    total_order_value=("order_value_eur","sum"),
    invoice_accuracy=("invoice_accuracy","mean"),
    avg_unit_price=("unit_price_eur","mean")
).reset_index()

scorecard["on_time_rate"] = (scorecard["on_time_rate"] * 100).round(1)
scorecard["quality_pass_rate"] = (scorecard["quality_pass_rate"] * 100).round(1)
scorecard["invoice_accuracy"] = (scorecard["invoice_accuracy"] * 100).round(1)
scorecard["avg_delay_days"] = scorecard["avg_delay_days"].round(1)
scorecard["avg_defect_rate"] = (scorecard["avg_defect_rate"] * 100).round(2)

# Overall performance score for negotiation prioritisation
scorecard["performance_score"] = (
    scorecard["on_time_rate"] * 0.35 +
    scorecard["quality_pass_rate"] * 0.35 +
    scorecard["invoice_accuracy"] * 0.20 +
    (100 - scorecard["avg_defect_rate"] * 100) * 0.10
).round(1)

scorecard["negotiation_priority"] = pd.cut(
    scorecard["performance_score"],
    bins=[0, 70, 80, 90, 100],
    labels=["Immediate Review", "Improvement Plan", "Monitor", "Preferred Partner"]
)

scorecard.to_csv("outputs/supplier_scorecard.csv", index=False)

# Category benchmarks
benchmarks = scorecard.groupby("category").agg(
    avg_on_time=("on_time_rate","mean"),
    avg_quality=("quality_pass_rate","mean"),
    avg_score=("performance_score","mean"),
    total_suppliers=("supplier_id","count")
).reset_index().round(1)

benchmarks.to_csv("outputs/category_benchmarks.csv", index=False)

# HTML dashboard
top_suppliers = scorecard.nlargest(10, "performance_score")
bottom_suppliers = scorecard.nsmallest(5, "performance_score")
total_spend = orders["order_value_eur"].sum()
avg_on_time = orders["on_time_delivery"].mean() * 100
avg_quality = orders["quality_pass"].mean() * 100

top_rows = "".join([
    f"<tr><td>{r['supplier_name']}</td><td>{r['category']}</td><td>{r['on_time_rate']}%</td><td>{r['quality_pass_rate']}%</td><td><b>{r['performance_score']}</b></td><td style='color:green'>{r['negotiation_priority']}</td></tr>"
    for _, r in top_suppliers.iterrows()
])
bottom_rows = "".join([
    f"<tr><td>{r['supplier_name']}</td><td>{r['category']}</td><td>{r['on_time_rate']}%</td><td>{r['quality_pass_rate']}%</td><td><b>{r['performance_score']}</b></td><td style='color:#DC2626'>{r['negotiation_priority']}</td></tr>"
    for _, r in bottom_suppliers.iterrows()
])
bench_rows = "".join([
    f"<tr><td>{r['category']}</td><td>{r['total_suppliers']}</td><td>{r['avg_on_time']}%</td><td>{r['avg_quality']}%</td><td>{r['avg_score']}</td></tr>"
    for _, r in benchmarks.iterrows()
])

html = f"""<!DOCTYPE html>
<html><head><meta charset='UTF-8'>
<title>Supplier Performance Analytics — PHOENIX Group</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',sans-serif}}
body{{background:#FFF7ED;color:#1A1A1A}}
.header{{background:#1C0A00;color:white;padding:28px 36px}}
.header h1{{font-size:22px;font-weight:700}}
.header p{{color:#FED7AA;font-size:13px;margin-top:4px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:24px 36px}}
.kpi{{background:white;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.08)}}
.kpi .val{{font-size:26px;font-weight:700;color:#EA580C}}
.kpi .lbl{{font-size:12px;color:#6B7280;margin-top:4px}}
.section{{padding:0 36px 24px}}
.section h2{{font-size:14px;font-weight:700;color:#7C2D12;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;border-bottom:2px solid #EA580C;padding-bottom:6px}}
.card{{background:white;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.08);margin-bottom:20px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;padding:8px 10px;background:#FFF7ED;color:#C2410C;font-weight:600}}
td{{padding:8px 10px;border-bottom:1px solid #F3F4F6}}
</style></head><body>
<div class='header'>
  <h1>Supplier Performance & Negotiation Analytics</h1>
  <p>PHOENIX Group · Operational Controlling Analytics · MSc Project ECE Paris 2025–2026</p>
</div>
<div class='kpis'>
  <div class='kpi'><div class='val'>{N_SUPPLIERS}</div><div class='lbl'>Active Suppliers</div></div>
  <div class='kpi'><div class='val'>€{total_spend/1e6:.1f}M</div><div class='lbl'>Total Spend (12M)</div></div>
  <div class='kpi'><div class='val'>{avg_on_time:.1f}%</div><div class='lbl'>Avg On-Time Delivery</div></div>
  <div class='kpi'><div class='val'>{avg_quality:.1f}%</div><div class='lbl'>Avg Quality Pass Rate</div></div>
</div>
<div class='section'>
  <div class='card'>
    <h2>Top 10 Preferred Partners</h2>
    <table><tr><th>Supplier</th><th>Category</th><th>On-Time</th><th>Quality</th><th>Score</th><th>Priority</th></tr>{top_rows}</table>
  </div>
  <div class='card'>
    <h2>Immediate Review Required</h2>
    <table><tr><th>Supplier</th><th>Category</th><th>On-Time</th><th>Quality</th><th>Score</th><th>Priority</th></tr>{bottom_rows}</table>
  </div>
  <div class='card'>
    <h2>Category Benchmarks</h2>
    <table><tr><th>Category</th><th>Suppliers</th><th>Avg On-Time</th><th>Avg Quality</th><th>Avg Score</th></tr>{bench_rows}</table>
  </div>
</div>
</body></html>"""

with open("outputs/supplier_dashboard.html", "w") as f:
    f.write(html)

print(f"Suppliers: {N_SUPPLIERS}, Orders: {N_ORDERS}")
print(f"Total spend: €{total_spend:,.0f}")
print(f"Avg on-time: {avg_on_time:.1f}%")
print("Dashboard saved to outputs/supplier_dashboard.html")
