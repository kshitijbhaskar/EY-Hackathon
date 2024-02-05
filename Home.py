import streamlit as st
# from YourApp import YourApp
# from pages.Dashboard import Dashboard
# from pages.AINegotiator import AINegotiator
# from pages.PersonalisedMarketing import PersonalisedMarketing
# from pages.AnalyticsPage import AnalyticsPage
# from pages.ModifyInventory import ModifyInventory
# from pages.SmartSuggest import SmartSuggest
# from pages.RestockingAlert import RestockingAlert
# from pages.ChatBot import ChatBot
# from FigmaUI import FigmaUI
import sqlite3
from io import BytesIO
from openai import OpenAI

st.set_page_config(page_title="Sky: Inventory Management System", page_icon=":bar_chart:")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.page_link("Home.py",icon="🏠")
st.page_link("pages/AINegotiator.py",icon="💲")
st.page_link("pages/AnalyticsPage.py",icon="📊")
st.page_link("pages/ChatBot.py",icon="🤖")
st.page_link("pages/Dashboard.py",icon="📋")
st.page_link("pages/ModifyInventory.py",icon="🏭")
st.page_link("pages/PersonalisedMarketing.py",icon="🧑‍🦰")
st.page_link("pages/RestockingAlert.py",icon="⚠️")
st.page_link("pages/SmartSuggest.py",icon="📢")

@st.cache_resource
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
# 
create_database()  # Make sure the database is created before using it
st.sidebar.markdown("<h1 style='text-align: left; color:white; font-size: 48px; font-weight: bold;'>Sky</h1>", unsafe_allow_html=True)
st.sidebar.title(":white[For small businesses, Sky is the limit!]")
# selected_option = st.sidebar.radio("Select Tab:", ["Dashboard","Analytics", "Modify Inventory", "Smart Suggest", "Restocking Alert",
#                                         "AI Negotiator", "Personalised Marketing", "Sky Assist"])

# if selected_option == "Dashboard":
#     dashboard_page = Dashboard()
#     with st.spinner('This can take a while sometimes...'):
#         # Simulate a delay
#         dashboard_page.run_web_app()    
#         # st.balloons()
# elif selected_option == "Analytics":
#     analytics_page = AnalyticsPage()
#     with st.spinner('This can take a while sometimes...'):
#         # Simulate a delay
#         analytics_page.run_web_app()    
#         # st.balloons()
# elif selected_option == "Modify Inventory":
#     modify_inventory_app = ModifyInventory()
#     with st.spinner('This can take a while sometimes...'):
#         modify_inventory_app.run_web_app()
# elif selected_option == "Smart Suggest":
#     smart_suggest_app = SmartSuggest()
#     with st.spinner('This can take a while sometimes...'):
#         smart_suggest_app.run_web_app()
# elif selected_option == "Restocking Alert":
#     restocking_alert_app = RestockingAlert()
#     with st.spinner('This can take a while sometimes...'):
#         restocking_alert_app.run_web_app()
# elif selected_option == "AI Negotiator":
#     ai_negotiator_app = AINegotiator()  # Use AINegotiator from the new script
#     with st.spinner('This can take a while sometimes...'):
#         ai_negotiator_app.run_web_app()
# elif selected_option == "Personalised Marketing":
#     personalised_marketing = PersonalisedMarketing()
#     with st.spinner('This can take a while sometimes...'):
#         personalised_marketing.run_web_app()
# elif selected_option == "Sky Assist":
#     chat_bot = ChatBot()
#     with st.spinner('This can take a while sometimes...'):
#         chat_bot.run_web_app()



# if __name__ == "__main__":
#     main()

import pandas as pd
import seaborn as sns
from datetime import datetime,timedelta
import matplotlib.pyplot as plt

# Read data from Excel file
file_path = 'smart_sell.xlsx'
df = pd.read_excel(file_path)

# Create a figure and axis with a specified figure size
fig, ax = plt.subplots(figsize=(12, 6))
plt.gca().set_aspect('auto', adjustable='datalim')

# Plot the data
ax.plot(df['Index'], df['Amount'])

# Set the x-ticks and x-tick labels to correspond to the 'Day'
xticks = df.drop_duplicates('Day')['Index']
xticklabels = df.drop_duplicates('Day')['Day']
# Adjust x-ticks by adding a half-day's worth of index
xticks_shifted = xticks + 0.75 * (xticks.max() - xticks.min()) / len(xticks)

ax.set_xticks(xticks_shifted)
ax.set_xticklabels(xticklabels, rotation=45)

# Highlight the portion between index 80 and 120
ax.axvspan(50, 130, color='yellow', alpha=0.3)

# Set the title and labels
ax.set_title('Sales per Hour for last week')
ax.set_xlabel('Day of the Week')
ax.set_ylabel('Amount')

# Display the plot in Streamlit
st.pyplot(fig)


def read_and_analyze_excel(file_path, model="gpt-3.5-turbo", temperature=0):
    # Read the Excel file using pandas
    df = pd.read_excel(file_path,nrows=125)

    # Extract relevant information from the DataFrame
    product_name = df['Date'].tolist()
    days_left = df['Time'].tolist()
    insights = df['Amount'].tolist()

    # Generate system message based on the inventory data
    system_message = f"Hourly Sales Trend in a week:"+"\n".join([f"{name}, {days}, {insight}" for name, days, insight in zip(product_name, days_left, insights)]) 

    # Generate user message based on the extracted information
    user_message = "Please respond in Bengali. Based on the Sales Data generate Insights or Suggestions which may me missed by the retail shopkeeper when he looks at this data. You can include as much analytics as you can"

    # Generate input for OpenAI based on analysis
    input = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message},
    ]

    # # Generate response using OpenAI API
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=input_for_openai,
    #     temperature=temperature,
    # )

    # return response.choices[0].content
    output = client.chat.completions.create(
        model=model,
        messages=input,
        temperature=temperature,

    )
    return output.choices[0].message.content

# def final_message(input, model="gpt-3.5-turbo", temperature=0):


# Example usage
with st.spinner('AI is generating your content. This can take a while sometimes...'):
    file_path = 'smart_sell.xlsx'
    response = read_and_analyze_excel(file_path)
    st.write(response)
    # speech_file_path = BytesIO()
    response5 = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=response
    )

    # Extract the raw bytes from the HTTP response content
    audio_bytes = response5.content

    # Convert the MP3 data to BytesIO
    audio_bytesio = BytesIO(audio_bytes)

    # Display the audio in Streamlit
    st.audio(audio_bytesio, format="audio/mp3")

    response6 = client.images.generate(
    model="dall-e-3",
    prompt="a white siamese cat",
    size="1024x1024",
    quality="standard",
    n=1,
    )

    st.write(response6)
    # response.stream_to_file(speech_file_path)
    # sound_file = BytesIO()
    # tts = gTTS(response, lang=language)
    # tts.write_to_fp(sound_file)
    # return sound_file

    # sound_file = text_to_speech(response1,selected_language)
    # st.audio(sound_file)