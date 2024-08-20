from openai import OpenAI
import streamlit as st
import base64

st.set_page_config(page_title="BRUCE WAYNE Chatbot",
                   page_icon="🦇", layout="centered")

# Function to add a custom background and font


def add_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    background_style = f"""
    <style>
    @font-face {{
        font-family: 'BatmanFont';
        src: url('data:font/ttf;base64,{base64.b64encode(open('batmfa__.ttf', 'rb').read()).decode()}') format('truetype');
    }}

    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        color: #FFEB3B; /* Yellow text */
        font-family: 'BatmanFont', sans-serif;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: #FFEB3B;
        font-family: 'BatmanFont', sans-serif;
    }}

    /* Set a dark theme for input elements with yellow highlights */
    .stTextInput > div > div {{
        background-color: #444;
        color: #FFEB3B;
        border: 2px solid #FFEB3B;
        font-family: 'BatmanFont', sans-serif;
    }}

    .stButton > button {{
        background-color: #FFEB3B;
        color: #2C2C2C;
        border: 2px solid #FFEB3B;
        font-family: 'BatmanFont', sans-serif;
    }}

    .stButton > button:hover {{
        background-color: #FFD700; /* Lighter yellow on hover */
        color: #2C2C2C;
    }}

    .stChatInput {{
        background-color: #444;
        color: #FFEB3B;
        border: 2px solid #FFEB3B;
        font-family: 'BatmanFont', sans-serif;
    }}

    .stMarkdown {{
        color: #FFEB3B;
        font-family: 'BatmanFont', sans-serif;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: #333;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #FFEB3B;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: #FFD700;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)


# Use the correct path for your image
add_background('bck.jpeg')  # Background image path
st.image('batmanlogo.png', width=100)  # Logo image path

# Set the title
st.title("BRUCE WAYNE")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session state initialization
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input prompt for user query
prompt = st.chat_input(
    "Enter your query, citizen... or face the consequences.")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    personality_prompt = (
        "You are Bruce Wayne, also known as Batman. When you talk, you have a deep, commanding voice. "

    )
    st.session_state.messages.append(
        {"role": "system", "content": personality_prompt})

    with st.chat_message("Batman"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append(
        {"role": "Batman", "content": response})
