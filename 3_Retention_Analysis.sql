/*
Q2: Cohort Analysis
How do different groups generate revenue?
*/

/*
 Business Terms:
• Active Customer: Customer who made a purchase within the last 6 months
• Churned Customer: Customer who hasn't made a purchase in over 6 months
What is the Churn Period?:
• - E-commerce → 6-12 months since last purchase (Contoso is an e-commerce company)
• • SaaS & Subscription Services → 30-90 days since last login/payment
•
•
Mobile Apps→ 7-30 days since last session
B2B Businesses → 6-12 months since last transaction
Why It Matters: Helps track customer retention and engagement
• Identifies at-risk customers before they fully churn
• Enables targeted re-engagement campaigns
• Measures effectiveness of retention strategies
• Provides insights into customer lifecycle
*/

WITH customer_last_purchase AS (SELECT customerkey,
                                       cleaned_name,
                                       orderdate,
                                       ROW_NUMBER() OVER (PARTITION BY customerkey ORDER BY orderdate DESC) AS rn,
                                       first_purchase_date,
                                       cohort_year
                                FROM cohort_analysis),
     churned_customer AS (SELECT customerkey,
                                 cleaned_name,
                                 orderdate AS last_purchase_date,
                                 CASE
                                     WHEN orderdate < (SELECT MAX(orderdate) FROM sales) - INTERVAL '6 month'
                                         THEN 'Churned'
                                     ELSE 'Active'
                                     END   AS customer_status,
                                 cohort_year
                          FROM customer_last_purchase
                          WHERE rn = 1
                            AND first_purchase_date < (SELECT MAX(orderdate) FROM sales) - INTERVAL '6 month')
-- Churned Rate Per Cohort Year
SELECT cohort_year,
       customer_status,
       COUNT(customerkey)                                                                     AS num_customers,
       SUM(COUNT(customerkey)) OVER (PARTITION BY cohort_year)                                AS total_customers,
       ROUND(COUNT(customerkey) / SUM(COUNT(customerkey)) OVER (PARTITION BY cohort_year), 2) AS status_pct
FROM churned_customer
GROUP BY cohort_year, customer_status;


