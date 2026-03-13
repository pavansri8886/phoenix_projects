"""
Inventory Cost Analysis Dashboard
PHOENIX Group Operational Controlling Analytics Project
Pharmaceutical inventory cost monitoring across product categories and warehouses
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

# Synthetic pharmaceutical inventory data
categories = ["Prescription Drugs","OTC Medication","Medical Devices","Vitamins & Supplements","Vaccines","Specialty Pharma"]
warehouses = ["Mannheim HQ","Munich","Berlin","Hamburg","Frankfurt","Cologne"]
suppliers = [f"Supplier_{chr(65+i)}" for i in range(12)]

N_PRODUCTS = 500
N_MONTHS = 12

def generate_inventory():
    products = []
    for i in range(N_PRODUCTS):
        category = random.choice(categories)
        base_cost = np.random.lognormal(3.5, 1.2)
        products.append({
            "product_id": f"PROD{str(i+1).zfill(4)}",
            "product_name": f"{category} Product {i+1}",
            "category": category,
            "supplier": random.choice(suppliers),
            "warehouse": random.choice(warehouses),
            "unit_cost_eur": round(base_cost, 2),
            "storage_cost_per_unit_eur": round(base_cost * random.uniform(0.02, 0.08), 3),
            "shelf_life_days": random.randint(90, 730),
            "min_stock_units": random.randint(50, 500),
            "max_stock_units": random.randint(500, 5000),
        })
    return pd.DataFrame(products)

def generate_monthly_data(products_df):
    records = []
    base_date = datetime(2024, 1, 1)
    for month in range(N_MONTHS):
        month_date = base_date + timedelta(days=30*month)
        for _, prod in products_df.iterrows():
            stock_level = random.randint(int(prod["min_stock_units"]*0.5), prod["max_stock_units"])
            units_sold = random.randint(20, int(stock_level*0.6))
            units_expired = random.randint(0, int(stock_level*0.05))
            reorder_triggered = 1 if stock_level < prod["min_stock_units"] else 0
            records.append({
                "product_id": prod["product_id"],
                "category": prod["category"],
                "warehouse": prod["warehouse"],
                "month": month_date.strftime("%Y-%m"),
                "stock_level": stock_level,
                "units_sold": units_sold,
                "units_expired": units_expired,
                "total_stock_cost_eur": round(stock_level * prod["unit_cost_eur"], 2),
                "storage_cost_eur": round(stock_level * prod["storage_cost_per_unit_eur"], 2),
                "waste_cost_eur": round(units_expired * prod["unit_cost_eur"], 2),
                "revenue_eur": round(units_sold * prod["unit_cost_eur"] * random.uniform(1.15, 1.45), 2),
                "reorder_triggered": reorder_triggered,
            })
    return pd.DataFrame(records)

products = generate_inventory()
monthly = generate_monthly_data(products)
products.to_csv("data/products.csv", index=False)
monthly.to_csv("data/monthly_inventory.csv", index=False)

# Analysis
cost_by_category = monthly.groupby("category").agg(
    total_stock_cost=("total_stock_cost_eur","sum"),
    total_storage_cost=("storage_cost_eur","sum"),
    total_waste_cost=("waste_cost_eur","sum"),
    total_revenue=("revenue_eur","sum"),
    units_expired=("units_expired","sum")
).reset_index()
cost_by_category["waste_pct"] = (cost_by_category["total_waste_cost"] / cost_by_category["total_stock_cost"] * 100).round(2)
cost_by_category["margin_pct"] = ((cost_by_category["total_revenue"] - cost_by_category["total_stock_cost"]) / cost_by_category["total_revenue"] * 100).round(2)

cost_by_warehouse = monthly.groupby("warehouse").agg(
    total_stock_cost=("total_stock_cost_eur","sum"),
    total_storage_cost=("storage_cost_eur","sum"),
    total_waste_cost=("waste_cost_eur","sum"),
    total_revenue=("revenue_eur","sum")
).reset_index()
cost_by_warehouse["efficiency_score"] = ((1 - cost_by_warehouse["total_waste_cost"]/cost_by_warehouse["total_stock_cost"]) * 100).round(1)

monthly_trend = monthly.groupby("month").agg(
    total_cost=("total_stock_cost_eur","sum"),
    total_waste=("waste_cost_eur","sum"),
    total_revenue=("revenue_eur","sum"),
    reorders=("reorder_triggered","sum")
).reset_index()

cost_by_category.to_csv("outputs/cost_by_category.csv", index=False)
cost_by_warehouse.to_csv("outputs/cost_by_warehouse.csv", index=False)
monthly_trend.to_csv("outputs/monthly_trend.csv", index=False)

# KPIs
total_cost = monthly["total_stock_cost_eur"].sum()
total_waste = monthly["waste_cost_eur"].sum()
total_revenue = monthly["revenue_eur"].sum()
overall_waste_pct = total_waste / total_cost * 100

cat_rows = "".join([
    f"<tr><td>{r['category']}</td><td>€{r['total_stock_cost']:,.0f}</td><td>€{r['total_waste_cost']:,.0f}</td><td>{r['waste_pct']}%</td><td>{r['margin_pct']}%</td></tr>"
    for _, r in cost_by_category.sort_values("total_stock_cost", ascending=False).iterrows()
])
wh_rows = "".join([
    f"<tr><td>{r['warehouse']}</td><td>€{r['total_stock_cost']:,.0f}</td><td>€{r['total_storage_cost']:,.0f}</td><td>{r['efficiency_score']}%</td></tr>"
    for _, r in cost_by_warehouse.sort_values("efficiency_score", ascending=False).iterrows()
])
trend_rows = "".join([
    f"<tr><td>{r['month']}</td><td>€{r['total_cost']:,.0f}</td><td>€{r['total_waste']:,.0f}</td><td>€{r['total_revenue']:,.0f}</td><td>{r['reorders']}</td></tr>"
    for _, r in monthly_trend.iterrows()
])

html = f"""<!DOCTYPE html>
<html><head><meta charset='UTF-8'>
<title>Inventory Cost Dashboard — PHOENIX Group</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',sans-serif}}
body{{background:#F0FDF4;color:#1A1A1A}}
.header{{background:#0A1F0E;color:white;padding:28px 36px}}
.header h1{{font-size:22px;font-weight:700}}
.header p{{color:#86EFAC;font-size:13px;margin-top:4px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:24px 36px}}
.kpi{{background:white;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.08)}}
.kpi .val{{font-size:26px;font-weight:700;color:#1D8348}}
.kpi .lbl{{font-size:12px;color:#6B7280;margin-top:4px}}
.section{{padding:0 36px 24px}}
.section h2{{font-size:14px;font-weight:700;color:#145A32;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;border-bottom:2px solid #3DCD58;padding-bottom:6px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.card{{background:white;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.08)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;padding:8px 10px;background:#F0FDF4;color:#1D8348;font-weight:600}}
td{{padding:8px 10px;border-bottom:1px solid #F3F4F6}}
</style></head><body>
<div class='header'>
  <h1>Pharmaceutical Inventory Cost Dashboard</h1>
  <p>PHOENIX Group · Operational Controlling Analytics · MSc Project ECE Paris 2025–2026</p>
</div>
<div class='kpis'>
  <div class='kpi'><div class='val'>{N_PRODUCTS:,}</div><div class='lbl'>Products Tracked</div></div>
  <div class='kpi'><div class='val'>€{total_cost/1e6:.1f}M</div><div class='lbl'>Total Stock Cost (12M)</div></div>
  <div class='kpi'><div class='val'>€{total_waste/1e6:.2f}M</div><div class='lbl'>Total Waste Cost</div></div>
  <div class='kpi'><div class='val'>{overall_waste_pct:.2f}%</div><div class='lbl'>Waste Rate</div></div>
</div>
<div class='section'>
  <div class='grid2'>
    <div class='card'>
      <h2>Cost by Product Category</h2>
      <table><tr><th>Category</th><th>Stock Cost</th><th>Waste Cost</th><th>Waste %</th><th>Margin %</th></tr>{cat_rows}</table>
    </div>
    <div class='card'>
      <h2>Efficiency by Warehouse</h2>
      <table><tr><th>Warehouse</th><th>Stock Cost</th><th>Storage Cost</th><th>Efficiency</th></tr>{wh_rows}</table>
    </div>
  </div>
</div>
<div class='section'>
  <div class='card'>
    <h2>Monthly Cost Trend</h2>
    <table><tr><th>Month</th><th>Stock Cost</th><th>Waste Cost</th><th>Revenue</th><th>Reorders</th></tr>{trend_rows}</table>
  </div>
</div>
</body></html>"""

with open("outputs/inventory_dashboard.html", "w") as f:
    f.write(html)

print(f"Products: {N_PRODUCTS}, Months: {N_MONTHS}")
print(f"Total stock cost: €{total_cost:,.0f}")
print(f"Waste rate: {overall_waste_pct:.2f}%")
print("Dashboard saved to outputs/inventory_dashboard.html")
