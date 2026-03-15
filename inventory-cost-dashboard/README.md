# 📦 Inventory Cost Intelligence Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square&logo=pandas)
![HTML](https://img.shields.io/badge/Dashboard-HTML%20%2F%20CSS-E34F26?style=flat-square&logo=html5)
![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-181717?style=flat-square&logo=github)

**An inventory analytics pipeline that identifies where capital is locked, which categories and warehouses carry the highest cost burden, and how inventory trends move month over month.**

</div>

---

## 🧠 The Problem

A product sitting in a warehouse is not neutral — it has a holding cost, a reorder risk, and a category concentration. Without visibility across these dimensions simultaneously, operations teams cannot tell whether rising inventory cost is a category problem, a warehouse problem, or a procurement problem.

This project was built to answer those questions cleanly and automatically from raw inventory data.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  INPUT DATA LAYER                   │
│                                                     │
│   monthly_inventory.csv   →  stock levels by month │
│   products.csv            →  product master data   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│           inventory_analysis.py                     │
│                                                     │
│  ① Data ingestion and merging                       │
│  ② Inventory cost calculation per SKU               │
│  ③ Category-level cost aggregation                  │
│  ④ Warehouse-level cost distribution                │
│  ⑤ Monthly trend computation                        │
│  ⑥ HTML dashboard generation                        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                  OUTPUT LAYER                       │
│                                                     │
│  cost_by_category.csv    →  category cost report   │
│  cost_by_warehouse.csv   →  warehouse cost report  │
│  monthly_trend.csv       →  trend over time        │
│  inventory_dashboard.html→  interactive dashboard  │
└─────────────────────────────────────────────────────┘
```

---

## 📊 What the Dashboard Shows

### Cost by Category
Breaks down total inventory cost across product categories, identifying which categories account for disproportionate capital relative to their stock volume.

### Cost by Warehouse
Distributes inventory cost across warehouse locations, surfacing concentration risks where a single site carries excess capital exposure.

### Monthly Inventory Trend
Tracks how inventory cost evolves month over month, helping operations teams detect seasonal build-up, procurement spikes, or drawdown patterns.

---

## ⚙️ Core Metrics Computed

```python
# Inventory value per SKU
inventory_value = stock_quantity * unit_cost

# Category cost aggregation
cost_by_category = df.groupby("category")["inventory_value"].sum()

# Warehouse cost distribution
cost_by_warehouse = df.groupby("warehouse")["inventory_value"].sum()

# Monthly trend
monthly_trend = df.groupby("month")["inventory_value"].sum()
```

---

## 📁 Repository Structure

```
inventory-cost-dashboard/
│
├── 📂 data/
│   ├── monthly_inventory.csv     # Monthly stock level records
│   └── products.csv              # Product master data (SKU, cost, category)
│
├── 📂 outputs/
│   ├── cost_by_category.csv      # Category-level cost breakdown
│   ├── cost_by_warehouse.csv     # Warehouse-level cost breakdown
│   ├── monthly_trend.csv         # Month-over-month inventory trend
│   └── inventory_dashboard.html  # Interactive HTML dashboard
│
├── inventory_analysis.py         # Main pipeline script
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

# Run the full pipeline
python inventory_analysis.py

# Open the dashboard
open outputs/inventory_dashboard.html
```

---

## 🔮 Planned Enhancements

- [ ] Stock status classification — Overstock, Balanced, Understock per SKU
- [ ] Reorder alert system for SKUs below threshold
- [ ] Demand forecasting layer for forward-looking inventory planning
- [ ] Supplier concentration analysis integration

---

## 👤 Author

**Pavan Kumar Naganaboina**
MSc Data Management & AI — ECE Paris 2025–2026
[LinkedIn](https://linkedin.com/in/pavankumarn01) · [GitHub](https://github.com/pavansri8886)
