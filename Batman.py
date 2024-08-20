from openai import OpenAI
import streamlit as st
import base64

st.set_page_config(page_title="BRUCE WAYNE Chatbot",
                   page_icon="🦇", layout="centered")


def add_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    background_style = f"""
    <style>
    .stApp {{
        background-image: url(data:image/png;base64,{encoded_string});
        background-size: cover;
        background-position: center;
        color: white; /* Force text to be white */
    }}

    /* Set a dark theme for input elements */
    .stTextInput > div > div {{
        background-color: #333;
        color: white;
    }}

    .stButton > button {{
        background-color: #444;
        color: white;
        border: none;
    }}

    .stButton > button:hover {{
        background-color: #555;
        color: white;
    }}

    .stChatInput {{
        background-color: #333;
        color: white;
    }}

    .stMarkdown {{
        color: white;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: #333;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #555;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: #777;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)


add_background('bck.jpeg')  # Background image path
st.image('batmanlogo.png', width=100)  # Logo image path

st.title("BRUCE WAYNE")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"


# Ensure that the 'messages' list is initialized in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Define the Batman personality prompt
    personality_prompt = (
        "You're now embodying Batman, the Dark Knight of Gotham. As Batman, your role is to protect "
        "the innocent and uphold justice. Your responses should be vigilant, direct, and embody the "
        "essence of a hero who operates in the shadows to safeguard his city. You do not break character, "
        "and all your dialogues are from the perspective of Batman dealing with the matters of justice and "
        "emergency in Gotham City."
    )
    # Add the personality prompt to the session state messages
    st.session_state.messages.append(
        {"role": "assistant", "content": personality_prompt})
    st.session_state.messages.append(
        {"role": "assistant", "content": "I'm Batman. What's your emergency?"}
    )

# Display each message in the chat history, except the first one (which is the personality prompt)
for message in st.session_state.messages[1:]:  # Skip the first message
    with st.chat_message(message["role"], avatar="🦇" if message["role"] == "assistant" else None):
        st.markdown(
            f"<div class='st-chat-message'>{message['content']}</div>", unsafe_allow_html=True)

# Input field for the user to enter a new chat message
prompt = st.chat_input(
    "Please report your issue, Gotham depends on it...")

# If the user enters a message, process it
if prompt:
    # Append the user's message to the session state messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(
            f"<div class='st-chat-message'>{prompt}</div>", unsafe_allow_html=True)

    # Generate the assistant's response using the OpenAI API, staying in character as Batman
    with st.chat_message("assistant", avatar="🦇"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    # Add the assistant's response to the session state messages
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

