import asyncio
import sys

# 1. Fix for Windows Python 3.11+ Asyncio Event Loop Bug
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
from PIL import Image
import os
import base64
from dotenv import load_dotenv

# Core LangChain imports (Swapped out Chroma for FAISS to ensure cloud compatibility)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 2. Configure the page settings (ONLY CALL THIS ONCE AT THE TOP)
if os.path.exists("logo.png"):
    browser_tab_logo = Image.open("logo.png")
else:
    browser_tab_logo = "⚡"

st.set_page_config(
    page_title="SafeX AI Support", 
    page_icon=browser_tab_logo, 
    layout="centered"
)

# Helper function to load logo image safely
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return "https://img.icons8.com/fluency/48/shield.png"

logo_base64 = get_base64_image("logo.png")
load_dotenv()

# --- PREMIUM SAAS LIVE CHAT PLATFORM DESIGN ---
st.markdown("""
    <style>
    /* 1. Global Reset & Full Bleed Layout Setup */
    [data-testid="stAppViewContainer"] {
        padding: 0px !important;
        background-color: #F8FAFC !important;
    }
    [data-testid="stHeader"] { 
        visibility: hidden; 
        height: 0px !important; 
    }
    footer { 
        visibility: hidden; 
    }
    
    /* 2. Sleek Smartphone Frame Mockup */
    .stApp { 
        max-width: 450px; 
        margin: 20px auto !important; 
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        min-height: 85vh;
        padding: 0px !important;
        background-color: #FFFFFF;
        box-shadow: 0px 20px 40px rgba(15, 23, 42, 0.08);
        overflow-x: hidden;
    }

    /* 3. High-End FIXED Tech Corporate Header (Locks at the Top) */
    .chat-header-saas {
        position: fixed;
        top: 3px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 450px;
        background: #27374D;
        padding: 25px;
        color: #FFFFFF;
        margin: 0px !important;
        z-index: 99999;
        border-top-left-radius: 22px;
        border-top-right-radius: 22px;
        border-bottom: 1px solid #334155;
        box-sizing: border-box;
    }
    
    .header-flex {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .company-title-block h2 { 
        margin: 0 !important; 
        font-size: 17px !important; 
        font-weight: 700 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', system-ui, sans-serif;
    }
    .company-logo-badge {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background-color: transparent; 
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden; 
    }
    
    .company-logo-badge img {
        width: 100%;
        height: 100%;
        object-fit: contain; 
    }
    .live-pulse-container {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 2px;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-ring 1.5s infinite;
    }
    
    @keyframes pulse-ring {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    .status-text {
        font-size: 11px;
        color: #94A3B8;
        font-weight: 500;
    }
    
    .tech-tag {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        color: #3B82F6;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* 4. Chat Feed Body */
    .block-container { 
        padding: 0px !important; 
    }
    
    .chat-body-container {
        padding: 75px 20px 10px 20px !important;
        background-color: #FFFFFF;
    }
    
    /* 5. Custom Message Bubble Enhancements */
    div[data-testid="stChatMessage"] {
        background-color: #F1F5F9 !important;
        border-radius: 16px !important;
        padding: 12px 16px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 12px;
    }
    
    /* Elegant Right-side Swapping for User Bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatavatardefault-user"]) {
        flex-direction: row-reverse !important;
        text-align: right !important;
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        border: none !important;
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="chatavatardefault-user"]) p {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- MODERN BACKGROUND DATA RETRIEVAL ---
@st.cache_resource
def setup_rag():
    if not os.path.exists("knowledge_base.txt"):
        return None
    
    try:
        # 1. Read the text file safely
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            raw_text = f.read()
        
        # 2. Production-grade chunking (Breaks data cleanly without losing meaning)
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,       # Targets single paragraphs/topics
            chunk_overlap=100,    # Ensures facts aren't cut mid-sentence
            separators=["\n\n", "\n", ".", " "]
        )
        
        # 3. Create searchable documents
        texts = text_splitter.split_text(raw_text)
        docs = [Document(page_content=t) for t in texts]
        
        if not docs:
            return None

        # 4. Process and index your knowledge base
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(docs, embeddings)
        
        # Pull the top 3 most relevant segments for every question
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})
        
        # 5. Initialize the high-end inference model
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
        
        # 6. Ultra-Strict System Prompt
        template = """You are the official corporate AI support agent for SafeX Solutions.
        
        Your ONLY job is to answer the user's question using the verified corporate context provided below.
        
        RULES:
        1. Base your answer completely on the Corporate Context. If the context mentions specific services, list them clearly with professional detail.
        2. Do NOT summarize into vague one-sentence fluff answers (e.g., do NOT just say "We offer services"). Be thorough and helpful.
        3. If the user asks a question that is completely missing from the Corporate Context below, reply exactly with: "I'm sorry, but that details is out of scope regarding our verified services framework."
        4. Never say 'according to the text' or 'in the provided context'. Act like a real human corporate agent.
        
        Corporate Context:
        {context}
        
        Customer Inquiry: {question}
        Support Reply:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        return ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
    except Exception as e:
        print(f"RAG Initialization Error: {e}")
        return None

rag_chain = setup_rag()

# --- HIGH-END PINNED TECH CORPORATE HEADER DISPLAY ---
st.markdown(f"""
    <div class="chat-header-saas">
        <div class="header-flex">
            <div class="header-left">
                <div class="company-logo-badge">
                    <img src="{logo_base64}" alt="SafeX Solutions Logo">
                </div>
                <div class="company-title-block">
                    <h2>SafeX Solutions</h2>
                    <div class="live-pulse-container">
                        <div class="pulse-dot"></div>
                        <span class="status-text">AI Support Agent</span>
                    </div>
                </div>
            </div>
            <div class="tech-tag">LIVE CHAT</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Container wrapping the scrollable chat feed elements
st.markdown('<div class="chat-body-container">', unsafe_allow_html=True)

# Initialize message logs safely
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Welcome to SafeX Chat Live. How can I assist you with our tech and cybersecurity services today?"}]

# Render current history stack
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User action processing loop
if user_prompt := st.chat_input("Message SafeX Solutions..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            if rag_chain:
                try:
                    response = rag_chain.invoke(user_prompt)
                    st.markdown(response)
                except Exception as e:
                    response = "I am currently experiencing a brief connectivity glitch. Please try your question again in a moment."
                    st.markdown(response)
            else:
                response = "SafeX live support channels are undergoing minor system maintenance. Please check back shortly."
                st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('</div>', unsafe_allow_html=True)