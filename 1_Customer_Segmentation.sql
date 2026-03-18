/*
 Q1: Customer Segmentation
Who are our most valuable customers?
 */

/*
Customer Segmentation
*/
WITH customer_ltv AS (SELECT customerkey,
                             cleaned_name,
                             SUM(total_net_revenue)::numeric(10, 2) as total_ltv
                      FROM cohort_analysis
                      GROUP BY customerkey, cleaned_name),
     customer_segments AS (SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_ltv) AS percentile_25,
                                  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_ltv) AS percentile_75
                           FROM customer_ltv),
     segment_values AS (SELECT c.*,
                               CASE
                                   WHEN c.total_ltv < cs.percentile_25 THEN '1 - Low-Value'
                                   WHEN c.total_ltv > cs.percentile_75 THEN '3 - High-Value'
                                   ELSE '2 - Mid-Value'
                                   END AS customer_segment
                        FROM customer_ltv c
                                 CROSS JOIN customer_segments cs)
SELECT customer_segment,
       SUM(total_ltv) AS total_ltv,
       COUNT(customerkey) AS customer_count,
       (SUM(total_ltv) / COUNT(customerkey))::numeric(10,2) AS avg_ltv
FROM segment_values
GROUP BY customer_segment
ORDER BY customer_segment DESC;

/*
• High-value segment (25% of customers)
drives 66% of revenue ($135.4M)
• Mid-value segment (50% of customers)
generates 32% of revenue ($66.6M)
• Low-value segment (25% of customers)
accounts for 2% of revenue ($4.3M)

Example:

• High-Value (66% revenue):
• Offer premium membership program to 12,372 VIP customers
• Provide early access to new products and dedicated support
• Focus on retention as losing one customer impacts revenue significantly
• Mid-Value (32% revenue):
• Create upgrade paths for 24,743 customers through personalized promotions
• Target with "next best product" recommendations based on high-value patterns
• Potential $66.6M → $135.4M revenue opportunity if upgraded to high-value
• Low-Value (2% revenue):
• Design re-engagement campaigns for 12,372 customers to increase purchase frequency
• Test price-sensitive promotion to encourage more frequent purchases
• Focus on converting $4.3M segment to mid-value through targeted offers
*/








