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
    st.sidebar.markdown("<h1 style='text-align: left; font-size: 48px; font-weight: bold;'>Sky</h1>", unsafe_allow_html=True)
    st.sidebar.title("For small businesses, Sky is the limit!")
    selected_option = st.sidebar.radio("Select Tab:", ["Analytics", "Modify Inventory", "Smart Suggest", "Restocking Alert",
                                            "AI Negotiator", "Personalised Marketing", "Sky Assist"])

    if selected_option == "Analytics":
        analytics_page = AnalyticsPage()
        with st.spinner('This can take a while sometimes...'):
            # Simulate a delay
            analytics_page.run_web_app()    
            # st.balloons()
    elif selected_option == "Modify Inventory":
        modify_inventory_app = ModifyInventory()
        with st.spinner('This can take a while sometimes...'):
            modify_inventory_app.run_web_app()
    elif selected_option == "Smart Suggest":
        smart_suggest_app = SmartSuggest()
        with st.spinner('This can take a while sometimes...'):
            smart_suggest_app.run_web_app()
    elif selected_option == "Restocking Alert":
        restocking_alert_app = RestockingAlert()
        with st.spinner('This can take a while sometimes...'):
            restocking_alert_app.run_web_app()
    elif selected_option == "AI Negotiator":
        ai_negotiator_app = AINegotiator()  # Use AINegotiator from the new script
        with st.spinner('This can take a while sometimes...'):
            ai_negotiator_app.run_web_app()
    elif selected_option == "Personalised Marketing":
        personalised_marketing = PersonalisedMarketing()
        with st.spinner('This can take a while sometimes...'):
            personalised_marketing.run_web_app()
    elif selected_option == "Sky Assist":
        chat_bot = ChatBot()
        with st.spinner('This can take a while sometimes...'):
            chat_bot.run_web_app()

if __name__ == "__main__":
    main()