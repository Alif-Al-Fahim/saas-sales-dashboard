import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

# ── Setup ──────────────────────────────────
conn = sqlite3.connect("saas_sales.db")
df = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()

os.makedirs("charts", exist_ok=True)

# ── Fix Date ────────────────────────────────
df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y')
df['year']       = df['order_date'].dt.year
df['month']      = df['order_date'].dt.month
df['year_month'] = df['order_date'].dt.to_period('M').astype(str)

print("✅ Date fixed. Range:", df['order_date'].min(), "→", df['order_date'].max())

# ── KPIs ────────────────────────────────────
print("\n📊 KPIs:")
print(f"  Total Revenue : ${df['sales'].sum():,.2f}")
print(f"  Total Profit  : ${df['profit'].sum():,.2f}")
print(f"  Profit Margin : {df['profit'].sum()/df['sales'].sum()*100:.1f}%")
print(f"  Total Orders  : {df['order_id'].nunique()}")
print(f"  Avg Order Value: ${df.groupby('order_id')['sales'].sum().mean():,.2f}")

# ── Chart 1: Monthly Revenue Trend ──────────
monthly = df.groupby('year_month')[['sales','profit']].sum().reset_index()
monthly = monthly.sort_values('year_month')

plt.figure(figsize=(14,5))
plt.plot(monthly['year_month'], monthly['sales'],  marker='o', label='Revenue', color='steelblue')
plt.plot(monthly['year_month'], monthly['profit'], marker='o', label='Profit',  color='green')
plt.title('Monthly Revenue & Profit Trend')
plt.xticks(monthly['year_month'][::3], rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('charts/01_monthly_trend.png')
plt.close()
print("\n✅ Chart 1 saved: Monthly Trend")

# ── Chart 2: Revenue by Region ───────────────
region = df.groupby('region')['sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(7,4))
region.plot(kind='bar', color=['steelblue','orange','green'])
plt.title('Revenue by Region')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts/02_revenue_by_region.png')
plt.close()
print("✅ Chart 2 saved: Revenue by Region")

# ── Chart 3: Top 10 Products ─────────────────
top_products = df.groupby('product')['sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top_products.plot(kind='barh', color='steelblue')
plt.title('Top 10 Products by Revenue')
plt.xlabel('Revenue ($)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('charts/03_top_products.png')
plt.close()
print("✅ Chart 3 saved: Top Products")

# ── Chart 4: Revenue by Industry ─────────────
industry = df.groupby('industry')['sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,5))
industry.plot(kind='bar', color='coral')
plt.title('Revenue by Industry')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/04_revenue_by_industry.png')
plt.close()
print("✅ Chart 4 saved: Revenue by Industry")

# ── Chart 5: Profit Margin by Product ────────
product_data = df.groupby('product')[['sales','profit']].sum()
product_data['margin'] = product_data['profit'] / product_data['sales'] * 100
product_data = product_data.sort_values('margin', ascending=False).head(10)

plt.figure(figsize=(10,5))
product_data['margin'].plot(kind='bar', color='mediumseagreen')
plt.title('Top 10 Products by Profit Margin %')
plt.ylabel('Margin (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/05_profit_margin.png')
plt.close()
print("✅ Chart 5 saved: Profit Margin")

# ── Export Clean CSV for Power BI ────────────
df.to_csv("saas_clean.csv", index=False)
print("\n✅ Clean CSV exported: saas_clean.csv")
print("🎉 Phase 3 complete! Charts saved in /charts folder")