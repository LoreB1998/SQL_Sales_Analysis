DROP VIEW cohort_analysis;

-- CREATE OR REPLACE VIEW cohort_analysis AS
WITH customer_revenue AS (SELECT s.customerkey,
                                 s.orderdate,
                                 SUM(s.quantity * s.netprice / s.exchangerate) AS total_net_revenue,
                                 COUNT(s.orderkey)                             AS num_orders,
                                 c.countryfull,
                                 c.age,
                                 c.givenname,
                                 c.surname
                          FROM sales s
                                   LEFT JOIN public.customer c on c.customerkey = s.customerkey
                          GROUP BY s.customerkey, c.customerkey, s.orderdate, c.countryfull, s.orderdate, s.customerkey,
                                   c.age, c.givenname, c.surname)
SELECT customerkey,
       orderdate,
       total_net_revenue,
       num_orders,
       countryfull,
       age,
       CONCAT(TRIM(givenname), ' ', TRIM(surname))                             AS cleaned_name,
       MIN(cr.orderdate) OVER (PARTITION BY cr.customerkey)                    AS first_purchase_date,
       EXTRACT(YEAR FROM MIN(cr.orderdate) OVER (PARTITION BY cr.customerkey)) AS cohort_year
FROM customer_revenue cr;

/*
 Optimized View
 */

CREATE OR REPLACE VIEW cohort_analysis AS
WITH customer_revenue AS (SELECT s.customerkey,
                                 s.orderdate,
                                 SUM(s.quantity * s.netprice / s.exchangerate)   AS total_net_revenue,
                                 COUNT(s.orderkey)                               AS num_orders,
                                 MAX(c.countryfull) AS countryfull,
                                 MAX(c.age) AS age,
                                 CONCAT(TRIM(c.givenname), ' ', TRIM(c.surname)) AS cleaned_name
                          FROM sales s
                                   INNER JOIN public.customer c on c.customerkey = s.customerkey
                          GROUP BY s.customerkey, c.customerkey, s.orderdate)
SELECT cr.*,
       MIN(cr.orderdate) OVER (PARTITION BY cr.customerkey)                    AS first_purchase_date,
       EXTRACT(YEAR FROM MIN(cr.orderdate) OVER (PARTITION BY cr.customerkey)) AS cohort_year
FROM customer_revenue cr;


