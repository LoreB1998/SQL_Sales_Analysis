/*
Customer Revenue By Cohort
Yearly Cohort Analysis
*/
SELECT cohort_year,
       COUNT(DISTINCT customerkey) AS total_customers,
       SUM(total_net_revenue)::numeric(10,2) AS total_revenue,
       (SUM(total_net_revenue) / COUNT(DISTINCT customerkey))::numeric(10,2) AS customer_revenue
FROM cohort_analysis
WHERE orderdate = first_purchase_date
GROUP BY cohort_year;

/*
BONUS: Investigate Monthly Revenue & Customer Trends
• Calculate the monthly revenue and customer trends to explore why we are seeing customers spend less over time.
• Could this be attributed to seasonal trends?
*/

SELECT DATE_TRUNC('month', orderdate)::date AS year_month,
       COUNT(DISTINCT customerkey) AS total_customers,
       SUM(total_net_revenue)::numeric(10,2) AS total_revenue,
       (SUM(total_net_revenue) / COUNT(DISTINCT customerkey))::numeric(10,2) AS customer_revenue
FROM cohort_analysis
GROUP BY year_month;