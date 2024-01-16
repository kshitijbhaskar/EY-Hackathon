import streamlit as st
# from YourApp import YourApp
from AINegotiator import AINegotiator
from PersonalisedMarketing import PersonalisedMarketing
from AnalyticsPage import AnalyticsPage
from ModifyInventory import ModifyInventory
from SmartSuggest import SmartSuggest
from RestockingAlert import RestockingAlert
from ChatBot import ChatBot
from FigmaUI import FigmaUI
import sqlite3

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

def main():
    create_database()  # Make sure the database is created before using it
    st.set_page_config(page_title="Sky: Inventory Management System", page_icon=":bar_chart:")

    st.sidebar.title("Options")
    selected_option = st.sidebar.radio("", ["Analytics", "Modify Inventory", "Smart Suggest", "Restocking Alert",
                                            "AI Negotiator", "Personalised Marketing", "Sky Assist", "FigmaUI"])

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
        ai_negotiator_app = AINegotiator()  # Use AINegotiator from the new script
        ai_negotiator_app.run_web_app()
    elif selected_option == "Personalised Marketing":
        personalised_marketing = PersonalisedMarketing()
        personalised_marketing.run_web_app()
    elif selected_option == "Sky Assist":
        chat_bot = ChatBot()
        chat_bot.run_web_app()
    elif selected_option == "FigmaUI":
        figma_ui = FigmaUI()
        figma_ui.run_web_app()

if __name__ == "__main__":
    main()