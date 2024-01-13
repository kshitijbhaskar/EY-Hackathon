import sqlite3
import streamlit as st

class RestockingAlert:

    def fetch_data_from_database(self, sku_id):
        # for this we have to use different database that also contains sell_rate
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        cursor.execute("SELECT sell_rate, quantity FROM items WHERE sku_id=?", (sku_id,))
        result = cursor.fetchone()

        conn.close()

        return result

    @staticmethod
    def calculate_time_to_last(selling_rate, current_stock):
        if selling_rate > 0:
            time_to_last = current_stock / selling_rate
        else:
            time_to_last = float('inf')
        return time_to_last

    def run_web_app(self):
        st.title("Inventory Management System - Restocking Alert")

        for sku_id in self.get_sku_units_needing_restock():
            st.warning(f"Urgent Restocking Alert: SKU Unit {sku_id} needs restocking!")

    def get_sku_units_needing_restock(self):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        cursor.execute("SELECT sku_id FROM items")
        sku_units = cursor.fetchall()

        items_needing_restock = []
        for sku_id in sku_units:
            selling_rate, current_stock = self.fetch_data_from_database(sku_id[0])
            # fetch selling rate, current stock (quantity) from database
            time_to_last = self.calculate_time_to_last(selling_rate, current_stock)

            if time_to_last < 6:
                items_needing_restock.append(sku_id[0])

        conn.close()

        return items_needing_restock
