-- ============================================================
-- Customer Churn Analytics — SQL Analysis Scripts
-- PHOENIX Group Operational Controlling Analytics
-- Compatible with SQL Server Management Studio
-- ============================================================

-- 1. Churn rate by region and segment
SELECT
    region,
    segment,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(CAST(SUM(churned) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(monthly_order_value_eur), 2) AS avg_monthly_value_eur,
    ROUND(AVG(nps_score), 2) AS avg_nps
FROM customers
GROUP BY region, segment
ORDER BY churn_rate_pct DESC;

-- 2. High-risk customers for commercial team negotiation
SELECT
    customer_id,
    segment,
    region,
    monthly_order_value_eur,
    late_payments_last_12m,
    last_order_days_ago,
    nps_score,
    support_tickets_last_6m,
    CASE
        WHEN late_payments_last_12m > 6 AND nps_score < 5 THEN 'CRITICAL'
        WHEN late_payments_last_12m > 3 OR last_order_days_ago > 45 THEN 'HIGH RISK'
        WHEN nps_score < 6 OR support_tickets_last_6m > 10 THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END AS risk_tier
FROM customers
WHERE churned = 0
ORDER BY monthly_order_value_eur DESC;

-- 3. Revenue at risk by region
SELECT
    region,
    COUNT(*) AS customers_at_risk,
    ROUND(SUM(monthly_order_value_eur), 2) AS monthly_revenue_at_risk_eur,
    ROUND(SUM(monthly_order_value_eur) * 12, 2) AS annual_revenue_at_risk_eur
FROM customers
WHERE churned = 1
GROUP BY region
ORDER BY annual_revenue_at_risk_eur DESC;

-- 4. Discount effectiveness vs churn
SELECT
    CASE
        WHEN discount_rate < 0.05 THEN '0-5%'
        WHEN discount_rate < 0.10 THEN '5-10%'
        WHEN discount_rate < 0.15 THEN '10-15%'
        ELSE '15%+'
    END AS discount_band,
    COUNT(*) AS customers,
    ROUND(AVG(CAST(churned AS FLOAT)) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(monthly_order_value_eur), 2) AS avg_order_value
FROM customers
GROUP BY
    CASE
        WHEN discount_rate < 0.05 THEN '0-5%'
        WHEN discount_rate < 0.10 THEN '5-10%'
        WHEN discount_rate < 0.15 THEN '10-15%'
        ELSE '15%+'
    END
ORDER BY discount_band;

-- 5. Monthly order value distribution for active customers
SELECT
    segment,
    ROUND(MIN(monthly_order_value_eur), 2) AS min_value,
    ROUND(AVG(monthly_order_value_eur), 2) AS avg_value,
    ROUND(MAX(monthly_order_value_eur), 2) AS max_value,
    ROUND(STDEV(monthly_order_value_eur), 2) AS std_dev,
    COUNT(*) AS customer_count
FROM customers
WHERE churned = 0
GROUP BY segment;
