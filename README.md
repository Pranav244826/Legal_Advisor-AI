# ⚖️ Legal_Advisor-AI

An AI-powered Legal Research Assistant designed for Indian Law (IPC/CrPC). Built for a Final Year Internship Project. 

## Features
- **Conversational UI**: Ask questions in plain English and get responses citing relevant Sections.
- **Document Analysis**: Upload a `.pdf` of any legal contract, lease, or notice, and the AI will answer questions specifically based on the contents!
- **Streaming Responses**: Real-time typing effects for a premium ChatGPT-like feel.
- **Customizable Aesthetics**: Switch between Light Mode, Dark Mode, and a custom *Crimson & Gold* law theme.

## Tech Stack
- Frontend: `Streamlit`
- Backend API: `Groq`  (Llama-3.3-70b-versatile)
- Parsing: `PyPDF2`

## How to run locally
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit server:
   ```bash
   python -m streamlit run advisor.py
   ```
