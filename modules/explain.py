from openai import OpenAI
#creating assistant
# def create_assistant():
#     from openai import OpenAI
#     client = OpenAI()
#     assistant = client.beta.assistants.create(
#     instructions="you are an experienced professor you have to explain the topic that the user asks you about and you have to break down the complex topic and explain it in detail depending upon user experience and also recommend user videos by correct video links to the user .you cannot recommend books if user prefer reading generate him good explanation and if user prefer tutorials recommend youtube videos in end.if user prefer visual learning",
#     model="gpt-3.5-turbo-0613",
#     tools=[
#         {
#         "type": "function",
#         "function": {
#         "name": "search_and_get_youtube_links",
#         "description": "Search YouTube for videos related to a given topic and retrieve their titles and URLs.",
#         "strict": false,
#         "parameters": {
#             "type": "object",
#             "properties": {
#             "topic": {
#                 "type": "string",
#                 "description": "The topic or keyword for which you want to search YouTube videos."
#             }
#             },
#             "required": [
#             "topic"
#             ]
#         }
#         }
#         }])
        
def topic_explanation(Query):
    from openai import OpenAI
    import streamlit  as st
    openai_key =st.secrets["assignment"]["ai_key"] 
    assistant_id =st.secrets["explain"]["assistant_id"]
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
                    "output": "youtube titles and links"
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
    api_key = st.secrets['youtube']["api_key"]
   
    url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&type=video&q={topic}'
    response = requests.get(url)
    data = response.json()
    video_links = []
    for item in data["items"]:  # Access the "items" part of the response JSON
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        video_links.append({"title": video_title, "url": video_url})

    return video_links

# # print(search_and_get_youtube_links("python while loop"))
# print(topic_explanation("Python while loop video"))




