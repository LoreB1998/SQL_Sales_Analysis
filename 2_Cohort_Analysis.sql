/*
 Q2: Cohort Analysis
How do different groups generate revenue?
 */

/*
Customer Revenue By Cohort
Yearly Cohort Analysis
*/
SELECT cohort_year,
       SUM(total_net_revenue)::numeric(10,2) AS total_revenue,
       COUNT(DISTINCT customerkey) AS total_customers,
       (SUM(total_net_revenue) / COUNT(DISTINCT customerkey))::numeric(10,2) AS customer_revenue
FROM cohort_analysis
GROUP BY cohort_year;

/*
Customer Revenue by Cohort (Adjusted for Time in Market)
Revenue share by days since first purchase
*/
WITH purchase_days AS (
    SELECT customerkey,
           total_net_revenue,
           orderdate - MIN(orderdate) OVER (PARTITION BY customerkey) AS days_since_first_purchase
    FROM cohort_analysis
)

SELECT days_since_first_purchase,
       SUM(total_net_revenue) AS total_revenue,
       (SUM(total_net_revenue) / (SELECT SUM(total_net_revenue) FROM cohort_analysis) * 100) AS percentage_of_total_revenue,
       SUM(SUM(total_net_revenue) / (SELECT SUM(total_net_revenue) FROM cohort_analysis) * 100)
           OVER (ORDER BY days_since_first_purchase) AS cumulative_percentage_of_total_revenue
FROM purchase_days
GROUP BY days_since_first_purchase
ORDER BY days_since_first_purchase;

/*
Customer Revenue By Cohort (Only First Purchase Date)
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