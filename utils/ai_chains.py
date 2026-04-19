import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

# Initialize Gemini - Using gemini-3-flash-preview as it is available in this environment
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

class ATSAnalysis(BaseModel):
    ats_score: float = Field(description="ATS compatibility score from 0 to 100")
    match_score: float = Field(description="Match percentage with job description from 0 to 100")
    missing_keywords: List[str] = Field(description="List of important keywords missing from the resume")
    suggestions: str = Field(description="Detailed suggestions for improvement")
    improved_bullets: List[str] = Field(description="List of professionally rewritten bullet points")

# Chain 1: ATS Analyzer
def analyze_resume_llm(resume_text, job_description):
    prompt_template = """
    You are an expert ATS (Applicant Tracking System) optimizer and career coach. 
    Analyze the provided resume against the job description.
    
    Resume Text: {resume_text}
    Job Description: {job_description}
    
    Provide a detailed analysis including:
    1. ATS Score (0-100)
    2. Match Score (0-100)
    3. Missing Keywords
    4. Actionable Suggestions
    5. Professionally rewritten bullet points for weak sections.
    
    Format the output as a clean JSON object.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    response = chain.invoke({"resume_text": resume_text, "job_description": job_description})
    if isinstance(response.content, list):
        return "".join([part.get('text', '') if isinstance(part, dict) else str(part) for part in response.content])
    return str(response.content)


# Chain 2: Resume Rewrite
def rewrite_resume_llm(resume_text, target_role):
    prompt_template = """
    You are a professional resume writer. Rewrite the following resume sections to make them more impactful, 
    using strong action verbs and quantifying achievements where possible. 
    Target Role: {target_role}
    
    Resume Sections: {resume_text}
    
    Provide the improved version.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    response = chain.invoke({"target_role": target_role, "resume_text": resume_text})
    
    if isinstance(response.content, list):
        return "".join([part.get('text', '') if isinstance(part, dict) else str(part) for part in response.content])
    return str(response.content)

# Chain 3: Cover Letter
def generate_cover_letter_llm(resume_text, job_description):
    prompt_template = """
    Write a professional and compelling cover letter based on the following resume and job description.
    
    Resume: {resume_text}
    Job Description: {job_description}
    
    The letter should be concise, highlight relevant skills, and show enthusiasm for the role.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    response = chain.invoke({"resume_text": resume_text, "job_description": job_description})
    if isinstance(response.content, list):
        return "".join([part.get('text', '') if isinstance(part, dict) else str(part) for part in response.content])
    return str(response.content)


# Chain 4: Interview Questions
def generate_interview_questions_llm(resume_text, job_description):
    prompt_template = """
    Generate 10 relevant interview questions (both technical and behavioral) based on the resume and job description.
    Provide brief sample answers or talking points for each.
    
    Resume: {resume_text}
    Job Description: {job_description}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    response = chain.invoke({"resume_text": resume_text, "job_description": job_description})
    if isinstance(response.content, list):
        return "".join([part.get('text', '') if isinstance(part, dict) else str(part) for part in response.content])
    return str(response.content)


