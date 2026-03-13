# Pharmaceutical Inventory Cost Dashboard

Built this as part of my MSc in Data Management and AI at ECE Paris (2025–2026).

I was interested in the operational controlling side of pharmaceutical distribution — specifically how a company managing 70,000+ pharmacy accounts tracks where inventory cost is accumulating and where waste is happening. Expired stock in pharma is not just a cost problem, it is also a compliance issue. I wanted to build something that made that visible at a glance.

---

## What I built

An inventory cost monitoring system covering 500 products across 6 categories and 6 warehouse locations, simulating 12 months of stock movement including sales, expiry events and reorder triggers.

The analysis calculates waste rate and storage efficiency per category and per warehouse, then tracks how both metrics move month by month. The warehouse efficiency scorecard was the most interesting output — some locations had significantly better waste rates than others even within the same product category, which in a real environment would immediately raise questions about storage conditions, stock rotation practices and supplier delivery timing.

The CSVs are structured to drop straight into Power BI for interactive drill-down.

---

## Stack

Python · pandas · NumPy · SQL Server compatible · HTML dashboard

---

## How to run

```bash
pip install pandas numpy
python inventory_analysis.py
```

Open `outputs/inventory_dashboard.html` to see the full dashboard. Import the CSVs in the `outputs/` folder into Power BI for interactive visuals.

---

## What I would do next

Add a reorder optimisation layer — right now the model flags when reorders are triggered but does not suggest optimal reorder quantities. Connecting stock velocity data with supplier lead times would let you calculate the right reorder point per product to minimise both stockout risk and waste.
