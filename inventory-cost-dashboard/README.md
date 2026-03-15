# 📦 Inventory Cost Intelligence Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square&logo=pandas)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat-square&logo=powerbi)
![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-181717?style=flat-square&logo=github)

**An operational inventory intelligence system that identifies where capital is locked, which suppliers dominate stock exposure, and where stockout or overstock risk is highest.**

</div>

---

## 🧠 The Problem

Most companies know their inventory *exists*. Few know what it's *costing* them.

A product sitting in a warehouse isn't neutral — it has a holding cost, a reorder risk, and a supplier dependency. Without visibility into these dimensions simultaneously, operations teams are flying blind on one of their largest capital expenditures.

This dashboard was built to answer three questions that traditional inventory reports miss:

> 1. Which products are locking the most capital relative to their sales velocity?
> 2. Which suppliers create the highest stock concentration risk?
> 3. Where are we closest to a stockout or overstock event right now?

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  RAW SUPPLY CHAIN DATA                  │
│         supply_chain_dataset.csv (multi-source)         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              PYTHON PROCESSING LAYER                    │
│                                                         │
│  ① Data Cleaning        → null handling, type casting  │
│  ② Feature Engineering  → cost metrics, ratios         │
│  ③ Stock Classification → Overstock / Balanced /       │
│                           Understock per SKU           │
│  ④ Supplier Scoring     → concentration index          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               METRICS CALCULATION ENGINE                │
│                                                         │
│  inventory_value    = stock_qty × unit_cost             │
│  holding_cost_total = inventory_value × holding_rate    │
│  inventory_turnover = COGS / avg_inventory              │
│  reorder_risk       = stock_qty < reorder_level         │
│  cost_velocity_gap  = inventory_value / revenue         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              POWER BI DASHBOARD LAYER                   │
│                                                         │
│  • Inventory Value by Category (treemap)                │
│  • Supplier Concentration (bar + %)                     │
│  • Stock Status Distribution (donut)                    │
│  • Regional Inventory Heatmap                           │
│  • Cost Hotspot Table (ranked SKUs)                     │
│  • Replenishment Alert Panel                            │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Dashboard Panels

### 1. Inventory Value Distribution
Shows how total inventory capital is allocated across product categories. Identifies which categories account for disproportionate stock value relative to revenue contribution.

### 2. Supplier Concentration Risk
Maps which suppliers control the largest share of active inventory. A single supplier accounting for >30% of stock value is flagged as a concentration risk.

### 3. Stock Status Classification

| Status | Condition | Action |
|--------|-----------|--------|
| 🔴 Understock | `stock_qty < reorder_level` | Immediate replenishment |
| 🟡 Balanced | `stock_qty ≈ reorder_level` | Monitor closely |
| 🟢 Overstock | `stock_qty >> reorder_level` | Review purchasing |

### 4. Cost Hotspot Table
Ranks SKUs by `inventory_value / revenue` ratio. Products with high inventory cost but low sales velocity are flagged as capital inefficiencies — the primary targets for operational action.

### 5. Regional Inventory Heatmap
Shows geographic distribution of stock across distribution locations. Identifies concentration in single warehouses and highlights redistribution opportunities.

### 6. Replenishment Alert Panel
Live panel showing all SKUs currently below reorder level, sorted by risk priority. Feeds directly into procurement planning.

---

## ⚙️ Key Metrics

```python
# Inventory Value
inventory_value = stock_quantity * unit_cost

# Total Holding Cost
holding_cost_total = inventory_value * holding_cost_rate

# Inventory Turnover Ratio
inventory_turnover = cost_of_goods_sold / average_inventory

# Cost-to-Revenue Ratio (inefficiency signal)
cost_velocity_gap = inventory_value / revenue

# Stock Classification
def classify_stock(stock_qty, reorder_level):
    if stock_qty < reorder_level:
        return "UNDERSTOCK"
    elif stock_qty <= reorder_level * 1.5:
        return "BALANCED"
    else:
        return "OVERSTOCK"
```

---

## 📁 Repository Structure

```
inventory-cost-dashboard/
│
├── 📂 data/
│   └── supply_chain_dataset.csv       # Raw operational dataset
│
├── 📂 notebooks/
│   └── data_cleaning.ipynb            # Preprocessing and EDA
│
├── 📂 src/
│   ├── feature_engineering.py         # Metrics calculation
│   ├── stock_classifier.py            # Status classification logic
│   └── cost_analysis.py               # Cost hotspot detection
│
├── 📂 dashboard/
│   └── inventory_dashboard.pbix       # Power BI report file
│
├── 📂 outputs/
│   ├── cost_hotspots.csv              # Ranked inefficiency report
│   ├── replenishment_alerts.csv       # Reorder needed SKUs
│   └── supplier_concentration.csv     # Supplier risk summary
│
└── README.md
```

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/pavansri8886/phoenix_projects.git
cd phoenix_projects/inventory-cost-dashboard

# Install dependencies
pip install pandas numpy

# Run the analysis pipeline
python src/feature_engineering.py
python src/stock_classifier.py
python src/cost_analysis.py

# Open Power BI dashboard
# Open dashboard/inventory_dashboard.pbix in Power BI Desktop
```

---

## 🔮 Planned Enhancements

- [ ] Demand forecasting integration (ARIMA / Prophet)
- [ ] Automated anomaly detection for stock spikes
- [ ] Real-time pipeline via API integration (Shopify / ERP)
- [ ] Slack / email alert triggers for replenishment events

---

## 👤 Author

**Pavan Kumar Naganaboina**
MSc Data Management & AI — ECE Paris 2025–2026
[LinkedIn](https://linkedin.com/in/pavankumarn01) · [GitHub](https://github.com/pavansri8886)
