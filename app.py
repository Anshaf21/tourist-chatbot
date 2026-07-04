import streamlit as st
from google import genai
from streamlit_js_eval import get_geolocation

# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Tourist Guide Chatbot",
    page_icon="🗺️"
)

st.title("🗺️ Tourist Guide Chatbot")

# Live location bar 
location = get_geolocation()
 
loc_col1, loc_col2 = st.columns([4, 1])
with loc_col1:
    if location and "coords" in location:
        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]
        st.info(f"📍 Live location: {lat:.5f}, {lon:.5f}")
    else:
        st.warning("📍 Waiting for location permission... allow it in your browser.")
with loc_col2:
    if st.button("Refresh \n Location"):
        st.rerun()

# ----------------------------
# Load Knowledge Base
# ----------------------------
try:
    with open("place.txt", "r", encoding="utf-8") as f:
        kb = f.read()
except FileNotFoundError:
    kb = "No tourist information available."

# ----------------------------
# Gemini API Key
# ----------------------------
API_KEY = "AQ.Ab8RN6JXwmHVZbuR39ZJ87f8AJWLaxUCK0NPfQZVeoFRKl9SKA"   # Replace with your API key

MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = f"""
You are a helpful Tourist Guide Assistant.

Your job is to:
- Answer tourists' questions.
- Recommend nearby attractions.
- Give travel tips.
- Suggest restaurants and hotels if asked.
- Be friendly and concise.

Use the following tourist information when relevant:

{kb}
"""

# ----------------------------
# Initialize Client
# ----------------------------
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

# ----------------------------
# Initialize Chat
# ----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model=MODEL,
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

# ----------------------------
# Initialize Messages
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Display Chat History
# ----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#----------------
#    images     #
#----------------



# ----------------------------
# User Input
# ----------------------------
user_input = st.chat_input("Ask me about tourist places...")

if user_input:

    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    try:
        response = st.session_state.chat.send_message(user_input)

        answer = response.text

    except Exception as e:
        answer = f"❌ Error: UNAVILABLE"

    # Display assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
        
