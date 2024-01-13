import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
