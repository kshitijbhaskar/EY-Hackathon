import sqlite3
import streamlit as st
import calendar

def predict_price(sku_id):
  sku_id = sku_id
  return 69

def process_summary(old_price, new_price, sku_id):
  pass

class InventoryItem:
    def __init__(self, sku_id, item_name, sell_price, buy_price, quantity, added_datetime):
        self.sku_id = sku_id
        self.item_name = item_name
        self.sell_price = sell_price
        self.buy_price = buy_price
        self.quantity = quantity
        self.added_datetime = added_datetime

class InventoryManager:
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path

    def get_item_by_sku_id(self, sku_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM items WHERE sku_id=?", (sku_id,))
        result = cursor.fetchone()

        conn.close()

        if result:
            # Create an InventoryItem object using the fetched details
            return InventoryItem(*result)
        else:
            return None

class SmartSuggest:
    def __init__(self):
        pass

    def fetch_old_price(self, sku_id):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        cursor.execute("SELECT sell_price FROM items WHERE sku_id=?", (sku_id,))
        result = cursor.fetchone()

        conn.close()

        return result[0] if result else None
    
    def is_sku_in_inventory(self, sku_id):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=?", (sku_id,))
        count = cursor.fetchone()[0]

        conn.close()

        return count > 0

    def run_web_app(self):
        st.title("Smart Suggest Web App")

        # User input for the month
        selected_month = st.selectbox("Select Month:", list(calendar.month_name)[1:], index=0)
        month_number = list(calendar.month_name).index(selected_month)

        # Process items added in the selected month
        suggestions, increased_sales_items = self.get_top_suggestions_for_month(month_number)

        # Display header message
        if increased_sales_items:
            st.header(f"In the month of {selected_month}, the sales of {', '.join(increased_sales_items[:3])} is higher than the previous month.")
            st.subheader("Your suitable recommendations are mentioned below:")
        elif suggestions:
            st.header(f"No items with increased sales in the month of {selected_month}.")
        else:
            st.header("No recommendations this month.")

        # Display suggestions in three card-like containers
        for suggestion in suggestions:
            self.display_suggestion_card(suggestion)

    def get_top_suggestions_for_month(self, month_number):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        # Get items added in the selected month
        cursor.execute("SELECT sku_id, item_name, added_datetime FROM items WHERE strftime('%m', added_datetime) = ?",
                       (f"{month_number:02d}",))
        items_added_in_month = cursor.fetchall()

        suggestions = []
        increased_sales_items = set()

        for sku_id, item_name, added_datetime in items_added_in_month:
            old_price = self.fetch_old_price(sku_id)
            new_price = predict_price(sku_id)

            if old_price is not None and new_price is not None:
                price_increase = (new_price - old_price) / old_price
                suggestions.append({"sku_id": sku_id, "item_name": item_name, "price_increase": price_increase})

                # Check if sales increased compared to the previous month
                cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=? AND strftime('%m', added_datetime) = ?",
                               (sku_id, f"{month_number-1:02d}"))
                # count = cursor.fetchone()[0]

                # if count > 0:
                increased_sales_items.add(item_name)

        # Sort suggestions by price increase in descending order
        suggestions.sort(key=lambda x: x["price_increase"], reverse=True)

        conn.close()

        # Return the top three suggestions and items with increased sales
        return suggestions[:3], list(increased_sales_items)

    def display_suggestion_card(self, suggestion):
        st.write(f"**Item Name:** {suggestion['item_name']}")
        st.write(f"**Price Increase:** {suggestion['price_increase']:.2%}")

        # Fetch details of the item using InventoryManager
        inventory_manager = InventoryManager()
        item_details = inventory_manager.get_item_by_sku_id(suggestion['sku_id'])

        # Display details using an expander
        with st.expander(f"Details for {suggestion['item_name']}"):
            if item_details:
                st.write(f"SKU ID: {item_details.sku_id}")
                st.write(f"Buy Price: ₹{item_details.buy_price:.2f}")
                st.write(f"Sell Price: ₹{item_details.sell_price:.2f}")
                st.write(f"Quantity: {item_details.quantity}")
                st.write(f"Added Datetime: {item_details.added_datetime}")
            else:
                st.warning(f"Item with SKU ID {suggestion['sku_id']} not found in the inventory.")
