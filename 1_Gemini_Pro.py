
import requests
import re
import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS


st.set_page_config(
    page_title="Chat To ZenBot",
    page_icon="🔥",
    initial_sidebar_state="collapsed" 
)

st.title("Chat To ZenBot")
st.caption("a chatbot, based on zendesk data.")
 
icon_pattern = re.compile(r'\[T\d\]')  
headers = { 
    "atoken" : "68VPUcYDMHFdi6SiG7uCb",
    "chatpdf-idtoken" : "eyJhbGciOiJSUzI1NiIsImtpZCI6IjMzMDUxMThiZTBmNTZkYzA4NGE0NmExN2RiNzU1NjVkNzY4YmE2ZmUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQXBvb3J2IEJhbGV0aWEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS2dRaHVqMURsSkV5dHQtZlQyT3BZaExkZDIzNWRQX3RsZ0toNG9LWTFZMUxwNlVnPXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3RhbGstdG8tYW55dGhpbmciLCJhdWQiOiJ0YWxrLXRvLWFueXRoaW5nIiwiYXV0aF90aW1lIjoxNzE2Mzc5Mzk0LCJ1c2VyX2lkIjoiNVVldjRzQWt4ZU42TE5LczFYQjZRYUlQSlpiMiIsInN1YiI6IjVVZXY0c0FreGVONkxOS3MxWEI2UWFJUEpaYjIiLCJpYXQiOjE3MTgzMTUxMzIsImV4cCI6MTcxODMxODczMiwiZW1haWwiOiJidW5ueWJhbGF0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE2MjAzMjY5Njc2MDE0NTE4NTY0Il0sImVtYWlsIjpbImJ1bm55YmFsYXRAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.DrfsB3_PSLGC9DK_GUGCKNkfnYsdjWaJytCtsXWcWdX9cFM8ulyADK6fAtM1_kz90BVNIQtoI5CuStM3JGLJ2glDCOnsimYkJM7k8NerMnpKS3x1_LommAQe_U_XFWgTx66Ys8rQBXq9YemPvciqDUM2IWvHHF70gt0yjGWGQJkzRiiqENBQd_Fz3pLrXgNohz07fr0jsfmPhxIgUO40CGWOlld_M1V5F9KKrEsm6-ClheCESn9VXHhx0Xx_MX03lJsh2LoNQRsB7ECBUGOkXYIzzzRNW_e-dVqt3pd27uYR5o2h3NDee2B7SMwDbsJAHpNcKQyEONA0EjGrCv_pdA",
    "Content-Type": "application/json", 
} 
 
if "app_key" not in st.session_state:
    app_key = st.secrets["gemini_key"]
    if app_key:
        st.session_state.app_key = app_key

if "history" not in st.session_state:
    st.session_state.history = []
 

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width = True, type="primary"):
        st.session_state.messages = []
        st.rerun()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask something"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    casualFlag = 0
    if ( prompt.lower()=="hi" or prompt.lower()=="hello" or prompt.lower()=="greetings" or prompt.lower()=="yes" or prompt.lower()=="no" or prompt.lower()=="ok" or prompt.lower()=="okay" or prompt.lower()=="thanks" or prompt.lower()=="thank you" or prompt.lower()=="bye" ) :
        casualFlag = 1
    
    epoch_time = int(time.time())
    data = {
        "v": 2,
        "chatSession": {
            "type": "join",
            "chatId": "cha_1oNtB90HT9T6bW8imTNyp"
        },
        "history": [
            { 
            "author": "uplaceholder",
            "msg": prompt,
            "time": epoch_time
            }
        ]
    } 
    response = requests.post('https://chat-pr4yueoqha-ue.a.run.app/', headers=headers, json=data) 
    content = "" 

    if response.status_code == 200: 
        content =  response.content.decode("utf-8")
        print(content) 
    
    if content != "":
        content = content.split("\n",1)[1] 
    else :
        content = "Couldn't Connect to Cloud" 
             
        
    x = re.findall(icon_pattern, content) 
    content = icon_pattern.sub("", content) 
 
    if len(x) == 0 and casualFlag == 0 : 
        content =  "I apologize, but I cannot provide an answer to your question as the information provided in my knowledgebase is not enough." 

    response = content
    # Display assistant response in chat message container
    with st.chat_message("assistant"): 
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})