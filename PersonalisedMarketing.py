import streamlit as st
import pandas as pd
import datetime
import numpy as np
from openai import OpenAI
import subprocess

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


occ = 'New year'
a = 'Rakesh'
b = 'reguler buyer'
c = 'young man'
d = 'suits'
e = '500'
f = 'English'
g = 'kurta'

messages_1 =  [
{'role':'system',
 'content':"""As an assistant (Ramesh Assava) at Assawa store, a clothing shop, your role involves creating concise and engaging messages for personalized campaigns linked to upcoming occasions like Diwali, Christmas, etc. The task is to craft a 100-word message that is polite and exciting. Begin with a personalized greeting based on the customer's profile, taking into account factors such as age group, language, and buying behavior. Highlight special offers on clothing tailored for the specific occasion. Conclude the message by mentioning the loyalty points that customers can utilize in their next purchase. The input details include the occasion, customer's name, category preference, buying behavior, language, and current loyalty points, with a special focus on targeted offers."""},
{'role':'user',
 'content':f"""Write a {occ} message for {a}, a {b} in the category of {c}, focusing on {d}. His loyalty points amount to {e} rupees. Language of the message: {f}."""},
]

messages_2 =  [
{'role':'system',
 'content':"""As an assistant at Assawa Stores, a clothing shop, your responsibilities include crafting concise and engaging messages for personalized campaigns aimed at selling deadstock (outdated items on offer). Your task is to create a 100-word message that is both polite and exciting. Commence with a personalized greeting tailored to the customer's profile, considering factors such as age group, language, and buying behavior. Showcase special offers on specific clothing items that align with their preferences. Conclude the message by highlighting the loyalty points available for use in their next purchase. Utilize input details, including deadstock, customer's name, category preference, buying behavior, language, and current loyalty points, with a special emphasis on targeted offers."""},
{'role':'user',
 'content':f"""Compose a message for {a}, a {b} in the category of {c}, emphasizing on {g} (stock available in-store). He currently has {e} rupees in loyalty points. The language of the message should be {f}."""},
]

messages_3 =  [
{'role':'system',
 'content':"""As an assistant at Assawa Stores, a clothing shop, your role involves creating concise and engaging messages for personalized campaigns targeting customers who are not frequent visitors. Craft a 100-word message that is polite and exciting. Initiate with a personalized greeting based on the customer's profile, considering factors like age group, language, and buying behavior. Present special offers designed to entice and retain these specific customers. Conclude the message by highlighting the loyalty points they can utilize in their next purchase. Utilize input details, including deadstock, customer's name, category preference, buying behavior, language, and current loyalty points, with a special focus on tailored offers."""},
{'role':'user',
 'content':f"""Compose a message for {a}, a {b} in the {c} category who hasn't visited our stores for a while. he currently has {e} rupees in loyalty points. The language of the message should be {f}."""},
]

def final_message(input, model="gpt-3.5-turbo", temperature=0):

    output = client.chat.completions.create(
        model=model,
        messages=input,
        temperature=temperature,

    )
    return output.choices[0].message.content

# Function to get the current date
def get_current_date():
    return datetime.date.today()

# Function to calculate days between two dates
def calculate_days_since_last_visit(last_visit_date):
    current_date = get_current_date()
    return (current_date - last_visit_date).days

# Function to display data table from Excel file
def display_data_table(file_path, key):
    df = pd.read_excel(file_path)
    st.table(df)

    if st.button("Send message to customers", key=key ,type="primary"):
        response = final_message(messages_1, temperature=1)
        subprocess.run(["python", "whatsapp_sender.py", '+919302389149', response, '6', '0'])


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

    def show_customer_segment_details(self, selected_segment):
        st.subheader(f"Details for {selected_segment}")

        # Dummy data for demonstration
        segment_data = {
            "Number of People": [100, 150, 75],
            "Percentage of Male": [40, 30, 20],
            "Percentage of Female": [60, 70, 80],
            "Revenue Generated": [500000, 750000, 300000],
            "Products": ["Product A", "Product B", "Product C"],
            "Amount Spent": [20000, 30000, 12500]
        }
        df_segment = pd.DataFrame(segment_data)

        # Display card with analysis details
        st.write(f"**Number of People in {selected_segment}:** {df_segment['Number of People'].sum()}")
        st.write(f"**Percentage of Gender:** {df_segment['Percentage of Male'][0]}% Male, {df_segment['Percentage of Female'][0]}% Female")
        st.write(f"**Total Revenue Generated:** ₹{df_segment['Revenue Generated'].sum():,.2f}")

        # Bar graph for amount spent on products
        st.subheader("Amount Spent on Products")
        st.bar_chart(df_segment.set_index('Products'))

    def generate_marketing_programs(self):
        st.title("Smart Marketing Campaign")
        # Buttons for each marketing program
        if st.button("Occasions specific program suggestions"):
            self.display_occasions_suggestions()

        if st.button("Deadstock specific program suggestions"):
            self.display_deadstock_suggestions()

        if st.button("Retention specific program suggestions"):
            self.display_retention_suggestions()

    def display_occasions_suggestions(self):
        st.subheader("Occasions Suggestions:")
        occasions_suggestions = {
            "Dussehra": "2024-10-10",
            "Diwali": "2024-11-04",
            "Christmas": "2024-12-25",
            "New Year": "2025-01-01"
        }
        for occasion, date_str in occasions_suggestions.items():
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            with st.expander(f"{occasion} - {date.strftime('%Y-%m-%d')}"):
                display_data_table('temp.xlsx', f"{occasion} - {date.strftime('%Y-%m-%d')}")

    def display_deadstock_suggestions(self):
        st.subheader("Deadstock Suggestions:")
        deadstock_suggestions = {
            "Kurta": 50,
            "Sherwani": 30,
            "Tuxedo": 20
        }
        for item, stock in deadstock_suggestions.items():
            with st.expander(f"{item} - Stock: {stock}"):
                display_data_table('temp.xlsx',f"{item} - Stock: {stock}")

    def display_retention_suggestions(self):
        st.subheader("Retention Suggestions:")
        retention_suggestions = {
            "Dewansh Assawa": "2024-01-01",
            "Rakesh": "2024-02-15",
            "Kshitij": "2024-03-20"
        }
        for customer, last_visit_date_str in retention_suggestions.items():
            last_visit_date = datetime.datetime.strptime(last_visit_date_str, "%Y-%m-%d").date()
            with st.expander(f"{customer} - Last Visit: {last_visit_date.strftime('%Y-%m-%d')}, Days Since Last Visit: {calculate_days_since_last_visit(last_visit_date)}"):
                display_data_table('temp.xlsx',f"{customer} - Last Visit: {last_visit_date.strftime('%Y-%m-%d')}, Days Since Last Visit: {calculate_days_since_last_visit(last_visit_date)}")

    def run_web_app(self):
        st.title("Personalised Marketing")

        # Sidebar options
        st.sidebar.title("Options")
        selected_option = st.sidebar.radio("", ["Customer Segments", "Smart Marketing Programs"])

        # Initialize and run the selected option
        if selected_option == "Customer Segments":
            self.display_customer_segments()
        elif selected_option == "Smart Marketing Programs":
            self.generate_marketing_programs()