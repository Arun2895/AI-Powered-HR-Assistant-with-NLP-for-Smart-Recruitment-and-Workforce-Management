import streamlit as st
from dotenv import load_dotenv
import os
from utils.helpers import gemini_response, input_pdf_setup

# Load environment variables
load_dotenv()

# Set up Streamlit page
st.set_page_config(page_title="AI-Powered HR Assistant", page_icon=":guardsman:", layout="wide")
st.title("💼 AI-Powered HR Assistant")

# Sidebar
st.sidebar.image("assets/hr_icon.png", width=120)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Resume Tracker", "Interview Chatbot", "Role Suggestion"])

# Common Inputs
st.markdown("---")

if page == "Resume Tracker":
    st.header("🔍 ATS Resume Tracker")
    input_text = st.text_area("Job Description:")
    uploaded_file = st.file_uploader("Upload Resume (PDF):", type=["pdf"])
    submit_1 = st.button("📋 Tell me about the Resume")
    submit_2 = st.button("📈 Percentage Match")

    prompt1 = """You are an experienced HR. Review the resume against the job description. Share professional evaluation."""
    prompt2 = """You are an ATS scanner. Evaluate the resume vs job description. Return match %, missing keywords, and insights."""

    if submit_1 or submit_2:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                prompt = prompt1 if submit_1 else prompt2
                response = gemini_response(prompt, pdf_content, input_text)
                st.subheader("💬 Response")
                st.write(response)
            else:
                st.error("Error processing resume.")
        else:
            st.error("Please upload a resume.")

elif page == "Interview Chatbot":
    st.header("🤖 Interview Preparation Chatbot")
    user_question = st.text_input("Ask a question:")
    submit_q = st.button("💡 Get Answer")
    if submit_q and user_question:
        prompt = """You are an expert interview mentor. Help answer this question professionally."""
        response = gemini_response(prompt, [{"mime_type": "text/plain", "data": ""}], user_question)
        st.subheader("📝 Answer")
        st.write(response)

elif page == "Role Suggestion":
    st.header("📊 Job Role Recommendation")
    domain = st.selectbox("Choose your domain:", [
        "Software Engineering", "Web Development", "Data Science", "AI/ML", "Cybersecurity",
        "Cloud", "DevOps", "Embedded Systems", "UI/UX Design"
    ])
    submit_s = st.button("📖 Get Role Suggestions")
    if submit_s:
        prompt = f"You are a career advisor. Suggest ideal roles in {domain} and the required skills."
        response = gemini_response("", [{"mime_type": "text/plain", "data": ""}], prompt)
        st.subheader("🎯 Suggested Roles")
        st.write(response)

