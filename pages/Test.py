import streamlit as st
from twilio.rest import Client
import time

# Your Account SID and Auth Token from twilio.com/console
account_sid = 'ACbc046d394f28e67d5430a662661dd8d3'
auth_token = 'bff3a3c73653b6e5d605fcffb6cc1e8f'
client = Client(account_sid, auth_token)

st.title('SMS Sender')

# Initialize messages in Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

recipient_number = st.text_input('Enter the recipient\'s phone number')
message_body = st.text_input('Enter your message')

if st.button('Send SMS'):
    message = client.messages.create(
        body=message_body,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{recipient_number}'
    )

    if message.sid:
        st.session_state['messages'].append({
            'type': 'sent',
            'content': message_body,
            'date_sent': message.date_sent
        })
        st.success('Message sent successfully')
    else:
        st.error('Failed to send message')

# Check for new messages
if st.button('Check for new messages'):
    messages = client.messages.list()
    for message in messages:
        # Only add messages that are newer than the latest message in session_state
        if (
            not st.session_state['messages'] or 
            (st.session_state['messages'][-1]['date_sent'] is not None and message.date_sent > st.session_state['messages'][-1]['date_sent'])
        ):
            # Check if the message is from the recipient and is inbound
            if message.direction == 'inbound' and message.from_ == f'whatsapp:{recipient_number}':
                st.session_state['messages'].append({
                    'type': 'received',
                    'content': message.body,
                    'date_sent': message.date_sent
                })

# Display sent and received messages
for message in st.session_state['messages']:
    if message['type'] == 'sent':
        st.write(f"You: {message['content']}")
    else:
        st.write(f"Recipient: {message['content']}")