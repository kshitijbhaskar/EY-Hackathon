import sqlite3
import streamlit as st
import calendar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from datetime import datetime,date
from gtts import gTTS
from io import BytesIO
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def predict_price(sku_id):
  sku_id = sku_id
  return 1000

@staticmethod
def plot_rates(analytics_df):
    # Plotting selling rates and buying rates
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(analytics_df['SKU_ID'], analytics_df['Selling Rate'], label='Selling Rate', marker='o')
    ax.plot(analytics_df['SKU_ID'], analytics_df['Buying Rate'], label='Buying Rate', marker='o')

    ax.set_title('Selling and Buying Rates Over SKU Units')
    ax.set_xlabel('SKU Unit')
    ax.set_ylabel('Rate')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=90)

    return fig, ax

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


def fetch_old_price(sku_id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT sell_price FROM items WHERE sku_id=?", (sku_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None

def is_sku_in_inventory(sku_id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=?", (sku_id,))
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

@st.cache_data
def final_message(input, model="gpt-3.5-turbo", temperature=0):

    output = client.chat.completions.create(
        model=model,
        messages=input,
        temperature=temperature,

    )
    return output.choices[0].message.content


@st.cache_data
def text_to_speech(response,selected_language):
    language = "en"
    if selected_language == "English":
        language = "en"
    elif selected_language == "Hindi":
        language = "hi"
    elif selected_language == "Bengali":
        language = "bn"
    output = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=response
    )
    audio_bytes = output.content

    # Convert the MP3 data to BytesIO
    audio_bytesio = BytesIO(audio_bytes)
    return audio_bytesio

@st.cache_data
def get_top_suggestions_for_month(month_number):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Get items added in the selected month
    cursor.execute("SELECT sku_id, item_name, quantity, added_datetime FROM items WHERE strftime('%m', added_datetime) = ?",
                   (f"{month_number:02d}",))
    items_added_in_month = cursor.fetchall()

    # Read predicted price increase from analytics.xlsx
    analytics_df = pd.read_excel("analytics.xlsx")
    price_increase_dict = dict(zip(analytics_df['SKU_ID'], analytics_df['Predicted Price after 15 days (%)']))

    suggestions = []
    increased_sales_items = set()

    for sku_id, item_name, quantity, added_datetime in items_added_in_month:
        old_price = fetch_old_price(sku_id)
        new_price = predict_price(sku_id)

        if old_price is not None and new_price is not None:
            profit_percent = (new_price - old_price) / old_price
            predicted_price_increase = price_increase_dict.get(sku_id, 0)

            suggestions.append({
                "sku_id": sku_id,
                "item_name": item_name,
                "quantity": quantity,
                "added_datetime": added_datetime,
                "profit_percent": profit_percent,
                "predicted_price_increase": predicted_price_increase
            })

            # Check if sales increased compared to the previous month
            cursor.execute("SELECT COUNT(*) FROM items WHERE sku_id=? AND strftime('%m', added_datetime) = ?",
                           (sku_id, f"{month_number:02d}"))
            # count = cursor.fetchone()[0]

            # if count > 0:
            increased_sales_items.add(item_name)

    # Sort suggestions by profit_percent in descending order
    suggestions.sort(key=lambda x: x["profit_percent"], reverse=True)

    conn.close()

    # Return the top ten suggestions and items with increased sales
    return suggestions[:10], list(increased_sales_items)

@st.cache_data
def display_suggestion_card(suggestion):
    
    # st.divider()
    st.write(f"**Item Name:** {suggestion['item_name']}")
    # st.write(f"**Price Increase:** {suggestion['price_increase']:.2%}")

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



# Display header message
# if increased_sales_items:
# messages_5 =  [
# {'role':'system',
# 'content':f"""Please respond in {selected_language} language,You need to analyze the input and provide a concise headline of 10-20 words, highlighting key items for restocking."""},
# {'role':'user',
# 'content':f"""{response}"""},
# ]


selected_option = st.sidebar.radio("Choose a tab", ["Selling", "Inventory", "Buying"])
# response1 = final_message(messages_5, temperature=1)

if selected_option == "Selling":
    st.title("Age, Gender and Category-wise Sales Distribution")
    @st.cache_data
    def read_and_analyze_excel(file_path, selected_language):
        # Read the Excel file using pandas
        df = pd.read_excel(file_path,nrows=125)

        # Extract relevant information from the DataFrame
        product_name = df['Date'].tolist()
        days_left = df['Time'].tolist()
        insights = df['Amount'].tolist()

        # Generate system message based on the inventory data
        system_message = f"Hourly Sales Trend in a week:"+"\n".join([f"{name}, {days}, {insight}" for name, days, insight in zip(product_name, days_left, insights)]) 

        # Generate user message based on the extracted information
        user_message = f"Please respond in {selected_language} language, Based on the Sales Data generate Insights or Suggestions which may me missed by the retail shopkeeper when he looks at this data. You can include as much analytics as you can. I need only top 3 top points in a concise way!"

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
            model="gpt-3.5-turbo",
            messages=input,
            temperature=0.75,
        )
        return output.choices[0].message.content
    @st.cache_data
    def read_and_analyze_excel1(file_path, selected_language):
        # Read the Excel file using pandas
        df = pd.read_excel(file_path,nrows=125)

        # Extract relevant information from the DataFrame
        category = df['Category'].tolist()
        gender = df['Gender'].tolist()
        age = df['Age'].tolist()
        amount = df['Amount'].tolist()

        # Generate system message based on the inventory data
        system_message = f"Data on: category, gender, age and amount contributed wise:"+"\n".join([f"{category}, {gender}, {age}, {amount}" for category, gender, age, amount in zip(category, gender, age, amount)]) 

        # Generate user message based on the extracted information
        user_message = f"Please respond in {selected_language} language, Based on the Category Data generate Insights or Suggestions which may include most popular items in a given category (i.e. gender, age, etc) and the contribution amount of each category to the total revenue. Protein Supplements has 35 percent, Grocery has 45 percent and Stationery has 20 percent contribution to the total revenue/amount"

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
            model="gpt-3.5-turbo",
            messages=input,
            temperature=0.75,

        )
        return output.choices[0].message.content

    # def final_message(input, model="gpt-3.5-turbo", temperature=0):


    # Example usage
    with st.spinner('AI is generating your content. This can take a while sometimes...'):
        selected_language = st.selectbox("Select Language", ["English", "Hindi", "Bengali"])
        
        file_path = 'smart_sell.xlsx'
        response = read_and_analyze_excel(file_path,selected_language)
        response1 = read_and_analyze_excel1('Sky_smart_suggest.xlsx',selected_language)
        st.write("Play the Audio")
        sound_file = text_to_speech(response1,selected_language)
        st.audio(sound_file)
        st.divider()
        container = st.container(border=True)
        container.write(response1)
        st.divider()

        st.title("Time of the Day Sales Pattern")

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
        ax.axvspan(30, 100, color='green', alpha=0.3)

        # Set the title and labels
        ax.set_title('Sales per Hour for last week')
        ax.set_xlabel('Day of the Week')
        ax.set_ylabel('Amount')

        # Display the plot in Streamlit
        st.pyplot(fig)
        st.write("Play the Audio")
        sound_file = text_to_speech(response,selected_language)
        st.audio(sound_file)
        st.divider()
        container = st.container(border=True)
        container.write(response)
        st.divider()

elif selected_option == "Inventory":

    st.title("Smart Inventory Restocking")
    selected_language = st.selectbox("Select Language", ["English", "Hindi", "Bengali"])
    st.divider()
    # st.markdown(
    #     f"""
    #     <div style='padding: 10px; border: 1px solid #d3d3d3; border-radius: 5px;'>
    #         <h1>{"response"}</h1>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    # st.divider()
    # st.markdown(
    #     f"""
    #     <div style='padding: 10px; border: 1px solid #d3d3d3; border-radius: 5px;'>
    #         <h1>{"response"}</h1>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    st.subheader("The following stocks need urgent restocking as they will last for less than 15 days")
    st.divider()
    
    with st.spinner('AI is generating your content. This can take a while sometimes...'):
        # Read data from analytics.xlsx
        analytics_df = pd.read_excel("analytics.xlsx")

        first_5_items = analytics_df.head(5)

        with st.expander("Items that are going out of Stock"):
            for index, row in first_5_items.iterrows():
                name = row['Product Name']
                days = row['Days left']
                profit = row['Profit']
                
                # time_to_last = self.calculate_time_to_last(selling_rate, current_stock)
                messages =  [
                {'role':'system',
                'content':f"""Please respond in {selected_language} language, always respond as if you know all the data I've provided you and you have analysed the entire data as you are an insights providing assistant at Assawa Store for example don't say "based on data provided" instead say "on analysing your inventory and sales data" or something similar, specializing in efficient inventory management. I need you to SUGGEST me possible discount percentage for each item, given that I'm facing some serious competition this month in the market. Data is fed to you inorder of - product name, days left in stock and profit percentage."""},
                {'role':'user',
                'content':f"""{name}, {days}, {profit}"""},
                ]
                # print(response)
                with st.spinner('Loading items. Please wait...'):
                    response = final_message(messages, temperature=0.8)
                    st.warning(response)
                
        # Adding "Show More" button
        # Read data from analytics.xlsx
        analytics_df = pd.read_excel("analytics.xlsx")

        first_5_items = analytics_df.head(5)

        with st.expander("Items that are going to Expire"):
            for index, row in first_5_items.iterrows():
                name = row['Product Name']
                expiry = row['Expiry']
                insight = row['Insights']
                
                # time_to_last = self.calculate_time_to_last(selling_rate, current_stock)
                messages =  [
                {'role':'system',
                'content':f"""Please respond in {selected_language} language, You are an assistant at Assawa Store, specializing in efficient inventory management. You need to generate insights or suggestions about what to do if this product is going to expire in less than 30 days(expiry for this item is {expiry}days). If its expiry is not less than 30 days then just say "No suggestions for {name}". I just need top 3 suggestions, format your response efficiently."""},
                {'role':'user',
                'content':f"""{name}, {expiry}, {insight}"""},
                ]
                # print(response)
                with st.spinner('Loading items. Please wait...'):
                    response = final_message(messages, temperature=1)
                    st.warning(response)
                
        # Adding "Show More" button
        if st.button("Show More"):
            # Creating an expander for the remaining items
            with st.expander("Remaining Items"):
                # Fetching and displaying remaining items
                remaining_items = analytics_df.iloc[5:]
                with st.spinner('AI is generating your content. This can take a while sometimes...'):
                    for index, row in remaining_items.iterrows():
                        name = row['Product Name']
                        expiry = row['Expiry']
                        insight = row['Insights']
                        
                        # time_to_last = self.calculate_time_to_last(selling_rate, current_stock)
                        messages =  [
                        {'role':'system',
                        'content':f"""Please respond in {selected_language} language, You are an assistant at Assawa Store, specializing in efficient inventory management. You need to generate insights or suggestions about what to do if this product is going to expire in less than 30 days(expiry for this item is {expiry}days). If its expiry is not less than 30 days then just say "No suggestions for {name}". I just need top 3 suggestions, format your response efficiently."""},
                        {'role':'user',
                        'content':f"""{name}, {expiry}, {insight}"""},
                        ]
                        # print(response)
                        with st.spinner('Loading items. Please wait...'):
                            response = final_message(messages, temperature=1)
                            st.warning(response)
        st.divider()
        st.page_link("pages/PersonalisedMarketing.py")
        

elif selected_option == "Buying":
    st.title("Smart Buying Suggestions")
    selected_language = st.selectbox("Select Language", ["English", "Hindi", "Bengali"])
    # Get the current ongoing month
    current_month = datetime.now().strftime("%B")
    # User input for the month with the default value set to the current month
    selected_month = st.selectbox("Select Month:", list(calendar.month_name)[1:], index=list(calendar.month_name).index(current_month)-1)

    month_number = list(calendar.month_name).index(selected_month)
    suggestions, increased_sales_items = get_top_suggestions_for_month(month_number)
    # Process items added in the selected month
    messages_6 =  [
    {'role':'system',
    'content':f"""My inventory: {suggestions}"""},
    {'role':'user',
    'content':f"""Please respond in {selected_language} language, based on my inventory and considering that I want insights for the month {selected_month} and upcoming festivals and events that happen this month in New Delhi, India and today is {date.today()}, can you recommend the percentage I should/can increase in quantity considering the provided price increase of each item after 15 days along with your reasoning behind it (try to also consider the type of the item, predicted price after 15 days and current day and time of the year)? To be more specific can you also suggest the date before which I should increase its stock (don't simply assume it to be after 15 days, you should choose this date according to all the information provided to you)? Also can you include a table in your response so that it is easier to see what percentage increase in stock you recommend for each item?"""},
    ]
    response2 = final_message(messages_6, temperature=0.8)
    # print(response2)
    st.write("Play the Audio")
    sound_file = text_to_speech(response2,selected_language)
    st.audio(sound_file)
    st.divider()
    response2
    # Extract the CSV portion from the response
    # Remove leading/trailing spaces from column names
    # start_index = response2.find('| SKU ID')
    # end_index = response2.find('Please note that', start_index)
    # csv_data = response2[start_index:end_index]

    # # Read CSV data into a Pandas DataFrame
    # df = pd.read_csv(io.StringIO(csv_data), sep='|', skipinitialspace=True)

    # df.columns = df.columns.str.strip()

    # # Set 'SKU ID' as the index
    # st.line_chart(df.set_index('SKU ID'))
    # # Display the DataFrame
    # st.write(df)

    # # Plot the data using line_chart
    # st.line_chart(df.set_index('SKU ID'))
    messages_4 =  [
    {'role':'system',
    'content':"""As the intelligent assistant for Assawa grocery stores, you deliver comprehensive pop-up alerts (80-100 words) guiding the restocking of key items to maximize profits. In your suggestions, you consider the current month, analyzing the demand for grocery items based on local trends, festivals in the Indian month, prevailing weather conditions, and other factors such as holidays. Your insights aim to optimize the store's inventory and cater to the specific needs of customers during various occasions and seasons."""},
    {'role':'user',
    'content':f"""Please respond in {selected_language} language, Give alert message for the month {selected_month}, use emojies and format the mesaage beautifully using bullet points, bold letters , italics"""},
    ]
    with st.spinner('AI is generating your content. This can take a while sometimes...'):
        response1 = final_message(messages_4, temperature=1)
        st.markdown(
            f"""
            <div style='padding: 10px; border: 1px solid #d3d3d3; border-radius: 5px;'>
                <h1>{response1}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()
        for suggestion in suggestions:
            display_suggestion_card(suggestion)
        with st.expander("Sales Prediction"):
            analytics_df = pd.read_excel("analytics.xlsx")
            fig, ax = plot_rates(analytics_df)
            st.pyplot(fig)
# Displaying a card
# Displaying a card-like layout using markdown with CSS styling
# st.markdown(
#     f"""
#     <div style='padding: 10px; border: 1px solid #d3d3d3; border-radius: 5px;'>
#         <h3 style='color: white;'>{response1}</h3>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
# # st.markdown(f"## {response1}")
# with st.expander(f"## {response1}"):
#     st.subheader(response)


# elif suggestions:
#     st.header(f"No items with increased sales in the month of {selected_month}.")
# else:
#     st.header("No recommendations this month.")

# Display suggestions in three card-like containers
# for suggestion in suggestions:
#     display_suggestion_card(suggestion)


# def fetch_data_from_excel(self, SKU_ID, analytics_df):
#     # Filter the dataframe based on SKU_ID
#     item_data = analytics_df[analytics_df['SKU_ID'] == SKU_ID]
    
#     # Extract selling rate and current stock (quantity)
#     selling_rate = item_data['Selling Rate'].values[0]
#     current_stock = item_data['Stock in Inventory(In KG for GROCERY)'].values[0]

#     return selling_rate, current_stock

# @staticmethod
# def calculate_time_to_last(selling_rate, current_stock):
#     if selling_rate > 0:
#         time_to_last = current_stock / selling_rate
#     else:
#         time_to_last = float('inf')
#     return time_to_last

# st.title("Restocking Alert")
# st.divider()
# st.subheader("The following stocks need urgent restocking as they will last for less than 15 days")

# Read data from analytics.xlsx
# analytics_df = pd.read_excel("analytics.xlsx")

# first_5_items = analytics_df.head(5)

# with st.expander("Show Items"):
#     for index, row in first_5_items.iterrows():
#         name = row['Product Name']
#         days = row['Days left']
#         insight = row['Insights']
        
#         # time_to_last = self.calculate_time_to_last(selling_rate, current_stock)
#         messages =  [
#         {'role':'system',
#         'content':"""You are an assistant at Assawa Store, specializing in efficient inventory management. Your responsibility includes issuing alerts for items requiring restocking and estimating the remaining days before they run out of stock, and insights overview. Input provides item name along with the corresponding number of days until depletion and one insights"""},
#         {'role':'user',
#         'content':f"""{name}, {days}, {insight}"""},
#         ]
#         response = final_message(messages, temperature=1)
#         # print(response)
#         st.warning(response)
        
# # Adding "Show More" button
# if st.button("Show More"):
#     # Creating an expander for the remaining items
#     with st.expander("Remaining Items"):
#         # Fetching and displaying remaining items
#         remaining_items = analytics_df.iloc[5:]
        
#         for index, row in remaining_items.iterrows():
#             name = row['Product Name']
#             days = row['Days left']
#             insight = row['Insights']
            
#             # time_to_last = self.calculate_time_to_last(selling_rate, current_stock)
#             messages =  [
#             {'role':'system',
#             'content':"""You are an assistant at Assawa Store, specializing in efficient inventory management. Your responsibility includes issuing alerts for items requiring restocking and estimating the remaining days before they run out of stock, and insights overview. Input provides item name along with the corresponding number of days until depletion and one insights"""},
#             {'role':'user',
#             'content':f"""{name}, {days}, {insight}"""},
#             ]
#             response = final_message(messages, temperature=1)
#             # print(response)
#             st.warning(response)


# def get_sku_units_needing_restock(self, analytics_df):
#     items_needing_restock = []

#     for SKU_ID in analytics_df['SKU_ID']:
#         selling_rate, current_stock = self.fetch_data_from_excel(SKU_ID, analytics_df)
#         time_to_last = self.calculate_time_to_last(selling_rate, current_stock)

#         if time_to_last < 5:
#             items_needing_restock.append(SKU_ID)

#     return items_needing_restock



# Plotting selling rates and buying rates
# if st.button("Show Graph",type="primary"):
#     fig, ax = plot_rates(analytics_df)
#     st.pyplot(fig)