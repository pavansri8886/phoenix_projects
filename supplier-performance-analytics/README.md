# Supplier Performance & Negotiation Analytics

Built this as part of my MSc in Data Management and AI at ECE Paris (2025–2026).

The motivation was straightforward — commercial teams negotiate with suppliers every year, but those negotiations are often based on incomplete or anecdotal performance data. I wanted to build a scorecard system that gave the commercial team an objective view of every supplier before entering price discussions, so the negotiation starts from a position of evidence rather than gut feel.

---

## What I built

A supplier performance scorecard covering 40 suppliers across 5 pharmaceutical product categories and 7 countries, based on 3,000 simulated purchase orders over 12 months.

Each supplier gets a weighted performance score built from four metrics: on-time delivery rate (35%), quality pass rate (35%), invoice accuracy (20%) and defect rate (10%). The weighting reflects what actually matters in pharmaceutical distribution — delivery reliability and quality compliance are non-negotiable, invoicing issues are costly but recoverable.

The score then maps each supplier to a negotiation priority tier: Preferred Partner, Monitor, Improvement Plan or Immediate Review. The idea is that the commercial team walks into every negotiation knowing exactly which tier their counterpart sits in and why.

The category benchmarks were an addition I found useful — they show average performance by product category, so you can tell whether a supplier's 78% on-time rate is acceptable for that category or below market standard.

---

## Stack

Python · pandas · NumPy · SQL Server compatible · HTML dashboard

---

## How to run

```bash
pip install pandas numpy
python supplier_analysis.py
```

Open `outputs/supplier_dashboard.html` to see the full dashboard. Import `supplier_scorecard.csv` and `category_benchmarks.csv` into Power BI for interactive scatter plots and drill-down by country and category.

---

## What I would do next

Add a price competitiveness layer — right now the scorecard only covers delivery, quality and invoicing. Connecting it to unit price benchmarks by category would let the commercial team see whether a high-performing supplier is also priced competitively, or whether their reliability premium has become too expensive.
