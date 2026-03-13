# Customer Churn Analytics
**MSc Data Management & AI — ECE Paris 2025–2026**

Churn prediction model for pharmaceutical wholesale customers, built to support commercial team negotiation strategy at enterprise scale.

## Business Problem
Identifying which pharmacy clients are at risk of churning before they leave — enabling the commercial team to intervene with targeted retention strategies and informed negotiation positions.

## What It Does
- Generates synthetic dataset of 2,000 pharmacy customers across 7 German regions and 4 segments
- Trains a Random Forest classifier to predict churn probability per customer
- Classifies customers into risk tiers: Critical, High Risk, Medium Risk, Low Risk
- Quantifies monthly revenue at risk by region and segment
- Analyses discount rate effectiveness vs churn outcomes
- Produces an executive HTML dashboard for commercial team review

## Stack
- Python · pandas · scikit-learn · NumPy
- SQL (SQL Server compatible queries in `analysis.sql`)
- HTML Dashboard

## Outputs
| File | Description |
|---|---|
| `outputs/churn_by_region.csv` | Churn rate and average order value by region |
| `outputs/churn_by_segment.csv` | Churn rate and average order value by segment |
| `outputs/feature_importance.csv` | Top churn predictors from Random Forest model |
| `outputs/risk_tiers.csv` | Revenue at risk by customer risk tier |
| `outputs/churn_dashboard.html` | Executive dashboard for commercial review |

## Key Results
- Model AUC: ~0.87
- Top churn predictors: days since last order, NPS score, late payments
- Revenue at risk quantified by region for negotiation prioritisation

## How to Run
```bash
pip install pandas numpy scikit-learn
python churn_analysis.py
open outputs/churn_dashboard.html
```

## Power BI Integration
Import `outputs/churn_by_region.csv`, `churn_by_segment.csv` and `risk_tiers.csv` directly into Power BI for interactive visualisation and drill-down by region, segment and risk tier.
