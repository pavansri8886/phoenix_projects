"""
Customer Churn Analytics — Data Generation
PHOENIX Group Operational Controlling Analytics Project
Generates synthetic pharmacy customer data for churn prediction modelling
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

N = 2000

regions = ["Baden-Württemberg", "Bavaria", "NRW", "Hesse", "Saxony", "Hamburg", "Berlin"]
segments = ["Independent Pharmacy", "Chain Pharmacy", "Hospital Pharmacy", "Online Pharmacy"]
payment_terms = ["Net 30", "Net 60", "Net 90", "Immediate"]

def generate_customer_data():
    data = []
    for i in range(N):
        region = random.choice(regions)
        segment = random.choice(segments)
        contract_start = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1000))
        monthly_order_value = round(np.random.lognormal(8.5, 0.8), 2)
        order_frequency = random.randint(2, 30)
        late_payments = random.randint(0, 12)
        support_tickets = random.randint(0, 20)
        discount_rate = round(random.uniform(0.02, 0.18), 3)
        contract_duration = random.randint(6, 48)
        last_order_days_ago = random.randint(1, 90)
        nps_score = random.randint(1, 10)
        product_categories = random.randint(1, 8)

        # Churn logic - based on realistic signals
        churn_score = 0
        if late_payments > 6: churn_score += 2
        if support_tickets > 12: churn_score += 2
        if last_order_days_ago > 45: churn_score += 3
        if nps_score < 5: churn_score += 2
        if monthly_order_value < 2000: churn_score += 1
        if order_frequency < 5: churn_score += 1
        churn_score += random.randint(-2, 2)
        churned = 1 if churn_score >= 5 else 0

        data.append({
            "customer_id": f"CUST{str(i+1).zfill(5)}",
            "region": region,
            "segment": segment,
            "contract_start": contract_start.strftime("%Y-%m-%d"),
            "contract_duration_months": contract_duration,
            "monthly_order_value_eur": monthly_order_value,
            "order_frequency_per_month": order_frequency,
            "late_payments_last_12m": late_payments,
            "support_tickets_last_6m": support_tickets,
            "discount_rate": discount_rate,
            "last_order_days_ago": last_order_days_ago,
            "nps_score": nps_score,
            "product_categories_ordered": product_categories,
            "payment_terms": random.choice(payment_terms),
            "churned": churned
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_customer_data()
    df.to_csv("data/customers_raw.csv", index=False)
    print(f"Generated {len(df)} customer records")
    print(f"Churn rate: {df['churned'].mean():.1%}")
    print(f"Regions: {df['region'].nunique()}")
    print(f"Segments: {df['segment'].value_counts().to_dict()}")
