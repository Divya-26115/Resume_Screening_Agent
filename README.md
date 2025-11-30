Resume Screening Agent
This project is an AI agent that ranks multiple resumes against a given Job Description for the AI Agent Development Challenge.

✨ Features
Upload a Job Description (PDF or TXT)

Upload multiple candidate resumes (PDF or TXT)

For each resume, the agent:

Generates a match score (0–100%)

Provides a one-line reasoning

Displays a ranked table of candidates

Allows CSV download of the ranked list

🛠 Tech Stack
Language: Python

AI Model: Google Gemini (via Gemini API)

Framework: LangChain

UI: Streamlit

Libraries: pandas, pypdf, langchain-google-genai, google-generativeai

▶️ How to Run the Project
Clone the repository (or just open this folder if you already have it).

Install dependencies in a terminal opened in this folder:

pip install -r requirements.txt

Get a Google Gemini API key from:

https://makersuite.google.com/app/apikey

Start the Streamlit app:

streamlit run app.py

In the browser:

Open the URL from the terminal (usually http://localhost:8501).

Paste your Gemini API key in the sidebar.

Upload a Job Description file.

Upload multiple resume files.

Click the button to screen resumes.