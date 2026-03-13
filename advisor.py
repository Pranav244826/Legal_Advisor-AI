import streamlit as st
from groq import Groq

# 1. Configuration - Use Streamlit Secrets for the API Key
# For local development, create a file at .streamlit/secrets.toml with:
# GROQ_API_KEY = "your_key_here"
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "PASTE_YOUR_KEY_HERE_IF_NOT_USING_SECRETS"

client = Groq(api_key=api_key)

# 2. UI Setup
st.set_page_config(
    page_title="LegalAI", 
    page_icon="⚖️",
    layout="wide", # Wider layout for better readability
    initial_sidebar_state="expanded"
)

# Sidebar layout
with st.sidebar:
    st.title("⚖️ LegalAI Settings")
    st.markdown("---")
    
    # Simple control to clear history
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    
    # Theme Settings
    st.subheader("🎨 Appearance")
    theme = st.selectbox("Choose Theme", ["Default", "Light Mode", "Dark Mode", "Crimson & Gold"])
    if theme == "Light Mode":
        st.markdown("<style>.stApp { background-color: #FFFFFF; color: #31333F; } .stTextInput input, .stSelectbox select { color: #31333F; background-color: #F0F2F6; border: 1px solid #CCC; }</style>", unsafe_allow_html=True)
    elif theme == "Dark Mode":
        st.markdown("<style>.stApp { background-color: #0E1117; color: #FAFAFA; } .stTextInput input, .stSelectbox select { color: #FAFAFA; background-color: #262730; border: 1px solid #444; }</style>", unsafe_allow_html=True)
    elif theme == "Crimson & Gold":
         st.markdown("""
            <style>
            /* Main background & Default Text */
            .stApp { background-color: #2C0F14; color: #F1DEC0 !important; } 
            div[data-testid="stMarkdownContainer"] { color: #F1DEC0 !important; }
            
            /* Input Fields & Dropdowns */
            .stTextInput input, .stSelectbox select, [data-baseweb="base-input"], div[data-baseweb="input"] { 
                color: #F1DEC0 !important; 
                background-color: #4A1A24 !important; 
                border-color: #D4AF37 !important; 
                -webkit-text-fill-color: #F1DEC0 !important; /* Forces text color on inputs */
                caret-color: #D4AF37 !important; /* Makes the typing cursor bright gold! */
            } 
            
            /* Chat Interface Elements */
            [data-testid="chat-message"] { background-color: #381219; border: 1px solid #4A1A24; border-radius: 8px; padding: 10px; }
            div[data-testid="stChatInput"] { background-color: #4A1A24; border: 1px solid #D4AF37; }
            div[data-testid="stChatInput"] textarea { color: #F1DEC0 !important; caret-color: #D4AF37 !important; }
            
            /* Headers & Typography */
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #D4AF37 !important; } 
            
            /* Buttons */
            .stButton button { border-color: #D4AF37 !important; color: #D4AF37 !important; background-color: transparent !important; transition: 0.2s;} 
            .stButton button:hover { background-color: rgba(212, 175, 55, 0.1) !important; color: #F9E596 !important; border-color: #F9E596 !important;}
            </style>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 5. Document Upload Feature (Moved to Sidebar)
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader("Contract, Lease, or Notice (PDF)", type=["pdf"])

    if uploaded_file is not None:
        if "document_parsed" not in st.session_state or st.session_state.document_name != uploaded_file.name:
            with st.spinner("Parsing document..."):
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                st.session_state.document_text = text
                st.session_state.document_name = uploaded_file.name
                st.session_state.document_parsed = True
                st.success(f"Successfully loaded '{uploaded_file.name}'!")
        else:
             st.success(f"Document '{uploaded_file.name}' is loaded and ready.")
        
        # Show a snippet of the document
        with st.expander("View Document Snippet"):
            st.text(st.session_state.document_text[:500] + "...\n[Document truncated for display]")

    st.markdown("---")

    # Disclaimer in Sidebar
    st.info("""
    **Disclaimer:** This is an AI research assistant. 
    It is not a substitute for a human lawyer. It may provide 
    incorrect or outdated information. Please verify with a 
    legal professional.
    """, icon="⚠️")
    
    st.markdown("---")
    st.caption("Final Year Internship Project")


st.title("⚖️ AI Legal Research Assistant")
st.caption("Indian Law (IPC/CrPC) Expert")

# 3. Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Example Prompt Chips (Only show if chat is empty)
if not st.session_state.messages:
    st.markdown("### 💡 Example Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What are the rights of a tenant?", use_container_width=True):
            st.session_state.example_prompt = "What are the rights of a tenant?"
            st.rerun()
    with col2:
        if st.button("Explain Section 420 IPC briefly", use_container_width=True):
            st.session_state.example_prompt = "Explain Section 420 IPC briefly"
            st.rerun()
    with col3:
        if st.button("What happens if someone is arrested?", use_container_width=True):
             st.session_state.example_prompt = "What happens if someone is arrested?"
             st.rerun()


# 6. Chat Input Logic (Handles both typed input and example prompts)
prompt = st.chat_input("Ask a legal question (e.g., What are the rights of a tenant?)")

# Check if an example prompt was clicked
if "example_prompt" in st.session_state:
    prompt = st.session_state.example_prompt
    del st.session_state.example_prompt # Clean up so it doesn't trigger again

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response with Spinner and Streaming
    with st.chat_message("assistant"):
        with st.spinner("Analyzing Indian Law databases..."):
            
            # Prepare messages payload
            messages_payload = [
                  {"role": "system", "content": "You are a professional Legal Research Assistant specializing in Indian Law. Provide clear, factual explanations citing relevant IPC, BNS, or CrPC sections. Format your response clearly using markdown headings and bullet points."}
            ]
            
            # Add document context if it exists
            if "document_parsed" in st.session_state and st.session_state.document_parsed:
                 messages_payload.append({
                     "role": "system", 
                     "content": f"The user has uploaded a document named '{st.session_state.document_name}'. Here is its content to answer questions against:\n\n{st.session_state.document_text}"
                 })
            
            # Append history (you might want to limit this for context window reasons in a real app)
            for msg in st.session_state.messages[:-1]: # exclude the latest prompt we just appended
                 messages_payload.append(msg)
            
            # Append latest prompt
            messages_payload.append({"role": "user", "content": prompt})
            
            try:
                # Call Groq API with stream=True
                response_stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", # High-performance model
                    messages=messages_payload,
                    stream=True # ✨ Streaming enabled! ✨
                )
                
                # Function to yield chunks for Streamlit's write_stream
                def generate_chunks():
                    for chunk in response_stream:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
                
                # Write stream to UI
                answer = st.write_stream(generate_chunks())
                
                # Append final answer to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error("Error communicating with the AI API.")
                st.error(f"Details: {e}")
                st.info("Your Groq API key might be invalid, or your network is blocking the request. Please check your API key and network settings.")
                st.stop()