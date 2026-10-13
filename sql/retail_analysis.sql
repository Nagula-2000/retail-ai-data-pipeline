-- Run after loading outputs/clean_sales.csv into a SQL table named clean_sales.
-- Revenue and transaction count by store
SELECT store_id, COUNT(*) AS transactions, ROUND(SUM(revenue), 2) AS revenue
FROM clean_sales
GROUP BY store_id
ORDER BY revenue DESC;

-- Top-selling products by revenue
SELECT product, SUM(quantity) AS units_sold, ROUND(SUM(revenue), 2) AS revenue
FROM clean_sales
GROUP BY product
ORDER BY revenue DESC;
