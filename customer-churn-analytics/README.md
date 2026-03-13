# Customer Churn Analytics — Pharmacy Client Risk Modelling

Built this as part of my MSc in Data Management and AI at ECE Paris (2025–2026).

The idea came from thinking about how pharmaceutical wholesalers manage thousands of pharmacy clients across multiple countries. Losing a high-value client is expensive — not just the revenue but the cost of replacing them. I wanted to see if churn could be predicted early enough for a commercial team to act before the client actually leaves.

---

## What I built

A full churn prediction pipeline — from raw data through to a machine learning model and an executive dashboard the commercial team could actually use.

The dataset covers 2,000 pharmacy customers across 7 German regions and 4 segments (independent, chain, hospital and online pharmacies). I generated it synthetically but modelled the churn logic on realistic signals: late payment history, NPS scores, days since last order, support ticket volume and order frequency.

The model is a Random Forest classifier. It ended up with an AUC of 0.916. The top predictors turned out to be days since last order, NPS score and late payment count — which makes sense. A customer who has not ordered in 6 weeks and rates you 3/10 is probably already talking to a competitor.

The output I was most interested in was the revenue at risk breakdown by region. Rather than just flagging churned customers, I wanted to show the commercial team where to focus negotiation efforts first based on actual money at risk.

---

## Stack

Python · pandas · scikit-learn · SQL (SQL Server compatible) · HTML dashboard

---

## How to run

```bash
pip install pandas numpy scikit-learn
python churn_analysis.py
```

Open `outputs/churn_dashboard.html` in your browser. The SQL scripts in `analysis.sql` cover churn by region, high-risk customer identification, revenue at risk and discount effectiveness — written for SQL Server Management Studio.

---

## What I would do next

The real value would come from integrating actual CRM and order data. I would also add a time-series component — right now the model treats customers statically, but churn prediction gets much stronger when you can track the trajectory of behaviour over time.
