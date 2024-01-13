import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class AnalyticsPage:
    def __init__(self):
        pass

    def display_analytics(self):
        st.header("Analytics")

        # Load data from SQLite database
        conn = sqlite3.connect("inventory.db")
        df_sql = pd.read_sql_query("SELECT * FROM items", conn)
        conn.close()

        # Load data from Excel sheet
        df_excel = pd.read_excel("analytics.xlsx")

        # Display basic statistics
        st.subheader("Basic Statistics for SQLite Database")
        st.write(df_sql.describe())

        st.subheader("Basic Statistics for Excel Sheet")
        st.write(df_excel.describe())

        # Visualize data using plots

        # Arrange plots horizontally

        # Bar plot for quantity of items in SQLite database
        st.subheader("Bar Plot: Quantity of Items in SQLite Database")
        plt.subplot(1, 2, 1)
        sns.barplot(x="item_name", y="quantity", data=df_sql)
        plt.xticks(rotation=45, ha="right")

        # Scatter plot for buy price and sell price in Excel sheet
        plt.subplot(1, 2, 2)
        sns.scatterplot(x="Buying Rate", y="Selling Rate", data=df_excel)

        # Display the plots horizontally
        st.pyplot(plt)

        # Add some space
        st.write("\n")

        # Arrange plots vertically

        # Line plot for buying rate in SQLite database
        st.subheader("Line Plot: Buying Rate in SQLite Database")
        plt.subplot(2, 1, 1)
        sns.lineplot(x="item_name", y="buy_price", data=df_sql)
        plt.xticks(rotation=45, ha="right")

        # Line plot for selling rate in Excel sheet
        plt.subplot(2, 1, 2)
        sns.lineplot(x="Product Number", y="Selling Rate", data=df_excel)

        # Display the plots vertically
        st.pyplot(plt)

        # Add some space
        st.write("\n")

        # Arrange three plots horizontally

        # Histogram for quantity in SQLite database
        st.subheader("Histogram: Quantity in SQLite Database")
        plt.subplot(1, 3, 1)
        plt.hist(df_sql['quantity'], bins=20, color='skyblue', edgecolor='black')

        # Box plot for buying rate in Excel sheet
        plt.subplot(1, 3, 2)
        sns.boxplot(x=df_excel['Buying Rate'])

        # Violin plot for selling rate in Excel sheet
        plt.subplot(1, 3, 3)
        sns.violinplot(x=df_excel['Selling Rate'], color='salmon')

        # Display the three plots horizontally
        st.pyplot(plt)

    def run_web_app(self):
        self.display_analytics()