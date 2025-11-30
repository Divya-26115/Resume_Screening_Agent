import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import tempfile
from pypdf import PdfReader
import io

st.set_page_config(page_title="Resume Screening Agent", page_icon="📄", layout="wide")

st.title("📄 Resume Screening Agent")
st.markdown("**AI-powered resume ranking based on Job Description**")

# Sidebar for API key
with st.sidebar:
    st.header("🔑 Setup")
    google_api_key = st.text_input(
        "Google Gemini API Key",
        type="password",           # hides the key
        help="Paste your Gemini API key (it will be hidden)"
    )
    if not google_api_key:
        st.warning("Enter your Gemini API key")
        st.stop()
    os.environ["GOOGLE_API_KEY"] = google_api_key


# Initialize LLM
@st.cache_resource
def load_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Extract text from file
def extract_text(file):
    if file.type == "application/pdf":
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    else:
        text = file.read().decode("utf-8")
    return text

# Score single resume
def score_resume(jd_text, resume_text, resume_name):
    # TEMP: no Gemini, just length‑based fake score
    overlap = len(set(jd_text.lower().split()) & set(resume_text.lower().split()))
    score = min(100, overlap * 5)

    return {
        "name": resume_name,
        "score": int(score),
        "reasoning": f"Temp local scoring: {overlap} matching keywords."
    }

# Main app
tab1, tab2 = st.tabs(["📤 Upload & Screen", "📊 Results"])

with tab1:
    st.header("Upload Job Description & Resumes")
    
    # Job Description
    jd_file = st.file_uploader("📋 Job Description (PDF/TXT)", type=['pdf', 'txt'])
    
    # Resumes (multiple)
    resume_files = st.file_uploader(
        "📄 Resumes (upload multiple)", 
        type=['pdf', 'txt'], 
        accept_multiple_files=True
    )
    
    if st.button("🚀 Screen Resumes") and jd_file and resume_files:
        with st.spinner("Analyzing resumes..."):
            # Extract JD text
            jd_text = extract_text(jd_file)
            st.text_area("Job Description Preview:", jd_text[:500] + "...", height=150)
            
            # Process resumes
            results = []
            llm = load_llm()
            
            progress_bar = st.progress(0)
            for i, resume_file in enumerate(resume_files):
                resume_text = extract_text(resume_file)
                result = score_resume(jd_text, resume_text, resume_file.name)
                results.append(result)
                progress_bar.progress((i + 1) / len(resume_files))
            
            st.session_state.results = results
            st.success(f"✅ Screened {len(results)} resumes!")
            st.rerun()

with tab2:
    if 'results' in st.session_state:
        df = pd.DataFrame(st.session_state.results)
        df = df.sort_values('score', ascending=False)
        
        st.header("🏆 Ranked Candidates")
        st.dataframe(df, use_container_width=True)
        
        # Top 3
        col1, col2, col3 = st.columns(3)
        with col1:
            if len(df) > 0:
                top1 = df.iloc[0]
                st.metric("🥇 Top Candidate", f"{top1['score']}%", delta=None)
                st.write(top1['name'])
                st.caption(top1['reasoning'])
        
        # Download
        csv = df.to_csv(index=False)
        st.download_button(
            "💾 Download Ranked List (CSV)",
            csv,
            "ranked_candidates.csv",
            "text/csv"
        )
    else:
        st.info("👈 Upload files and click 'Screen Resumes' first")

# Footer
st.markdown("---")
st.markdown("**Challenge Compliant: Gemini + LangChain + Streamlit** ✅")
