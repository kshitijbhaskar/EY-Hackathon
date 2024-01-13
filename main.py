import streamlit as st
from YourApp import YourApp
from datetime import datetime,timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import calendar
import sqlite3

def predict_price(sku_id):
  sku_id = sku_id
  return 69

def process_summary(old_price, new_price, sku_id):
  pass

def create_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            sku_id TEXT PRIMARY KEY,
            item_name TEXT,
            sell_price REAL,
            buy_price REAL,
            quantity INTEGER,
            added_datetime TEXT
        )
    ''')

    conn.commit()
    conn.close()

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
        sns.lineplot(x="item_name", y="Selling Rate", data=df_excel)

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

class ModifyInventory:
    def __init__(self):
        pass

    def add_or_modify_item(self, sku_id, item_name, buy_price, sell_price, quantity):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        try:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Check if SKU ID already exists
            cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=?", (sku_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                # SKU ID exists, update the item
                cursor.execute("""
                    UPDATE items
                    SET item_name=?, sell_price=?, buy_price=?, quantity=?, added_datetime=?
                    WHERE sku_id=?
                """, (item_name, sell_price, buy_price, quantity, current_datetime, sku_id))
                st.success(f"Item {sku_id} modified successfully at {current_datetime}!")
            else:
                # SKU ID doesn't exist, add a new item
                cursor.execute("""
                    INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)
                """, (sku_id, item_name, sell_price, buy_price, quantity, current_datetime))
                st.success(f"Item {sku_id} added successfully at {current_datetime}!")

            conn.commit()
        except sqlite3.IntegrityError:
            st.warning(f"Item {sku_id} already exists in the database. Use a different SKU ID.")
        finally:
            conn.close()

    def remove_item(self, sku_id):
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        try:
            # Check if SKU ID exists
            cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=?", (sku_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                # SKU ID exists, remove the item
                cursor.execute("DELETE FROM items WHERE sku_id=?", (sku_id,))
                st.success(f"Item {sku_id} removed successfully!")
            else:
                st.warning(f"Item with SKU ID {sku_id} not found in the inventory.")

            conn.commit()
        finally:
            conn.close()

    def run_web_app(self):
        st.title("Inventory Management System - Modify Inventory")

        # User input for item details
        sku_id = st.text_input("Enter SKU ID:")
        item_name = st.text_input("Enter Item Name:")
        buy_price = st.number_input("Enter Cost Price:", min_value=0.01)
        sell_price = st.number_input("Enter Sell Price:", min_value=0.01)
        quantity = st.number_input("Enter Quantity:", min_value=0, step=1, format="%d")

        if st.button("Add/Modify Item"):
            self.add_or_modify_item(sku_id, item_name, buy_price, sell_price, quantity)

        # Display existing items and buttons to remove them
        st.title("Existing Items in Inventory")
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        conn.close()

        for item in items:
            self.display_existing_item(item)

    def display_existing_item(self, item):
        sku_id, item_name, sell_price, buy_price, quantity, added_datetime = item

        # Display existing item details
        st.write(f"**Item Name:** {item_name}")
        st.write(f"SKU ID: {sku_id}")
        st.write(f"Buy Price: ₹{buy_price:.2f}")
        st.write(f"Sell Price: ₹{sell_price:.2f}")
        st.write(f"Quantity: {quantity}")
        st.write(f"Added Datetime: {added_datetime}")

        # Add a button to remove the item
        if st.button(f"Remove Item {sku_id}"):
            self.remove_item(sku_id)

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

class AINegotiator:
    def __init__(self):
        self.user = "*User*"

        if 'responses1' not in st.session_state:
            st.session_state['responses1'] = []
        if 'responses2' not in st.session_state:
            st.session_state['responses2'] = []
        if 'items' not in st.session_state:
            st.session_state['items'] = ""
        if 'quantities' not in st.session_state:
            st.session_state['quantities'] = {}
        if 'df1' not in st.session_state:
            st.session_state['df1'] = pd.DataFrame()
        if 'df2' not in st.session_state:
            st.session_state['df2'] = pd.DataFrame()

    def run_web_app(self):
        st.title("AI Negotiator")

        tabs = ["Message Generators", "Negotiator", "Best Deal"]
        selected_tab = st.sidebar.radio("Select Tab:", tabs)

        if selected_tab == "Message Generators":
            self.display_message_generators()
        elif selected_tab == "Negotiator":
            self.display_negotiator()
        elif selected_tab == "Best Deal":
            self.display_best_deal()

    def generate_message_template(self, quantities):
            message = f"Hello from {self.user}!\nI need to restock the following items:\n"

            for item, quantity in quantities.items():
                message += f" - {item} by {quantity} units.\n"

            message += "Please tell me the price and time of the delivery."
            return message

    def display_message_generators(self):
        st.header("Message Generators")

        st.session_state['items'] = st.text_area("Enter Item Names (comma-separated):", value=st.session_state['items'])
        item_list = list(set([item.strip() for item in st.session_state['items'].split(',') if item.strip()]))

        st.button("Add Quantity")

        for item in item_list:
            quantity = st.number_input(f"Quantity for {item}:", min_value=1, step=1, format="%d", key=item, value=st.session_state['quantities'].get(item, 1))
            st.session_state['quantities'][item] = quantity

        if st.button("Generate Template"):
            template = self.generate_message_template(st.session_state['quantities'])
            st.text_area("Message Template", template, height=200)

        if st.button("Send Message"):
            item_list = list(set([item.strip() for item in st.session_state['items'].split(',') if item.strip()]))
            for i, item in enumerate(item_list, start=1):
                st.session_state['responses1'].append({
                    "wholesaler_name": f"Wholesaler {i}",
                    "message": f"Example Message for {item}",
                    "price": 100 + i * 10,
                    "shipping_charges": 10 + i * 2,
                    "delivery_date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
                })
            st.session_state['df1'] = pd.read_excel('negotiation details table.xlsx')  
            st.success("Message sent successfully!")

    def display_negotiator(self):
        st.header("Negotiator")
        for response in st.session_state['responses1']:
            with st.expander(f"From: {response['wholesaler_name']}", expanded=True):
                st.write(f"Message: {response['message']}")
                st.write(f"Price: {response['price']}")
                st.write(f"Shipping Charges: {response['shipping_charges']}")
                st.write(f"Delivery Date: {response['delivery_date']}")
        st.subheader("Negotiation Details Table")
        st.write(st.session_state['df1'])
        if st.button("Negotiate Deal"):
            item_list = list(set([item.strip() for item in st.session_state['items'].split(',') if item.strip()]))
            for i, item in enumerate(item_list, start=1):
                st.session_state['responses2'].append({
                    "wholesaler_name": f"Wholesaler {i}",
                    "message": f"Example Message for {item}",
                    "price": 100 + i * 10,
                    "shipping_charges": 10 + i * 2,
                    "delivery_date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
                })
            st.session_state['df2'] = pd.read_excel('best deal table.xlsx')
            st.success("Deal negotiated successfully!")
    
    def display_best_deal(self):
        st.header("Best Deal")
        for response in st.session_state['responses2']:
            with st.expander(f"From: {response['wholesaler_name']}", expanded=True):
                st.write(f"Message: {response['message']}")
                st.write(f"Price: {response['price']}")
                st.write(f"Shipping Charges: {response['shipping_charges']}")
                st.write(f"Delivery Date: {response['delivery_date']}")
        st.subheader("Best Deal Table")
        st.write(st.session_state['df2'])

        if st.button("Place Order"):
            # Your logic to fill the "Best Deal" entries with respective values
            st.success("Order placed successfully!")


class PersonalisedMarketing:
    def __init__(self):
        pass

    def display_customer_segments(self):
        st.header("Customer Segments")

        # Dropdown to select customer segment
        selected_segment = st.selectbox("Select Customer Segment:", ["Young Adults", "Adults", "Elderly"])

        # Button to show details of the selected segment
        if st.button("Show Details"):
            self.show_customer_segment_details(selected_segment)

        # Button to generate marketing programs
        if st.button("Generate Marketing Programs"):
            self.generate_marketing_programs()

    def show_customer_segment_details(self, selected_segment):
        st.subheader(f"Details for {selected_segment}")

        # Dummy data for demonstration
        segment_data = {
            "Number of People": [100, 150, 75],
            "Percentage of Male": [40, 30, 20],
            "Percentage of Female": [60, 70, 80],
            "Revenue Generated": [5000, 7500, 3000],
            "Products": ["Product A", "Product B", "Product C"],
            "Amount Spent": [2000, 3000, 1200]
        }
        df_segment = pd.DataFrame(segment_data)

        # Display card with analysis details
        st.write(f"**Number of People in {selected_segment}:** {df_segment['Number of People'].sum()}")
        st.write(f"**Percentage of Gender:** {df_segment['Percentage of Male'][0]}% Male, {df_segment['Percentage of Female'][0]}% Female")
        st.write(f"**Total Revenue Generated:** ${df_segment['Revenue Generated'].sum():,.2f}")

        # Bar graph for amount spent on products
        st.subheader("Amount Spent on Products")
        sns.barplot(x="Products", y="Amount Spent", data=df_segment)
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt)

    def generate_marketing_programs(self):
        st.header("Marketing Programs")

        # Dummy data for demonstration
        dormant_customers_data = {
            "Plan 1": ["Discount Coupons", "Social Media Campaign"],
            "Plan 2": ["Loyalty Points", "Email Newsletter"]
        }

        loyal_customers_data = {
            "Plan 1": ["Exclusive Deals", "VIP Events"],
            "Plan 2": ["Personalized Offers", "Early Access Sales"]
        }

        # Display Dormant Customers block
        st.subheader("Dormant Customers")
        self.display_marketing_plans(dormant_customers_data)

        # Display Loyal Customers block
        st.subheader("Loyal Customers")
        self.display_marketing_plans(loyal_customers_data)

    def display_marketing_plans(self, plans_data):
        # Display two plan options
        for plan, details in plans_data.items():
            st.write(f"**Plan {plan}:**")
            for detail in details:
                st.write(f"- {detail}")
            st.write("\n")

    def run_web_app(self):
        st.title("Personalised Marketing")

        # Sidebar options
        st.sidebar.title("Options")
        selected_option = st.sidebar.radio("", ["Customer Segments", "Marketing Programs"])

        # Initialize and run the selected option
        if selected_option == "Customer Segments":
            self.display_customer_segments()
        elif selected_option == "Marketing Programs":
            self.generate_marketing_programs()

def main():
    analytics_app = YourApp()
    analytics_app.run_web_app()
    create_database()  # Make sure the database is created before using it
    st.set_page_config(page_title="Sky: Inventory Management System", page_icon=":bar_chart:")

    st.sidebar.title("Options")
    selected_option = st.sidebar.radio("", ["Analytics","Modify Inventory", "Smart Suggest", "Restocking Alert", "AI Negotiator", "Personalised Marketing"])

    if selected_option == "Analytics":
        analytics_page = AnalyticsPage()
        analytics_page.run_web_app()
    elif selected_option == "Modify Inventory":
        modify_inventory_app = ModifyInventory() 
        modify_inventory_app.run_web_app()
    elif selected_option == "Smart Suggest":
        smart_suggest_app = SmartSuggest()
        smart_suggest_app.run_web_app()
    elif selected_option == "Restocking Alert":
        restocking_alert_app = RestockingAlert()
        restocking_alert_app.run_web_app()
    elif selected_option == "AI Negotiator":
        ai_negotiator_app = AINegotiator()
        ai_negotiator_app.run_web_app()
    elif selected_option == "Personalised Marketing":
        personalised_marketing = PersonalisedMarketing()
        personalised_marketing.run_web_app()

if __name__ == "__main__":
    main()
