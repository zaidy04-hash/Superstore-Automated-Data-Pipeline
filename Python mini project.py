
# Mini-Project: Advanced Python Data Exploration & Automated Reporting
# Dataset: Sample - Superstore 2019.xls
# Tool: Python (Pandas, NumPy, Matplotlib, Seaborn)

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')


class SuperstoreAnalyzer:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.df_cleaned = None
        self.output_folder = "superstore_output_report"
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def load_data(self):
        print("--- [1] Loading Dataset ---")
        try:
            if self.file_path.endswith('.xls') or self.file_path.endswith('.xlsx'):
                try:
                    self.df = pd.read_excel(self.file_path)
                except Exception:
                    self.df = pd.read_excel(self.file_path, engine='xlrd')
            else:
                self.df = pd.read_csv(self.file_path, encoding='latin1')
            print(f"Dataset Loaded Successfully! Rows: {len(self.df)}")
        except Exception as e:
            print(f"Error loading file: {e}")

    def inspect_data(self):
        print("\n--- [2] Inspecting Metadata ---")
        if self.df is not None:
            print("Dataset Shape (Rows, Columns):", self.df.shape)
            print("\nMissing Values Count:")
            print(self.df.isnull().sum())

    def clean_data(self):
        print("\n--- [3] Cleaning and Preprocessing Data ---")
        df = self.df.copy()

        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
        df = df.drop_duplicates()

        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        if 'ship_date' in df.columns:
            df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')

        num_cols = df.select_dtypes(include=[np.number]).columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())

        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype('category')

        self.df_cleaned = df
        print("Data cleaning completed successfully.")

    def add_features(self):
        print("\n--- [4] Feature Engineering ---")
        df = self.df_cleaned

        if 'order_date' in df.columns and 'ship_date' in df.columns:
            df['shipping_duration'] = (df['ship_date'] - df['order_date']).dt.days

        if 'sales' in df.columns and 'profit' in df.columns:
            df['profit_margin'] = np.where(df['sales'] > 0, (df['profit'] / df['sales']) * 100, 0)

        if 'order_date' in df.columns:
            df['order_month'] = df['order_date'].dt.strftime('%Y-%m')

        if 'sales' in df.columns:
            q1 = df['sales'].quantile(0.33)
            q2 = df['sales'].quantile(0.66)
            conditions = [
                df['sales'] <= q1,
                (df['sales'] > q1) & (df['sales'] <= q2),
                df['sales'] > q2
            ]
            labels = ['Low', 'Medium', 'High']
            df['sales_performance_category'] = np.select(conditions, labels, default='Medium')

        self.df_cleaned = df
        print("Feature engineering completed successfully.")

    def create_plots(self):
        print("\n--- [5] Generating 8 Visualizations ---")
        df = self.df_cleaned

        # 1. Monthly Sales Trend
        plt.figure(figsize=(8, 4))
        monthly = df.groupby('order_month')['sales'].sum().reset_index()
        sns.lineplot(data=monthly, x='order_month', y='sales', marker='o')
        plt.title('1. Monthly Sales Trend')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{self.output_folder}/chart1_monthly_sales.png")
        plt.show()

        # 2. Total Sales by Category
        plt.figure(figsize=(7, 4))
        sns.barplot(data=df, x='category', y='sales', estimator=sum, errorbar=None)
        plt.title('2. Total Sales by Category')
        plt.tight_layout()
        plt.savefig(f"{self.output_folder}/chart2_sales_by_category.png")
        plt.show()

        # 3. Correlation Matrix Heatmap
        plt.figure(figsize=(6, 4))
        num_df = df.select_dtypes(include=[np.number])
        sns.heatmap(num_df.corr(), annot=True, cmap='Blues', fmt=".2f")
        plt.title('3. Correlation Matrix')
        plt.tight_layout()
        plt.savefig(f"{self.output_folder}/chart3_correlation.png")
        plt.show()

        # 4. Sales Distribution
        plt.figure(figsize=(7, 4))
        sns.histplot(df['sales'], kde=True, bins=30, color='teal')
        plt.title('4. Sales Value Distribution')
        plt.tight_layout()
        plt.savefig(f"{self.output_folder}/chart4_sales_distribution.png")
        plt.show()

        # 5. Shipping Duration Boxplot
        plt.figure(figsize=(7, 4))
        if 'ship_mode' in df.columns and 'shipping_duration' in df.columns:
            sns.boxplot(data=df, x='ship_mode', y='shipping_duration')
            plt.title('5. Shipping Duration across Ship Modes')
            plt.tight_layout()
            plt.savefig(f"{self.output_folder}/chart5_shipping_duration.png")
            plt.show()

        # 6. Regional Profit Contribution
        plt.figure(figsize=(7, 4))
        if 'region' in df.columns:
            sns.barplot(data=df, x='region', y='profit', estimator=sum, errorbar=None)
            plt.title('6. Total Profit by Region')
            plt.tight_layout()
            plt.savefig(f"{self.output_folder}/chart6_profit_by_region.png")
            plt.show()

        # 7. Discount vs Profitability
        plt.figure(figsize=(7, 4))
        if 'discount' in df.columns:
            sns.scatterplot(data=df, x='discount', y='profit', alpha=0.6)
            plt.title('7. Discount Rates vs Profitability')
            plt.tight_layout()
            plt.savefig(f"{self.output_folder}/chart7_discount_vs_profit.png")
            plt.show()

        # 8. Sales Performance Tiers Count
        plt.figure(figsize=(6, 4))
        if 'sales_performance_category' in df.columns:
            sns.countplot(data=df, x='sales_performance_category')
            plt.title('8. Orders Count by Sales Performance Category')
            plt.tight_layout()
            plt.savefig(f"{self.output_folder}/chart8_sales_categories.png")
            plt.show()

        print("All 8 visualizations created and saved successfully.")

    def export_report(self):
        print("\n--- [6] Generating Automated KPI Report ---")
        df = self.df_cleaned

        total_sales = df['sales'].sum()
        total_profit = df['profit'].sum()
        avg_margin = df['profit_margin'].mean() if 'profit_margin' in df.columns else 0

        summary_text = f"""
==========================================
        AUTOMATED KPI SUMMARY REPORT
==========================================
Total Revenue (Sales) : ${total_sales:,.2f}
Total Net Profit      : ${total_profit:,.2f}
Average Profit Margin : {avg_margin:.2f}%
Total Records         : {len(df)}
==========================================
"""
        print(summary_text)

        with open(f"{self.output_folder}/summary_report.txt", "w", encoding='utf-8') as f:
            f.write(summary_text)

        df.to_csv(f"{self.output_folder}/cleaned_superstore_data.csv", index=False)
        print("Cleaned dataset and text summary report exported successfully.")


if __name__ == "__main__":
    file_name = "i:/Python_Learning/Sample - Superstore 2019.xls"

    app = SuperstoreAnalyzer(file_name)
    app.load_data()
    app.inspect_data()
    app.clean_data()
    app.add_features()
    app.create_plots()
    app.export_report()

    print("\n[SUCCESS] Pipeline executed successfully!")

    