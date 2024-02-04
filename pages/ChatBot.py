import streamlit as st
import sqlite3
from openai import OpenAI
import datetime

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def generate_joke():
    # Use OpenAI to generate a joke
    joke_prompt = [
        {"role": "user", "content": "Generate a new joke related to shopkeepers."}
    ]
    joke_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=joke_prompt,
        temperature=1.8
    )
    return joke_response.choices[0].message.content

@st.cache_data
def generate_upcoming_occasions():
    # Fetch the current month
    current_month = datetime.datetime.now().strftime("%B")
    occasion_prompt = [
        {"role": "user", "content": f"Upcoming Indian festivals and occasions in {current_month} as a numbered list, don't write anything other than the list"}
    ]
    # Use OpenAI to generate information about upcoming occasions
    occasion_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=occasion_prompt,
        temperature=1.5
    )
    return occasion_response.choices[0].message.content

def customize_response(message):
    # Customize the assistant's response based on specific instructions
    # Add more logic here for additional personalizations
    return message

# Function to fetch inventory items and construct user-like messages
def get_inventory_messages():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Fetch items from the inventory
    cursor.execute("SELECT item_name, sell_price, buy_price, quantity, added_datetime FROM items")
    inventory_items = cursor.fetchall()

    # Construct user-like messages for each inventory item
    messages = []
    for item in inventory_items:
        item_name, sell_price, buy_price, quantity, added_datetime = item
        message = f"My Current Inventory - " \
                  f"• Name: {item_name} Sell Price: INR {sell_price} Buy Price: INR {buy_price} Quantity: {quantity} Added on: {added_datetime}"
        messages.append({"role": "user", "content": message})

    # Close the database connection
    conn.close()

    return messages

# Function to display the chatbot
def display_chatbot():
    st.title("skAI")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        # Welcome message with a dynamically generated joke and upcoming occasions
        joke = generate_joke()
        occasions_info = generate_upcoming_occasions()
        welcome_message = f"🛒 Welcome Mr. Assawa! Here's a fun fact for you: {joke}\n" + \
                          "\nUpcoming Indian festivals and occasions\n" + \
                          f"{occasions_info}\n" + \
                          "\nHow can I assist you today?\n"
        st.chat_message("skAI").markdown(
            customize_response(welcome_message)
        )

        # Fetch inventory messages and append them to the session state
        st.session_state.messages = get_inventory_messages()

    # Display previous messages with their respective roles
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # Ensure there is at least one user message before making a request to OpenAI
    if len(st.session_state.messages) >= 2:
        with st.spinner("Thinking..."):
            # Make a request to the OpenAI chat model
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7
            )
            assistant_response = response.choices[0].message.content

            # Display the assistant's response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

            # Save the assistant's response with its role
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Call the function to display the chatbot
display_chatbot()
