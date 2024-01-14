import streamlit as st
import pandas as pd
import datetime

# Function to get the current date
def get_current_date():
    return datetime.date.today()

# Function to calculate days between two dates
def calculate_days_since_last_visit(last_visit_date):
    current_date = get_current_date()
    return (current_date - last_visit_date).days

# Function to display data table from Excel file
def display_data_table(file_path):
    df = pd.read_excel(file_path)
    st.table(df)

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
        if st.button("Occasions"):
            self.display_occasions_suggestions()

        if st.button("Deadstock"):
            self.display_deadstock_suggestions()

        if st.button("Retention"):
            self.display_retention_suggestions()

    def display_occasions_suggestions(self):
        st.subheader("Occasions Suggestions:")
        occasions_suggestions = {
            "Dashara": "2024-10-10",
            "Diwali": "2024-11-04",
            "Christmas": "2024-12-25",
            "New Year": "2025-01-01"
        }
        for occasion, date_str in occasions_suggestions.items():
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            with st.expander(f"{occasion} - {date.strftime('%Y-%m-%d')}"):
                display_data_table('temp.xlsx')

    def display_deadstock_suggestions(self):
        st.subheader("Deadstock Suggestions:")
        deadstock_suggestions = {
            "Kurta": 50,
            "Sherwani": 30,
            "Tuxedo": 20
        }
        for item, stock in deadstock_suggestions.items():
            with st.expander(f"{item} - Stock: {stock}"):
                display_data_table('temp.xlsx')

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
                display_data_table('temp.xlsx')

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


