import streamlit as st
from openai import OpenAI
import datetime

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

class ChatBot:
    def __init__(self):
        pass

    def generate_joke(self):
        # Use OpenAI to generate a joke
        joke_prompt = [
        {"role": "user", "content": "Generate a grocery-related joke."}
        ]
        joke_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=joke_prompt,
            temperature=0.5,
            max_tokens=50
        )
        return joke_response.choices[0].message.content

    def generate_upcoming_occasions(self):
        # Fetch the current month
        current_month = datetime.datetime.now().strftime("%B")
        occasion_prompt = [
        {"role": "user", "content": f"Upcoming Indian festivals and occasions in {current_month}."}
        ]
        # Use OpenAI to generate information about upcoming occasions
        occasion_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=occasion_prompt,
            temperature=0.5,
            max_tokens=100
        )
        return occasion_response.choices[0].message.content

    def customize_response(self, message):
        # Customize the assistant's response based on specific instructions
        # Add more logic here for additional personalizations
        return message

    def display_chatbot(self):
        st.title("skAI")

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display previous messages with their respective roles
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if not st.session_state.messages:
            # Welcome message with a dynamically generated joke and upcoming occasions
            joke = self.generate_joke()
            occasions_info = self.generate_upcoming_occasions()
            #pre_instructions = "Feel free to ask about grocery-related information, upcoming occasions, or request a joke! You can guide the conversation."

            welcome_message = f"🛒 Welcome Mr. Assawa! Here's a fun fact for you: {joke}\n" + f"\nAlso, in {occasions_info}\n" + "\nHow can I assist you today?\n"

            st.chat_message("skAI").markdown(
                self.customize_response(welcome_message)
            )

        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            # Add clickable prompt suggestions
            st.write("Choose a suggestion:")
            suggestion_options = ["Tell me a joke", "Upcoming occasions", "Recommend groceries"]
            selected_suggestion = st.selectbox("", suggestion_options)

            # Process the user's selection
            if selected_suggestion == "Tell me a joke":
                full_response = self.generate_joke()
            elif selected_suggestion == "Upcoming occasions":
                full_response = self.generate_upcoming_occasions()
            elif selected_suggestion == "Recommend ":
                # Add logic for grocery recommendations
                full_response = "Here are some recommended groceries: ..."
            else:
                full_response = "How can I assist you today?"
            # Add the conversation context and instructions to the OpenAI prompt
            pre_instructions = "Feel free to ask about grocery-related information, upcoming occasions, or request a joke! You can guide the conversation."
            openai_prompt = f"{pre_instructions}\n" + "\n".join([m["content"] for m in st.session_state.messages])
            openai_response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                prompt=openai_prompt,
                temperature=0.5,
                max_tokens=150
            )

            # Assistant role and message
            with st.chat_message("skAI"):
                message_placeholder = st.empty()
                full_response = openai_response.choices[0].message.content
                message_placeholder.markdown(full_response + "▌")

            # Customize the assistant's response and save it with its role
            custom_response = self.customize_response(full_response)
            st.session_state.messages.append({"role": "assistant", "content": custom_response})

    def run_web_app(self):
        self.display_chatbot()