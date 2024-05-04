
from openai import OpenAI
import time

def create_thread(client):
    thread = client.beta.threads.create()
    return thread.id

def get_response(client, thread_id, assistant_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

def check_code(problem_statement, code):
    import streamlit as st
    combined_query = f"{problem_statement}\n\n{code}"
    openai_api=st.secrets["code_checker"]["ai_key"]
    assistant_id=st.secrets["code_checker"]["assistant_id"]
    client = OpenAI(api_key=openai_api)
    thread_id = create_thread(client)
    messages = get_response(client, thread_id, assistant_id,combined_query)
    print(messages)
    return messages

import streamlit as st


def show():
    st.markdown("<h1 style='color: white;'>Assignment</h1>", unsafe_allow_html=True)
    
    # Add background image
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"]{
        background-image: url("https://wallpaperboat.com/wp-content/uploads/2019/10/coding-16.jpg");
        background-size: cover;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add transparent white overlay and text box
    st.markdown("""
        <style>
        .text-box {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 5px;
            border-radius: 20px;
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.4);
            margin: 5px auto;
            width: 120%;
            height: 1000px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Get user input
    problem_statement = st.text_area("Enter Problem Statement:")
    code = st.text_area("Enter Code:")

    # Run code explanation
    if st.button("Get Explanation"):
        explanation= check_code(problem_statement, code)

        # Display response
        html_content = f'<div class="text-box"><h4 style="color:black;">{explanation}</h4></div>'
        st.markdown(html_content, unsafe_allow_html=True)
