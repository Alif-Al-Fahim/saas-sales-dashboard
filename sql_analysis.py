import pandas as pd
import sqlite3

# Fix path - use raw string
df = pd.read_csv(r"D:\practice_datasets\SaaS-Sales.csv")

# Clean column names (remove spaces)
df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

# Connect to SQLite (creates a local DB file)
conn = sqlite3.connect("saas_sales.db")

# Load dataframe into SQL table
df.to_sql("sales", conn, if_exists="replace", index=False)

print("✅ Data loaded into SQLite successfully!")
print(f"Total rows: {len(df)}")

# ──────────────────────────────────────────
# QUERY 1: Total Revenue, Profit, Orders
# ──────────────────────────────────────────
q1 = pd.read_sql_query("""
    SELECT 
        ROUND(SUM(sales), 2)    AS total_revenue,
        ROUND(SUM(profit), 2)   AS total_profit,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity)           AS total_units_sold
    FROM sales
""", conn)
print("\n📊 KPI Summary:")
print(q1)

# ──────────────────────────────────────────
# QUERY 2: Revenue & Profit by Region
# ──────────────────────────────────────────
q2 = pd.read_sql_query("""
    SELECT 
        region,
        ROUND(SUM(sales), 2)  AS revenue,
        ROUND(SUM(profit), 2) AS profit,
        COUNT(*)              AS transactions
    FROM sales
    GROUP BY region
    ORDER BY revenue DESC
""", conn)
print("\n🌍 Revenue by Region:")
print(q2)

# ──────────────────────────────────────────
# QUERY 3: Top 10 Products by Revenue
# ──────────────────────────────────────────
q3 = pd.read_sql_query("""
    SELECT 
        product,
        ROUND(SUM(sales), 2)  AS revenue,
        ROUND(SUM(profit), 2) AS profit,
        ROUND(AVG(discount) * 100, 1) AS avg_discount_pct
    FROM sales
    GROUP BY product
    ORDER BY revenue DESC
    LIMIT 10
""", conn)
print("\n🏆 Top 10 Products:")
print(q3)

# ──────────────────────────────────────────
# QUERY 4: Revenue by Industry (Segment)
# ──────────────────────────────────────────
q4 = pd.read_sql_query("""
    SELECT 
        industry,
        ROUND(SUM(sales), 2)  AS revenue,
        ROUND(SUM(profit), 2) AS profit,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM sales
    GROUP BY industry
    ORDER BY revenue DESC
""", conn)
print("\n🏭 Revenue by Industry:")
print(q4)

# ──────────────────────────────────────────
# QUERY 5: Monthly Revenue Trend
# ──────────────────────────────────────────
q5 = pd.read_sql_query("""
    SELECT 
        SUBSTR(order_date, 7, 4) || '-' || SUBSTR(order_date, 1, 2) AS year_month,
        ROUND(SUM(sales), 2)  AS revenue,
        ROUND(SUM(profit), 2) AS profit
    FROM sales
    GROUP BY year_month
    ORDER BY year_month ASC
""", conn)
print("\n📅 Monthly Revenue Trend:")
print(q5)

conn.close()
print("\n✅ All SQL queries done!")