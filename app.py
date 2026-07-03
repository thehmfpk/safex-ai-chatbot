import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = FastAPI()

# Mount the folder holding logo.png so the frontend can read it safely
app.mount("/static", StaticFiles(directory="."), name="static")

# ================= BACKEND ENGINE INITIALIZATION =================
retriever = None
rag_chain = None

def initialize_rag_system():
    global retriever, rag_chain
    if not os.path.exists("knowledge_base.txt"):
        return False
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            raw_text = f.read()
        paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
        docs = [Document(page_content=t) for t in paragraphs]
        
        embeddings = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=os.getenv("HF_TOKEN")
        )
        vector_db = InMemoryVectorStore.from_documents(docs, embeddings)
        retriever = vector_db.as_retriever(search_kwargs={"k": 2})
        
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
        template = """You are the official corporate AI support agent for SafeX Solutions.
Corporate Context: {context}
Customer Inquiry: {question}
Support Reply:"""
        prompt = ChatPromptTemplate.from_template(template)
        rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
        return True
    except Exception as e:
        print(f"Engine connection fallback active: {e}")
        return False

initialize_rag_system()

# ================= API ENDPOINT FOR MESSAGES =================
@app.post("/api/chat")
async def chat_endpoint(request: Request):
    global rag_chain
    data = await request.json()
    user_message = data.get("message", "")
    
    if not rag_chain:
        if not initialize_rag_system():
            return {"reply": "⚠️ System maintenance window active. Please check network connections."}
            
    try:
        bot_response = rag_chain.invoke(user_message)
    except Exception as e:
        bot_response = f"Connection error: {str(e)}"
        
    return {"reply": bot_response}

# ================= BEAUTIFIED FRONTEND SERVING =================
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="/static/logo.png" type="image/png">
        <title>SafeX Solutions Agent</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body, html { height: 100vh; width: 100vw; background: #27374D; display: flex; justify-content: center; align-items: center; overflow: hidden; }
            
            /* Responsive Phone Frame Shell */
            .app-container {
                width: 100%;
                max-width: 420px;
                height: 95vh;
                background: #DDE6ED;
                border-radius: 32px;
                box-shadow: 0 25px 60px rgba(0,0,0,0.5);
                position: relative;
                overflow: hidden;
                border: 1px solid rgba(255,255,255,0.15);
            }

            /* Keep your original .app-container code exactly as it is, then add this below it */

@media (max-width: 480px) {
    body, html {
        align-items: flex-start; /* Forces the app container to align to the top instead of center */
        padding-top: 5px;        /* This creates that exact "little gap from above" on a phone */
        height: 95vh;
    }

    .app-container {
        height: calc(95vh - 5px); /* Stretches the frame to perfectly sit right above the bottom nav bar */
        border-radius: 24px 24px 24px 24px; /* Optional: keeps nice rounded corners on top, flat on bottom */
        padding-bottom: 20px;
    }
}

            /* Screen Master Layout Toggle States */
            .screen { width: 100%; height: 100%; display: flex; flex-direction: column; position: absolute; top: 0; left: 0; transition: transform 0.4s ease-in-out; }
            #splash-screen { background: radial-gradient(circle at top, #526D82, #27374D); justify-content: center; align-items: center; padding: 40px; text-align: center; z-index: 2; }
            #chat-screen { transform: translateX(100%); z-index: 1; background: #DDE6ED; }
            
            /* Active transition override */
            .app-container.active-chat #splash-screen { transform: translateX(-100%); }
            .app-container.active-chat #chat-screen { transform: translateX(0); }

            /* Splash View Components Layout */
            .splash-logo { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #9DB2BF; margin-bottom: 24px; object-fit: cover; }
            .splash-title { color: #DDE6ED; font-size: 2rem; font-weight: 700; margin-bottom: 10px; }
            .splash-subtitle { color: #9DB2BF; font-size: 1rem; margin-bottom: 40px; }
            .btn-start { background: #9DB2BF; color: #27374D; font-weight: 700; font-size: 1.1rem; border: none; padding: 16px 44px; border-radius: 30px; cursor: pointer; transition: 0.2s; box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
            .btn-start:hover { transform: translateY(-2px); background: #DDE6ED; }

            /* Chat Brand-Header Component Layout */
            .brand-header { background: #27374D; padding: 16px 20px; display: flex; align-items: center; border-bottom: 2px solid #526D82; gap: 14px; }
            .header-logo { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 1px solid #9DB2BF; }
            .header-info h1 { color: #DDE6ED; font-size: 1.2rem; font-weight: 700; }
            .header-info p { color: #9DB2BF; font-size: 0.8rem; margin-top: 2px; }

            /* Dynamic Interior Scroll Message Board Layout */
            .message-board { flex-grow: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 16px; scroll-behavior: smooth; }
            .message-row { display: flex; align-items: flex-end; gap: 10px; max-width: 85%; }
            .message-row.user-row { align-self: flex-end; flex-direction: row-reverse; }
            .message-row.bot-row { align-self: flex-start; }
            
            .msg-avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 1px solid #9DB2BF; }
            .bubble { padding: 12px 16px; font-size: 0.95rem; line-height: 1.4; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            
            .user-row .bubble { background: #9DB2BF; color: #27374D; border-radius: 18px 18px 2px 18px; }
            .bot-row .bubble { background: #526D82; color: #DDE6ED; border-radius: 18px 18px 18px 2px; }

            /* Dynamic Actions Dock UI */
            .actions-dock { background: #ffffff; padding: 14px 18px; border-top: 1px solid rgba(0,0,0,0.06); display: flex; align-items: center; gap: 12px; }
            .text-box { flex-grow: 1; background: #F3F4F6; border: 1px solid #9DB2BF; padding: 12px 18px; border-radius: 24px; font-size: 0.95rem; color: #27374D; outline: none; }
            .send-btn { background: #27374D; color: #DDE6ED; border: none; width: 44px; height: 44px; border-radius: 50%; cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 1.1rem; font-weight: bold; transition: 0.2s; }
            .send-btn:hover { background: #526D82; }
        </style>
    </head>
    <body>

        <div class="app-container" id="shell">
            
            <div class="screen" id="splash-screen">
                <img src="/static/logo.png" class="splash-logo" onerror="this.src='https://placehold.co/120?text=SafeX'">
                <h1 class="splash-title">SafeX Solutions</h1>
                <p class="splash-subtitle">Need our help now?</p>
                <button class="btn-start" onclick="enterChatboard()">Get Started &gt;&gt;&gt;</button>
            </div>

            <div class="screen" id="chat-screen">
                <div class="brand-header">
                    <img src="/static/logo.png" class="header-logo" onerror="this.src='https://placehold.co/44?text=SX'">
                    <div class="header-info">
                        <h1>SafeX Solutions</h1>
                        <p>● Live — Support Agent</p>
                    </div>
                </div>

                <div class="message-board" id="chat-board">
                    <div class="message-row bot-row">
                        <img src="/static/logo.png" class="msg-avatar" onerror="this.src='https://placehold.co/32?text=SX'">
                        <div class="bubble">Hello! Welcome to SafeX Solutions. How can I assist you with our services today?</div>
                    </div>
                </div>

                <div class="actions-dock">
                    <input type="text" id="user-input" class="text-box" placeholder="Type your message here..." onkeydown="handleKey(event)">
                    <button class="send-btn" onclick="sendMessage()">➔</button>
                </div>
            </div>

        </div>

        <script>
            function enterChatboard() {
                document.getElementById('shell').classList.add('active-chat');
            }

            function handleKey(e) {
                if (e.key === 'Enter') sendMessage();
            }

            async function sendMessage() {
                const input = document.getElementById('user-input');
                const text = input.value.trim();
                if (!text) return;

                input.value = '';
                const board = document.getElementById('chat-board');

                // 1. Inject User Bubble
                board.innerHTML += `
                    <div class="message-row user-row">
                        <div class="bubble">${text}</div>
                    </div>
                `;
                board.scrollTop = board.scrollHeight;

                // 2. Fetch API Output
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: text })
                    });
                    const data = await response.json();

                    // 3. Inject Assistant Bubble with Logo icon
                    board.innerHTML += `
                        <div class="message-row bot-row">
                            <img src="/static/logo.png" class="msg-avatar" onerror="this.src='https://placehold.co/32?text=SX'">
                            <div class="bubble">${data.reply}</div>
                        </div>
                    `;
                } catch (err) {
                    board.innerHTML += `
                        <div class="message-row bot-row">
                            <div class="bubble" style="background:#ef4444;">Connection failed to access support API stream.</div>
                        </div>
                    `;
                }
                board.scrollTop = board.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return html_content


import os

if __name__ == "__main__":
    import uvicorn
    # Read the port Hugging Face assigns, fallback to 7860 if empty
    port = int(os.environ.get("PORT", 7860)) 
    uvicorn.run("app:app", host="0.0.0.0", port=port)
