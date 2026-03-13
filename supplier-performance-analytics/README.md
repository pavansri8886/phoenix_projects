# Supplier Performance & Negotiation Analytics
**MSc Data Management & AI — ECE Paris 2025–2026**

Supplier scorecard system supporting commercial team negotiation strategy through performance benchmarking, risk classification and spend analysis.

## Business Problem
Giving commercial teams an objective, data-driven view of supplier performance before entering price negotiations — identifying preferred partners, suppliers requiring improvement plans and those needing immediate review.

## What It Does
- Models 40 suppliers across 5 pharmaceutical categories and 7 countries
- Simulates 3,000 purchase orders with delivery, quality and invoicing outcomes
- Calculates a weighted performance score: on-time delivery (35%), quality pass rate (35%), invoice accuracy (20%), defect rate (10%)
- Assigns negotiation priority tier: Preferred Partner, Monitor, Improvement Plan, Immediate Review
- Benchmarks performance by product category
- Produces an executive scorecard dashboard

## Stack
- Python · pandas · NumPy
- SQL Server compatible
- HTML Dashboard

## Outputs
| File | Description |
|---|---|
| `outputs/supplier_scorecard.csv` | Full scorecard with performance scores and negotiation priority |
| `outputs/category_benchmarks.csv` | Average KPIs by product category |
| `outputs/supplier_dashboard.html` | Executive negotiation dashboard |

## Scoring Methodology
| Metric | Weight | Rationale |
|---|---|---|
| On-time delivery rate | 35% | Direct impact on pharmacy supply continuity |
| Quality pass rate | 35% | Core compliance requirement |
| Invoice accuracy | 20% | Controlling overhead and payment disputes |
| Defect rate | 10% | Secondary quality signal |

## How to Run
```bash
pip install pandas numpy
python supplier_analysis.py
open outputs/supplier_dashboard.html
```

## Power BI Integration
Import `supplier_scorecard.csv` and `category_benchmarks.csv` into Power BI. Recommended visuals:
- Scatter plot: on-time rate vs quality score, sized by spend
- Bar chart: performance score by supplier
- Matrix: negotiation priority by category and country
- KPI cards: avg on-time, avg quality, total spend
