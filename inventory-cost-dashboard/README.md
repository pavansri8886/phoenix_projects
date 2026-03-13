# Pharmaceutical Inventory Cost Dashboard
**MSc Data Management & AI — ECE Paris 2025–2026**

Inventory cost monitoring and waste analysis across product categories and warehouse locations, designed for operational controlling teams in pharmaceutical distribution.

## Business Problem
Tracking where inventory cost is accumulating, identifying waste hotspots by product category and warehouse, and monitoring monthly cost trends to support controlling decisions.

## What It Does
- Generates 500 pharmaceutical products across 6 categories and 6 warehouse locations
- Simulates 12 months of inventory movement including stock levels, sales, expiry and reorder events
- Calculates waste rate, storage efficiency and margin by category
- Produces warehouse efficiency scorecard
- Tracks monthly cost and revenue trends with reorder frequency
- Outputs structured CSVs ready for Power BI import

## Stack
- Python · pandas · NumPy
- SQL Server compatible
- HTML Dashboard

## Outputs
| File | Description |
|---|---|
| `outputs/cost_by_category.csv` | Stock cost, waste cost, waste % and margin by product category |
| `outputs/cost_by_warehouse.csv` | Storage cost and efficiency score by warehouse |
| `outputs/monthly_trend.csv` | 12-month cost, waste and revenue trend |
| `outputs/inventory_dashboard.html` | Management dashboard |

## How to Run
```bash
pip install pandas numpy
python inventory_analysis.py
open outputs/inventory_dashboard.html
```

## Power BI Integration
Import all CSV outputs into Power BI. Recommended visuals:
- Clustered bar: waste cost by category
- Line chart: monthly cost trend
- Matrix: warehouse efficiency scorecard
- KPI cards: total cost, waste rate, revenue
