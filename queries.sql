-- Retail Sales Analytics: SQL queries
-- Assumed table name: sales
-- Adjust date functions to your SQL database if needed.

-- 1. Overall KPIs
SELECT
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    COUNT(DISTINCT Order_ID) AS total_orders,
    SUM(Quantity) AS total_units,
    100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0) AS profit_margin_pct
FROM sales;

-- 2. Sales and profit by category
SELECT Category, SUM(Sales) AS total_sales, SUM(Profit) AS total_profit
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;

-- 3. Sales and profit by region
SELECT Region, SUM(Sales) AS total_sales, SUM(Profit) AS total_profit
FROM sales
GROUP BY Region
ORDER BY total_profit DESC;

-- 4. Monthly sales trend (PostgreSQL)
SELECT DATE_TRUNC('month', CAST(Order_Date AS date)) AS sales_month,
       SUM(Sales) AS monthly_sales
FROM sales
GROUP BY 1
ORDER BY 1;

-- 5. Products with lowest total profit
SELECT Product_Name, SUM(Sales) AS total_sales, SUM(Profit) AS total_profit
FROM sales
GROUP BY Product_Name
ORDER BY total_profit ASC
LIMIT 10;

-- 6. Discount bands (portable CASE expression)
SELECT
    CASE
      WHEN Discount <= 0.05 THEN '0-5%'
      WHEN Discount <= 0.15 THEN '5-15%'
      WHEN Discount <= 0.30 THEN '15-30%'
      ELSE '30%+'
    END AS discount_band,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    AVG(Profit) AS average_profit
FROM sales
WHERE Discount IS NOT NULL
GROUP BY 1
ORDER BY 1;
