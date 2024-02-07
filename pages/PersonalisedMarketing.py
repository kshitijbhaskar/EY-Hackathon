import streamlit as st
import pandas as pd
import datetime
import numpy as np
from twilio.rest import Client
from openai import OpenAI
import subprocess

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Your Account SID and Auth Token from twilio.com/console
account_sid = 'ACbc046d394f28e67d5430a662661dd8d3'
auth_token = 'bff3a3c73653b6e5d605fcffb6cc1e8f'
client1 = Client(account_sid, auth_token)

occ = 'New year'
a = 'Rakesh'
b = 'reguler buyer'
c = 'young man'
d = 'suits'
e = '500'
f = 'English'
g = 'kurta'

message_tone = "Friendly"
custom_instructions = "None"
set_message_length = 100


messages_1 =  [
    {'role':'system',
    'content':"""As an assistant (Ramesh Assava) at Assawa store, a clothing shop, your role involves creating concise and engaging messages for personalized campaigns linked to upcoming occasions like Diwali, Christmas, etc. The task is to craft a 100-word message that is polite and exciting. Begin with a personalized greeting based on the customer's profile, taking into account factors such as age group, language, and buying behavior. Highlight special offers on clothing tailored for the specific occasion. Conclude the message by mentioning the loyalty points that customers can utilize in their next purchase. The input details include the occasion, customer's name, category preference, buying behavior, language, and current loyalty points, with a special focus on targeted offers."""},
    {'role':'user',
    'content':f"""
        With message tone {message_tone} and custom instructions {custom_instructions}, in {set_message_length} words,
        write a {occ} message for {a}, a {b} in the category of {c}, focusing on {d}. His loyalty points amount to {e} rupees. Language of the message: {f}.
        """
    },
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


# Function to get the current date
def get_current_date():
    return datetime.date.today()

# Function to calculate days between two dates
def calculate_days_since_last_visit(last_visit_date):
    current_date = get_current_date()
    return (current_date - last_visit_date).days


@st.cache_data
def final_message(input, model="gpt-3.5-turbo", temperature=0):

    output = client.chat.completions.create(
        model=model,
        messages=input,
        temperature=temperature,

    )
    return output.choices[0].message.content
# Function to display data table from Excel file
@st.cache_data
def display_data_table(file_path, sheet_name, key):
    df = pd.read_excel(file_path, sheet_name)
    st.table(df)

def display_customer_segments():
    st.header("Customer Segments")

    # Dropdown to select customer segment
    selected_segment = st.selectbox("Select Customer Segment:", ["Young Adults", "Adults", "Elderly"])

    # Button to show details of the selected segment
    if st.button("Show Details"):
        show_customer_segment_details(selected_segment)
@st.cache_data
def show_customer_segment_details(selected_segment):
    st.subheader(f"Details for {selected_segment}")

    # Dummy data for demonstration
    segment_data = {
        "Young Adults": {
            "Number of People": 100,
            "Percentage of Male": 40,
            "Percentage of Female": 60,
            "Revenue Generated": 500000,
            "Amount Spent": 20000
        },
        "Adults": {
            "Number of People": 150,
            "Percentage of Male": 30,
            "Percentage of Female": 70,
            "Revenue Generated": 750000,
            "Amount Spent": 30000
        },
        "Elderly": {
            "Number of People": 75,
            "Percentage of Male": 45,
            "Percentage of Female": 55,
            "Revenue Generated": 300000,
            "Amount Spent": 12500
        }
    }
    # Select the data for the selected segment
    data = segment_data[selected_segment]
    df_segment = pd.DataFrame(data, index=[0])

    # Display card with analysis details
    st.write(f"**Number of People in {selected_segment}:** {df_segment['Number of People'][0]}")
    st.write(f"**Percentage of Gender:** {df_segment['Percentage of Male'][0]}% Male, {df_segment['Percentage of Female'][0]}% Female")
    st.write(f"**Total Revenue Generated:** ₹{df_segment['Revenue Generated'][0]:,.2f}")
    messages_6 = [
        {'role': 'system',
        'content': """You are a smart assistant at Assawa Grocery Stores. Your role is to provide suggestions seeing input to Mr. Assawa on increasing sales, retaining and satisfying customers, and creating targeted marketing campaigns. Input will include customer segments, the number of customers in each segment, gender ratio percentages, and revenue from each segment in a specific period. suggest like in first person you are saying and step-wise, info should be like insight and helpful, step-wise """},
        {'role': 'user',
        'content': f"""Segment: {selected_segment}
                    Number of People: {df_segment['Number of People'][0]},
                    Gender Ratio (M/F): {df_segment['Percentage of Male'][0]}% Male, {df_segment['Percentage of Female'][0]}% Female,
                    Total Revenue: ₹{df_segment['Revenue Generated'][0]:,.2f} """},
    ]
    with st.spinner('AI is generating your content. This can take a while sometimes...'):

        response2 = final_message(messages_6, temperature=1)
        
        st.write(response2)
    # Bar graph for amount spent on products
    # st.subheader("Amount Spent on Products")
    # st.bar_chart(df_segment.set_index('Products'))

def generate_marketing_programs():
    st.title("Smart Marketing Campaign")
    # Buttons for each marketing program
    selected_option = st.sidebar.radio("Choose campaign strategy", ["Occasions", "Deadstock", "Retention"])

    if selected_option == "Occasions":
        st.radio("Choose the target occasion for campaign", ["Dussehra: 2024-10-10", "Diwali: 2024-11-04", "Christmas: 2024-12-25"])
        with st.expander("Customer Details"):
            df = pd.read_excel('Profiles.xlsx', 'Sheet1')
            st.table(df)
    elif selected_option == "Deadstock":
        stock_data = pd.read_excel('stock.xlsx')
        deadstock_suggestions = dict(zip(stock_data['Item'], stock_data['Stock']))
        options=[]
        for i, (item, stock) in enumerate(deadstock_suggestions.items()):
            options.append(f"{item} - Stock: {stock}")

        st.multiselect("Choose items", options)
        with st.expander("Customer Details"):
            df = pd.read_excel('Profiles.xlsx', 'Sheet1')
            st.table(df)
    elif selected_option == "Retention":
        with st.expander("Last Visited Customers"):
            df = pd.read_excel('Profiles.xlsx', 'Sheet2')
            if "Last Purchase Date" in df.columns:
                df["Last Purchase Date"] = pd.to_datetime(df["Last Purchase Date"]).dt.date.astype(str)
            st.table(df)

    # if st.radio("Occasions specific program suggestions"):
    #     self.display_occasions_suggestions()

    # if st.button("Deadstock specific program suggestions"):
    #     self.display_deadstock_suggestions()

    # if st.button("Retention specific program suggestions"):
    #     self.display_retention_suggestions()

    # self.display_data_table('Profiles.xlsx','Sheet1',f" ")
    # Options for message customization
    message_tone = st.selectbox("Set Message Tone:", ["Friendly", "Formal", "Casual"])
    custom_instructions = st.text_area("Add Custom Instructions:")
    personalize_message = st.checkbox("Personalize each Message")
    use_default_poster = st.checkbox("Use Default AI-generated Poster")
    add_posters = st.file_uploader("Add Custom Posters (Image or PDF):", type=["jpg", "jpeg", "png", "pdf"])
    set_message_length = st.slider("Set Message Length (No. of Words):", min_value=10, max_value=500, value=100)
    messages_1 =  [
    {'role':'system',
    'content':"""As an assistant (Ramesh Assava) at Assawa store, a clothing shop, your role involves creating concise and engaging messages for personalized campaigns linked to upcoming occasions like Diwali, Christmas, etc. The task is to craft a 100-word message that is polite and exciting. Begin with a personalized greeting based on the customer's profile, taking into account factors such as age group, language, and buying behavior. Highlight special offers on clothing tailored for the specific occasion. Conclude the message by mentioning the loyalty points that customers can utilize in their next purchase. The input details include the occasion, customer's name, category preference, buying behavior, language, and current loyalty points, with a special focus on targeted offers."""},
    {'role':'user',
    'content':f"""
        With message tone {message_tone} and custom instructions {custom_instructions}, in {set_message_length} words,
        write a {occ} message for {a}, a {b} in the category of {c}, focusing on {d}. His loyalty points amount to {e} rupees. Language of the message: {f}.
        """
    },
    ]
    if use_default_poster:
        response6 = client.images.generate(
        model="dall-e-3",
        prompt=F"VERY IMPORTANT: **DONT USE ANY TEXT IN THE GENERATED IMAGE/ YOU CAN USE ONLY GRAPHICS**. Generate a Retail shop advertisement poster FOR THIS MESSAGE: {final_message(messages_1, temperature=1)}, keep the poster minimalistic",
        size="1024x1024",
        quality="standard",
        n=1,
        )
        image_url = response6.data[0].url
        st.image(image_url)
    response = st.text_area("Edit Message:", value=final_message(messages_1, temperature=1))
    if st.button("Send message to customers" ,type="primary"):
        response = final_message(messages_1, temperature=1)
        subprocess.run(["python", "whatsapp_sender.py", '+919330341418', response, '6', '0'])

def display_occasions_suggestions():
    st.subheader("Occasions Suggestions:")
    occasions_suggestions = {
        "Dussehra": "2024-10-10",
        "Diwali": "2024-11-04",
        "Christmas": "2024-12-25",
        "New Year": "2025-01-01"
    }
    for occasion, date_str in occasions_suggestions.items():
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        st.radio(f"{occasion} - {date.strftime('%Y-%m-%d')}")

def display_deadstock_suggestions():
    stock_data = pd.read_excel('stock.xlsx')

    # Create a dictionary from the two columns in the DataFrame
    deadstock_suggestions = dict(zip(stock_data['Item'], stock_data['Stock']))
    for item, stock in deadstock_suggestions.items():
        with st.expander(f"{item} - Stock: {stock}"):
            display_data_table('Profiles.xlsx','Sheet1',f"{item} - Stock: {stock}")

def display_retention_suggestions():
    st.subheader("Retention Suggestions:")
    with st.expander("Last Visited Customers"):
            df = pd.read_excel('Profiles.xlsx', 'Sheet2')
            if "Last Purchase Date" in df.columns:
                df["Last Purchase Date"] = pd.to_datetime(df["Last Purchase Date"]).dt.date.astype(str)
            st.table(df)


st.title("Personalised Marketing")

selected_option = st.sidebar.radio("Select Tab:", ["Customer Segments", "Smart Marketing Programs"])

# Initialize and run the selected option
if selected_option == "Customer Segments":
    display_customer_segments()
elif selected_option == "Smart Marketing Programs":
    generate_marketing_programs()