import streamlit as st
import google.generativeai as genai
import pdfplumber
import tempfile

# Configure Gemini API Key
genai.configure(api_key="AIzaSyBebHKyWyXzEKyyGOyz0cioDc7d3EaYZ0Q")  # Replace with your actual Gemini API key
model = genai.GenerativeModel("gemini-2.5-pro")

st.set_page_config(page_title="AI Interview Coach", layout="centered")
st.title("🎯 AI Interview Coach")
st.markdown("Get personalized interview help using your background and resume.")

# Input fields
job_title = st.text_input("🧑‍💼 Job Title", placeholder="e.g., Software Engineer")
company_or_industry = st.text_input("🏢 Company or Industry", placeholder="e.g., Google or Tech")
experience_level = st.text_input("📈 Experience Level", placeholder="e.g., Entry-level, 2 years")
strengths = st.text_area("✅ Your Strengths", placeholder="e.g., Leadership, Creativity")
weaknesses = st.text_area("⚠️ Your Weaknesses", placeholder="e.g., Public speaking, Perfectionism")
interview_type = st.selectbox("🎯 Interview Type", ["Behavioral", "Technical", "Case Study", "HR", "Other"])

# PDF Resume Upload
resume_text = ""
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    try:
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
    except Exception as e:
        st.error("❌ Failed to read PDF. Please upload a valid resume.")
        st.stop()

# Generate Prompt
if st.button("🧠 Generate Interview Prep"):
    with st.spinner("Generating AI Response..."):
        prompt = f"""
You are a professional interview coach. Help this person prepare for an upcoming interview based on the following information:

- 🧑‍💼 Interview Role/Job Title: {job_title}
- 🏢 Company/Industry (optional): {company_or_industry}
- 📈 Experience Level: {experience_level}
- ✅ Strengths: {strengths}
- ⚠️ Weaknesses: {weaknesses}
- 🎯 Interview Type: {interview_type}

Resume content (for deeper context):
{resume_text[:2000]}  # First 2000 characters of resume to stay within token limits

Using this information, generate:
1. A personalized mindset and prep plan.
2. Suggested questions + sample answers.
3. Coaching advice tailored to their weaknesses.
4. Resume-based tips to highlight strengths.
"""

        try:
            response = model.generate_content(prompt)
            st.success("✅ Done! Here's your personalized interview prep:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"⚠️ Failed to generate response: {e}")