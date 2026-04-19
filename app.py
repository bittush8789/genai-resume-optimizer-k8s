import streamlit as st
import os
from dotenv import load_dotenv
from database import init_db, get_db, SessionLocal
from auth import init_session_state, login, logout, create_user, authenticate_user
import pandas as pd

load_dotenv()

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #4F46E5;
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        color: #1F2937 !important;
    }
    .card p, .card li, .card span, .card div {
        color: #1F2937 !important;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        text-align: center;
        border-top: 4px solid #4F46E5;
        color: #1F2937 !important;
    }
    h1, h2, h3 {
        color: #1F2937;
    }
</style>
""", unsafe_allow_html=True)

# Initialize DB and Session
init_db()
init_session_state()

def main():
    # Sidebar Navigation
    with st.sidebar:
        st.title("🚀 CareerAI")
        st.markdown("---")
        
        if not st.session_state.authenticated:
            menu = ["Login", "Signup"]
            choice = st.selectbox("Menu", menu)
            
            if choice == "Login":
                st.subheader("Login to your account")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.button("Login"):
                    db = SessionLocal()
                    user = authenticate_user(db, email, password)
                    db.close()
                    if user:
                        login(user)
                        st.success(f"Welcome back, {user.name}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
            
            else:
                st.subheader("Create a new account")
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                if st.button("Signup"):
                    db = SessionLocal()
                    try:
                        create_user(db, new_name, new_email, new_password)
                        st.success("Account created successfully! Please login.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        db.close()
        
        else:
            st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
            menu = ["🏠 Home", "🔍 Resume Analyzer", "🛠️ AI Tools", "🕒 History"]
            choice = st.radio("Navigation", menu)
            
            st.markdown("---")
            if st.button("Logout"):
                logout()

    # Main Content Area
    if not st.session_state.authenticated:
        # Public Landing Page
        render_landing_page()
    else:
        # Routes
        if choice == "🏠 Home":
            render_home()
        elif choice == "🔍 Resume Analyzer":
            render_analyzer()
        elif choice == "🛠️ AI Tools":
            render_tools()
        elif choice == "🕒 History":
            render_history()

def render_landing_page():
    st.title("Unlock Your Career Potential with AI")
    st.markdown("""
    ### Optimize your resume for ATS and get more interviews.
    Our AI-powered platform helps you:
    - **Analyze** your resume against specific job descriptions.
    - **Improve** your ATS score with keyword optimization.
    - **Generate** high-impact cover letters in seconds.
    - **Prepare** for interviews with personalized questions.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **ATS Scoring**\nGet instant feedback on how your resume performs.")
    with col2:
        st.success("📝 **Smart Rewriting**\nProfessionally rewrite bullet points for impact.")
    with col3:
        st.warning("🎯 **Targeted Prep**\nGenerate role-specific interview questions.")
        
    st.image("https://images.unsplash.com/photo-1586281380349-632531db7ed4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", use_column_width=True)

def render_home():
    st.title("Welcome to your Dashboard")
    st.write("Ready to land your dream job? Start by analyzing your resume or using our AI tools.")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Analyze Resume")
            st.write("Compare your resume with a job description to see your match score.")
            if st.button("Start Analysis"):
                st.session_state.choice = "🔍 Resume Analyzer" # Note: choice is local to main, this won't work directly but indicates intent
                st.write("Use the sidebar to navigate to Resume Analyzer")
            st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Cover Letter Gen")
            st.write("Generate a custom cover letter based on your experience.")
            st.write("Use the sidebar to navigate to AI Tools")
            st.markdown('</div>', unsafe_allow_html=True)

def render_analyzer():
    from utils.parser import parse_resume
    from utils.ai_chains import analyze_resume_llm
    from database import Resume, Report
    import json

    st.title("🔍 AI Resume Analyzer")
    st.write("Upload your resume and paste the job description to get a detailed ATS analysis.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Upload Resume")
        uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
        
    with col2:
        st.subheader("2. Job Description")
        job_description = st.text_area("Paste the job description here", height=200)
        
    if st.button("Analyze Resume"):
        if uploaded_file and job_description:
            with st.spinner("Analyzing your resume with Gemini AI..."):
                try:
                    # Parse Resume
                    resume_text = parse_resume(uploaded_file)
                    
                    # LLM Analysis
                    analysis_raw = analyze_resume_llm(resume_text, job_description)
                    
                    # Try to parse JSON from LLM response (handling potential markdown blocks)
                    try:
                        clean_json = str(analysis_raw).strip()
                        # Handle common markdown and labeling patterns
                        if "```json" in clean_json:
                            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                        elif "```" in clean_json:
                            clean_json = clean_json.split("```")[1].split("```")[0].strip()
                        elif clean_json.startswith("json\n"):
                            clean_json = clean_json[5:].strip()
                        
                        # Find the outermost curly braces
                        start_idx = clean_json.find('{')
                        end_idx = clean_json.rfind('}')
                        if start_idx != -1 and end_idx != -1:
                            clean_json = clean_json[start_idx:end_idx+1]
                            
                        analysis = json.loads(clean_json)
                    except Exception as e:
                        st.error(f"Failed to parse AI response. Raw output: {analysis_raw}")
                        st.stop()

                    # Save to DB
                    db = SessionLocal()
                    new_resume = Resume(
                        user_id=st.session_state.user_id,
                        filename=uploaded_file.name,
                        parsed_text=resume_text
                    )
                    db.add(new_resume)
                    db.commit()
                    db.refresh(new_resume)
                    
                    new_report = Report(
                        user_id=st.session_state.user_id,
                        resume_id=new_resume.id,
                        ats_score=analysis.get('ats_score', 0),
                        match_score=analysis.get('match_score', 0),
                        missing_keywords=json.dumps(analysis.get('missing_keywords', [])),
                        suggestions=analysis.get('suggestions', ''),
                        job_description=job_description
                    )
                    db.add(new_report)
                    db.commit()
                    db.close()
                    
                    # Display Results
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    
                    # Metrics
                    m1, m2 = st.columns(2)
                    with m1:
                        st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1 style="color:#4F46E5;">{analysis.get("ats_score")}%</h1></div>', unsafe_allow_html=True)
                    with m2:
                        st.markdown(f'<div class="metric-card"><h3>Job Match</h3><h1 style="color:#10B981;">{analysis.get("match_score")}%</h1></div>', unsafe_allow_html=True)
                    
                    st.markdown("### 🔑 Missing Keywords")
                    keywords = analysis.get('missing_keywords', [])
                    if keywords:
                        st.write(", ".join([f"`{k}`" for k in keywords]))
                    else:
                        st.write("No major keywords missing!")
                        
                    st.markdown("### 💡 Improvement Suggestions")
                    st.info(analysis.get('suggestions'))
                    
                    st.markdown("### ✍️ Optimized Bullet Points")
                    for bullet in analysis.get('improved_bullets', []):
                        st.markdown(f"- {bullet}")
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload a resume and provide a job description.")

def render_tools():
    from utils.ai_chains import generate_cover_letter_llm, generate_interview_questions_llm, rewrite_resume_llm
    
    st.title("🛠️ AI Career Tools")
    
    tool = st.tabs(["📝 Cover Letter", "🎙️ Interview Prep", "✍️ Resume Rewrite"])
    
    with tool[0]:
        st.subheader("Generate a Professional Cover Letter")
        res_text = st.text_area("Your Resume Text (Paste or it will use last uploaded)", height=150)
        job_desc = st.text_area("Job Description for Cover Letter", height=150)
        if st.button("Generate Cover Letter"):
            if res_text and job_desc:
                with st.spinner("Generating..."):
                    letter = generate_cover_letter_llm(res_text, job_desc)
                    st.markdown("### Generated Cover Letter")
                    st.markdown(f'<div class="card">{letter}</div>', unsafe_allow_html=True)
                    st.download_button("Download as Text", letter, file_name="cover_letter.txt")
            else:
                st.warning("Please provide both resume and job description.")
                
    with tool[1]:
        st.subheader("Interview Preparation")
        res_text_q = st.text_area("Resume Text for Interview Prep", height=150)
        job_desc_q = st.text_area("Job Description for Interview Prep", height=150)
        if st.button("Generate Questions"):
            if res_text_q and job_desc_q:
                with st.spinner("Generating questions..."):
                    questions = generate_interview_questions_llm(res_text_q, job_desc_q)
                    st.markdown("### Top Interview Questions & Answers")
                    st.markdown(f'<div class="card">{questions}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please provide both resume and job description.")

    with tool[2]:
        st.subheader("Resume Section Rewriter")
        role = st.text_input("Target Role (e.g., Senior DevOps Engineer)")
        sections = st.text_area("Paste sections to improve", height=150)
        if st.button("Rewrite Sections"):
            if role and sections:
                with st.spinner("Rewriting..."):
                    improved = rewrite_resume_llm(sections, role)
                    st.markdown("### Improved Version")
                    st.markdown(f'<div class="card">{improved}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please provide both role and sections.")


def render_history():
    from database import Report, Resume
    import json
    
    st.title("🕒 Your Analysis History")
    db = SessionLocal()
    reports = db.query(Report).filter(Report.user_id == st.session_state.user_id).order_by(Report.created_at.desc()).all()
    db.close()
    
    if not reports:
        st.write("You haven't analyzed any resumes yet.")
        return
        
    for report in reports:
        with st.expander(f"Analysis on {report.created_at.strftime('%Y-%m-%d %H:%M')} | ATS Score: {report.ats_score}%"):
            st.write(f"**ATS Score:** {report.ats_score}%")
            st.write(f"**Match Score:** {report.match_score}%")
            st.write("**Missing Keywords:**")
            try:
                kw = json.loads(report.missing_keywords)
                st.write(", ".join(kw))
            except:
                st.write(report.missing_keywords)
            st.write("**Suggestions:**")
            st.write(report.suggestions)
            st.markdown("---")
            st.write("**Job Description Excerpt:**")
            st.write(report.job_description[:300] + "...")

if __name__ == "__main__":
    main()
