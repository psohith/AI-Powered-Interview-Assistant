import streamlit as st
import requests
import os

# Backend URLs
UPLOAD_RESUME_URL = "http://localhost:5000/upload_resume"
CHAT_URL = "http://localhost:5000/chat"


if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False
if "file_id" not in st.session_state:
    st.session_state.file_id = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Resume Interview Bot", layout="centered", initial_sidebar_state="collapsed")


def render_chat():
    """Function to render chat messages dynamically."""
    with chat_container.container():
        st.markdown(
            """
            <style>
                .chat-container {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    margin-top: 20px;
                }
                .chat {
                    display: flex;
                    align-items: flex-start;
                    margin: 5px 0;
                }
                .chat.user {
                    justify-content: flex-end;
                }
                .chat.bot {
                    justify-content: flex-start;
                }
                .bubble {
                    padding: 12px 15px;
                    border-radius: 15px;
                    max-width: 70%;
                    font-size: 14px;
                    line-height: 1.5;
                    word-wrap: break-word;
                }
                .gradient-border {
                    background: linear-gradient(135deg, #76c7c0, #34a0a4);
                    color: #fff;
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                }
                .bot-bubble {
                    background: #f1f1f1;
                    color: #333;
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f"""
                    <div class="chat user">
                        <div class="bubble gradient-border">{message['content']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat bot">
                        <div class="bubble bot-bubble">{message['content']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)


def upload_resume_section():
    """Handles the resume upload and communication with the backend."""
    if not st.session_state.resume_uploaded:
        st.write("### Upload Your Resume")
        uploaded_file = st.file_uploader("Upload a PDF file of your resume", type=["pdf"])

        if uploaded_file is not None:
            temp_file_path = f"temp_{uploaded_file.name}"

            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())

            with open(temp_file_path, "rb") as temp_file:
                response = requests.post(UPLOAD_RESUME_URL, files={"file": temp_file})

            if response.status_code == 200:
                response_data = response.json()
                st.session_state.file_id = response_data.get("file_id", "")
                st.session_state.resume_uploaded = True
                st.success("Resume uploaded successfully! You can now start asking questions.")
            else:
                st.error("Failed to process the uploaded resume. Please try again.")
            os.remove(temp_file_path)

def chat_section():
    """Handles the chat interface and communication with the backend."""
    if st.session_state.resume_uploaded:
        st.write("### Ask Interview Questions")
        with st.form("user_input_form", clear_on_submit=True):
            user_input = st.text_input("", placeholder="Type your question...", label_visibility="collapsed")
            submit = st.form_submit_button("Send")

        if submit and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            render_chat()  
            response = requests.post(
                CHAT_URL,
                json={
                    "question": user_input,
                    "file_id": st.session_state.file_id,
                },
            )

            if response.status_code == 200:
                bot_reply = response.json().get("answer", "")
                st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
                render_chat() 
            else:
                st.error("Failed to get a response from the bot. Please try again.")



st.title("AI-Powered Interview Assistant")
st.subheader("Upload your resume and start practicing interview questions!")

chat_container = st.empty()
upload_resume_section()
chat_section()

