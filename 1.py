import os
import chromadb
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="🔆 Solar AI Assistant",
    page_icon="☀️",
    layout="wide"
)

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🚨 GOOGLE_API_KEY is missing! Add it to the `.env` file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

DB_PATH = "solar_vector_db"
chroma_client = chromadb.PersistentClient(path=DB_PATH)

collection_name = "langchain"  
try:
    collection = chroma_client.get_collection(collection_name)
    st.info(f"✅ Connected to ChromaDB Collection: `{collection_name}`")
except Exception as e:
    st.error(f"🚨 Error: ChromaDB collection `{collection_name}` not found. Please run the embedding script again.")
    st.stop()

embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")  

def get_relevant_docs(query, top_k=3):
    """Fetch top_k most relevant document chunks."""
    query_embedding = embedding_model.encode([query])[0]  
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    retrieved_texts = results["documents"][0] if results["documents"] else []
    return "\n\n".join(retrieved_texts) if retrieved_texts else "No relevant data found."

st.markdown("""
<style>
    .main { padding: 0 !important; margin: 0 !important; }
    .header { padding: 1.5rem 2rem; background-color: white; border-bottom: 1px solid #eee; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }
    .header-title { font-size: 2.5rem !important; font-weight: 600; display: flex; align-items: center; gap: 0.75rem; }
    .welcome-container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: calc(100vh - 200px); text-align: center; }
    .welcome-icon { font-size: 4rem; margin-bottom: 1rem; }
    .welcome-text { font-size: 1.5rem; color: #64748b; font-weight: 500; }
    .chat-container { margin: 100px 0 100px 0; padding: 0 2rem; overflow-y: auto; max-width: 1200px; margin-left: auto; margin-right: auto; min-height: calc(100vh - 200px); }
    .chat-message { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; max-width: 80%; }
    .user-message { background-color: #f8fafc; color: #334155; margin-left: auto; border: 1px solid #e2e8f0; }
    .assistant-message { background-color: #f8fafc; color: #334155; margin-right: auto; border: 1px solid #e2e8f0; }
    .input-container { position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 1.5rem 2rem; border-top: 1px solid #eee; z-index: 1000; }
    .input-container .element-container { max-width: 1200px; margin: 0 auto; }
    .stTextInput > div > div { padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #e2e8f0; background-color: white; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
    <div class="header">
        <div class="header-title">
            <span>🔆</span> Solar Panel AI Assistant
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-icon">🤖</div>
            <div class="welcome-text">
                Hello! I'm your AI assistant.<br>
                Ask me anything about solar panels, installation, cost, and trends!
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        reference = message.get("reference", "")
        
        style_class = "assistant-message" if role == "assistant" else "user-message"
        
        st.markdown(f"""
            <div class="chat-message {style_class}">
                {content}
                {f'<div class="reference-data"><strong>Reference Data:</strong><br>{reference}</div>' if reference else ''}
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Ask anything about solar panels, installation, cost, and trends!",
            label_visibility="collapsed"
        )
    with col2:
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("Retrieving relevant data..."):
            reference_text = get_relevant_docs(user_input)

            prompt = f"""You are SolarGuide, an expert AI consultant specializing in solar energy with deep industry expertise. Your goal is to provide accurate, practical, and user-friendly responses while maintaining professionalism.

                RULES FOR RESPONSES:
            - Balance technical accuracy with clear explanations
            - Cite specific data points from provided documents when available
            - Include practical recommendations
            - Consider both residential and commercial perspectives
            - Account for current market trends and technology
            - Be direct and actionable in your advice

            USE THIS STRUCTURE:
            1. Direct answer to the query
            2. Supporting evidence from internal documents
            3. Additional relevant context
            4. Practical recommendations
            5. Optional: Related information if relevant

            KNOWLEDGE BASE:
            - Primary Source (60%): Use the provided internal documentation
            - Secondary Source (40%): Draw from industry standards and best practices

            **Reference Data (from internal documents):**
            {reference_text}

            **User Query:** {user_input}

            Provide a clear, structured response that directly addresses the user's needs while incorporating relevant information from both sources."""

            try:
                response = model.generate_content(prompt)
                ai_response = response.text if response else "Error: No response from Gemini AI."

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_response,
                    "reference": reference_text
                })

                st.rerun()
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)
