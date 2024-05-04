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

def create_assignment(query):
    import streamlit as st
    openai_key =st.secrets["assignment"]["ai_key"] 
    assistant_id = st.secrets["assignment"]["assistant_id"]
    client = OpenAI(api_key=openai_key)
    thread_id = create_thread(client)
    messages = get_response(client, thread_id, assistant_id, query)
    print(messages)
    return messages

def show(response):
    
    import streamlit as st
    st.markdown("<h1 style='color: white;'>Assignment</h1>", unsafe_allow_html=True)
    # Add background image
    #https://wallpapercave.com/wp/wp6763962.png
    page_element="""
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://wallpaperboat.com/wp-content/uploads/2019/10/coding-16.jpg");
    background-size: cover;
    }
    </style>
    """

    st.markdown(page_element, unsafe_allow_html=True)

    # Add transparent white overlay and text box
    st.markdown(
        """
    <style>
    .text-box {
        background-color: rgba(255, 255, 255, 0.9); /* Adjust opacity here */
        padding: 5px;
        border-radius: 20px;
        box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.4);
        margin: 5px auto;
        width: 120%; /* Adjust width as needed */
        height: 1500px; /* Adjust height as needed */
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Add text box
    html_content = f'<div class="text-box"><h4 style="color:black;">{response}</h4></div>'

    # Adding the HTML content to Streamlit using st.markdown
    st.markdown(html_content, unsafe_allow_html=True)

