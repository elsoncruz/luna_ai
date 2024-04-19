import streamlit as st
import os
import json
from dotenv import load_dotenv
import google.generativeai as gen_ai
from fuzzywuzzy import fuzz
load_dotenv()

st.markdown("""
    <style>
        .st-emotion-cache-janbn0{
            flex-direction:row-reverse;
            background: transparent;
            
        }
        .cus{
            position:relative;
            width:100%;
            max-width:auto;
             
        }
        .st-emotion-cache-4zpzjl{
                display:none;
                visibility:hidden;
                
            
        }
        .st-emotion-cache-18qnold{
                display:none;
                visibility:hidden;
            
        }  
        .user-box{
            text-align: center;
            background-color: rgba(0, 178, 255,50);
            color:white;
            padding: 10px;
            border-radius: 15px;
            clear: both;
            float:right;
            margin-top: 6px;
            margin-right:5px;    
        } 
        .img2 {
            width: 40px; 
            height: 40px;
            border-radius: 50%;
            border: solid;
            max-width:100%;
            margin:0 auto;
            margin-left: auto;
            float: inline-end;
        }       
        .message-box {
            text-align: left;
            float: left;
            background-color: rgba(240, 242, 246,50);
            padding: 10px;
            border-radius: 15px;
            clear: both;
            border:1px;
            color:black;  
            margin-bottom: 6px; 
        }
        img {
            margin-right:60px;
            margin-top: -12px;
            width: 40px; 
            height: 40px;
            border-radius: 50%;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown(
    """
<style>
    .st-emotion-cache-usj992{
        background-color: transparent;
    }
    [data-testid="stAppViewContainer"]{
        background-image:url("luna_ai/static/09.jpg");
        background-size:cover;
    }
</style>
""",
    unsafe_allow_html=True,
)


st.markdown("""
            <style>
            #MainMenu{visibility:hidden;}
            footer{visibility:hidden;}
            header{visibility:hidden;}
            .st-emotion-cache-15zrgzn{
                display: none;
            }
            </style>
            """,unsafe_allow_html=True)
st.markdown(
        """
        <style>
        .stChatInputContainer {
            margin-bottom:-40px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_css():
    with open("static/styles.css","r") as f:
        css=f"<style>{f.read()}</style>"
        st.markdown(css,unsafe_allow_html=True)


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


with open('own_questions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    own_questions = {item['question']: item['answer'] for item in data['questions']}


def ask_own_question(user_query):
    similarity_threshold = 85

    fill_qr = user_query.lower().strip()

    # Check for exact match
    if fill_qr in own_questions:
        return own_questions[fill_qr]
    else:
        # Find similar questions in own_questions
        similarities = {
            question: fuzz.token_set_ratio(fill_qr, question)
            for question in own_questions
        }
        best_match = max(similarities, key=similarities.get)
        
        # If similarity is above threshold, use the closest match
        if similarities[best_match] > similarity_threshold:
            return own_questions[best_match]
        else:
            # Pass to the Gemini AI model
            gemini_response = model.generate_content(user_query)
            response_text = " ".join(part.text for part in gemini_response.parts)
            return response_text
          
        
        
# Existing code...
st.title("BCA_BoT🤖\n\nelson")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.markdown('<div class="message-box">{}</div>'.format(message["role"]), unsafe_allow_html=True):
        if message["role"]=="user":
            st.markdown('<div class="cus"><img src="luna_ai/static/user.png" class="img2"></div>''<div class="user-box" style="margin-right: auto;">{}</div>'.format(message["content"]), unsafe_allow_html=True)
            pass
        else:
            st.markdown('<img src="luna_ai/static/chatbot.png" width=32 height=32>''<div class="message-box">{}</div>'.format(message["content"]), unsafe_allow_html=True)   
            pass


if prompt := st.chat_input("say"):
    st.chat_message("user").markdown('<div class="cus"><img src="luna_ai/static/user.png" class="img2"></div>''<div class="user-box">{}</div>'.format(prompt), unsafe_allow_html=True)

    st.session_state.messages.append({"role":"user","content": prompt})

    response = ask_own_question(prompt)

    with st.chat_message("🤖"):
        st.markdown('<img src="luna_ai/static/chatbot.png" width=32 height=32>''<div class="message-box">{}</div>'.format(response), unsafe_allow_html=True)

    st.session_state.messages.append({"role":"🤖","content":response})


