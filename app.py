# streamlit_app.py

import streamlit as st
from modules.question import asking_questions
from modules import LearningPath
from modules import assignment
from modules.explain import topic_explanation
from modules import code_checker
def show(response):
    import streamlit as st
    st.markdown("<h1 style='color: white;'>RoadMap To Learn</h1>", unsafe_allow_html=True)
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


def main():
   
    content_dict = {
        "RoadMap": None,
        "Explain": None,
        "assignment": None,
        
    }

    # Get user answers
    answers = asking_questions() 
    
    # Create  query strings
    assignment_query = f"Language: {answers['language']}, Learning Goal: {answers['learning_goal']}, Experience Level: {answers['experience_level']}"
    roadmap_query = f"Language: {answers['language']}, Learning Goal: {answers['learning_goal']}, Experience Level: {answers['experience_level']}, prior Experience: {answers['prior_experience']}, Learning_method: {answers['learning_methods']}, time_committment: {answers['time_commitment']}"
    Topic_query=f"Topic:{answers["topic_today"]}Language: {answers['language']}, Experience Level:{answers['experience_level']},prior_Experience:{answers["prior_experience"]},Learning_method:{answers["learning_methods"]}"
    
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "RoadMap", "Topic","Assignment","Code Checker"])


    if page == "Home":
        st.title("Welcome to Coding Buddy")

    elif page == "RoadMap":
        if content_dict["RoadMap"] is None:
            content_dict["RoadMap"] = LearningPath.roadmap(roadmap_query)
            show(content_dict["RoadMap"])
        else:
            show(content_dict["RoadMap"])


        
    elif page == "Topic":
        if content_dict["Explain"] is None:
            content_dict["Explain"] = topic_explanation(Topic_query) 
        
        show(content_dict["Explain"])

    elif page == "Assignment":
        if content_dict["assignment"] is None:
            content_dict["assignment"] = assignment.create_assignment(assignment_query)

        show(content_dict["assignment"])
    elif page == "Code Checker":
        code_checker.show()


if __name__ == "__main__":
    main()
