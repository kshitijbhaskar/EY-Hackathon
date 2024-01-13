import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

class RestockingAlert:

    def fetch_data_from_excel(self, SKU_ID, analytics_df):
        # Filter the dataframe based on SKU_ID
        item_data = analytics_df[analytics_df['SKU_ID'] == SKU_ID]
        
        # Extract selling rate and current stock (quantity)
        selling_rate = item_data['Selling Rate'].values[0]
        current_stock = item_data['Stock in Inventory(In KG for GROCERY)'].values[0]

        return selling_rate, current_stock

    @staticmethod
    def calculate_time_to_last(selling_rate, current_stock):
        if selling_rate > 0:
            time_to_last = current_stock / selling_rate
        else:
            time_to_last = float('inf')
        return time_to_last

    def run_web_app(self):
        st.title("Inventory Management System - Restocking Alert")
        st.subheader("The following stocks need urgent restocking as they will last for less than 5 days")

        # Read data from analytics.xlsx
        analytics_df = pd.read_excel("analytics.xlsx")

        for SKU_ID in self.get_sku_units_needing_restock(analytics_df):
            selling_rate, current_stock = self.fetch_data_from_excel(SKU_ID, analytics_df)
            time_to_last = self.calculate_time_to_last(selling_rate, current_stock)

            st.warning(f"Urgent Restocking Alert: {SKU_ID} needs restocking! "
                       f"Current stock can last for {time_to_last:.2f} days.")

        # Plotting selling rates and buying rates
        fig, ax = self.plot_rates(analytics_df)
        st.pyplot(fig)

    def get_sku_units_needing_restock(self, analytics_df):
        items_needing_restock = []

        for SKU_ID in analytics_df['SKU_ID']:
            selling_rate, current_stock = self.fetch_data_from_excel(SKU_ID, analytics_df)
            time_to_last = self.calculate_time_to_last(selling_rate, current_stock)

            if time_to_last < 5:
                items_needing_restock.append(SKU_ID)

        return items_needing_restock

    @staticmethod
    def plot_rates(analytics_df):
        # Plotting selling rates and buying rates
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(analytics_df['SKU_ID'], analytics_df['Selling Rate'], label='Selling Rate', marker='o')
        ax.plot(analytics_df['SKU_ID'], analytics_df['Buying Rate'], label='Buying Rate', marker='o')

        ax.set_title('Selling and Buying Rates Over SKU Units')
        ax.set_xlabel('SKU Unit')
        ax.set_ylabel('Rate')
        ax.legend()
        ax.grid(True)

        return fig, ax
