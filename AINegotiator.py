import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

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
            quantity = st.number_input(f"Quantity for {item}:", min_value=1, step=1, format="%d", key=item,
                                       value=st.session_state['quantities'].get(item, 1))
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
                    "delivery_date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                    "latitude": 28.6278 + i * 0.1,  # Adjust the latitude for each wholesaler
                    "longitude": 77.2190 + i * 0.1  # Adjust the longitude for each wholesaler
                })
            st.session_state['df1'] = pd.read_excel('negotiation details table.xlsx')
            st.success("Message sent successfully!")

    def display_negotiator(self):
        st.header("Negotiator")
        map_data = {'LAT': [28.6278], 'LON': [77.2190]}  # Fixed coordinates for the map
        st.header("Negotiator")
        # Initialize with a DataFrame containing column names 'lat' and 'lon' to match Streamlit's requirements.
        map_data = pd.DataFrame({
            'lat': [28.6278], 
            'lon': [77.2190]
        })

        # Additional coordinates to be plotted should be appended to this DataFrame.
        for response in st.session_state['responses1']:
            with st.expander(f"From: {response['wholesaler_name']}", expanded=True):
                # Your response details display logic...

                # Add response coordinates to the map data.
                if 'latitude' in response and 'longitude' in response:
                    map_data = map_data.append({'lat': response['latitude'], 'lon': response['longitude']}, ignore_index=True)
        
        # Now, display the map with all the coordinates included.
        st.map(map_data)

        # ...Rest of the code below...

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
                    "delivery_date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                    "latitude": 28.6278 + i * 0.1,  # Adjust the latitude for each wholesaler
                    "longitude": 77.2190 + i * 0.1  # Adjust the longitude for each wholesaler
                })
                map_data['LAT'].append(response['latitude'])
                map_data['LON'].append(response['longitude'])
            st.session_state['df2'] = pd.read_excel('best deal table.xlsx')
            
            st.success("Deal negotiated successfully!")

    def display_best_deal(self):
        st.header("Best Deal")
        map_data = {'LAT': [28.6278], 'LON': [77.2190]}  # Fixed coordinates for the map
        st.map(map_data)  # Use st.map with the fixed map data
        for response in st.session_state['responses2']:
            with st.expander(f"From: {response['wholesaler_name']}", expanded=True):
                st.write(f"Message: {response['message']}")
                st.write(f"Price: {response['price']}")
                st.write(f"Shipping Charges: {response['shipping_charges']}")
                st.write(f"Delivery Date: {response['delivery_date']}")
                if 'latitude' in response and 'longitude' in response:
                    map_data['LAT'].append(response['latitude'])
                    map_data['LON'].append(response['longitude'])
        st.subheader("Best Deal Table")
        st.write(st.session_state['df2'])

        if st.button("Place Order"):
            # Your logic to fill the "Best Deal" entries with respective values
            st.success("Order placed successfully!")
