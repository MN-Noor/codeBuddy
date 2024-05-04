

def topic_explanation(Query):
    from openai import OpenAI
    import streamlit  as st
    openai_key = st.secrets["explain"]["ai_key"]
    assistant_id = st.secrets["explain"]["assistant_id"]

    client = OpenAI(api_key=openai_key)

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=Query,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages)
    else:
        print(run.status)

    tool_outputs = []
    
    if run.required_action and run.required_action.submit_tool_outputs:
       
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name =="search_and_get_youtube_links":
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": "search youtube videos  and gives"
                })
    
   
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")
        
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages)
        return messages.data[0].content[0].text.value
    else:
        print(run.status)

def search_and_get_youtube_links(topic):
    import streamlit as st
    import requests
    max_results = 4
    api_key =st.secrets['youtube']["api_key"]
   
    url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&type=video&q={topic}'
    response = requests.get(url)
    data = response.json()
    video_info = ""  

    if 'items' in data:
        for item in data['items'][:max_results]:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_info += f"Title:{video_title}\nLink:({video_link})\n\n"  
    return video_info





