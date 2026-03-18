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
       SUM(total_ltv) AS total_ltv
FROM segment_values
GROUP BY customer_segment
ORDER BY customer_segment DESC;





