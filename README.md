# SafeX Chat Live — Premium Corporate AI Support Agent

<div align="center">

---

---

## What is SafeX Chat Live About?

**SafeX Chat Live** is an enterprise-grade AI customer support application custom-tailored for a modern technology and cybersecurity firm. Instead of acting like a generic AI that gives robotic, copy-pasted responses, this chatbot is engineered to act as a highly specialized, human-like corporate agent.

It provides instant, accurate, and secure information about the company's technical services, internal operations, and customer policies directly to web visitors. It blends a high-end, premium SaaS software aesthetic with advanced engineering to ensure customers receive context-backed answers in real time without any operational downtime.

---

## How the Work Flow and Technology Works

The backend of this application is powered by a high-performance **Retrieval-Augmented Generation (RAG)** pipeline. Here is the step-by-step process of how the system handles a user's question from start to finish:

### 1. Data Ingestion & Semantic Chunking

* The company's raw corporate knowledge data (`knowledge_base.txt`) is read directly into memory.
* The system breaks down large paragraphs of text into precise, manageable text blocks. This ensures that the AI can look up hyper-specific sentences instead of guessing based on full, unorganized documents.

### 2. High-Fidelity Vector Embedding

* Every single text block is passed through a deep-learning embedding model (`all-MiniLM-L6-v2`).
* This model translates raw English words into complex mathematical vectors (coordinates). This allows the application to understand the true *meaning* and *intent* behind sentences rather than just performing simple keyword matching.

### 3. Localized Database Storage (Chroma DB)

* These mathematical coordinates are indexed and securely saved inside a localized **Chroma Vector Database**.
* When a user submits an inquiry, the app instantly searches this database, finds the top two text chunks that best match the query's meaning, and extracts them instantly.

### 4. Context-Insulated AI Inference (Llama 3.3 via Groq)

* The user's question, along with the two matched text pieces from your database, are bundled together and passed to the ultra-fast **Llama 3.3 70B** model.
* The model is bounded by strict corporate guardrails. It is forbidden from hallucinating or mentioning technical system backends (such as *"according to the database file"*). It synthesizes the data cleanly, outputting a polished, natural support response.

### 5. Seamless UI/UX Injection Layer

* The response is loaded dynamically into a custom mobile-first live-chat container.
* By using advanced, deep-target CSS overrides, the branding header remains fixed firmly to the top while messages scroll smoothly underneath it. Local image paths are converted via secure **Base64 binary string encoding** so that assets load flawlessly across any public server infrastructure globally.

---

## Tech Stack Architecture

* **Frontend Interface:** Streamlit (Enhanced with injected full-bleed CSS layout overrides)
* **Orchestration Framework:** LangChain Core & Advanced Runnables
* **Inference Engine:** Cloud Systems API (`llama-3.3-70b-versatile`)
* **Embedding Engine:** HuggingFace Hub (`all-MiniLM-L6-v2`)
* **Vector Database Store:** Chroma DB (High-performance localized text indexing)

---

## Core Features & UI Engineering

* **Fixed SaaS Navigation Header:** The dark slate-blue branding banner remains permanently locked at the top of the interface frame (`position: fixed`). Chat bubbles glide cleanly behind it with optimized, fluid scrolling dynamics.
* **Zero-Bleed Edge Layout:** Native Streamlit core margins (`stMainBlockContainer` and `stVerticalBlock`) were completely re-engineered to sit at `0px`, bringing the main branding blocks completely flush to the widget frame margins.
* **Secure Image Encoding:** Bypasses local network assets parsing sandboxes by handling brand graphics via dynamic python-based **Base64 binary string converters**.
* **Corporate Security Guardrails:** The context injection prompt forces complete corporate alignment—blocking the model from mentioning backend structures (e.g., "based on the documents/database provided") and keeping interactions human-centric.
* **Silent Error Recovery:** Replaces default system API tracebacks or scary console `st.error()` blocks with clean, client-facing fallback responses if network timeouts occur.

---

## Step-by-Step Installation & Local Execution

### 1. Clone the Workspace Repository

```bash
git clone [https://github.com/thehmfpk/safex-ai-chat.git](https://github.com/thehmfpk/safex-ai-chat.git)
cd safex-ai-chat
```

## 2. Configure Your Isolated Python Environment

```Bash
python -m venv .venv
# On Windows activation:
.venv\Scripts\activate
# On Mac/Linux activation:
source .venv/bin/activate
```

## 3. Install Core System Requirements

```Bash
pip install -r requirements.txt
```

## 4. Inject Local Environment Variable Keys

```bash
Create a .env file right within the root workspace and drop in your private endpoint authorization tokens:
API_KEY=your_secret_api_token_here
```

## 5. Fire Up the Engine Locally

```Bash
streamlit run app.py
```

## Production Cloud Deployment Process

*This interface runs completely live in production via Streamlit Community Cloud directly pulling from main Git branch trees.

*To maintain security, local .env keys are blocked from code sync operations using active .gitignore rules. Instead, private parameters are securely loaded during cloud build stages via Advanced App Settings -> Secrets Dashboard using standard TOML styling configurations

## Author & Contributors

ML Engineer: Hafiz Muhammad Faizan

Project Name: SafeX Chat Live Agent

Version: 1.0.0

License: MIT License

Website: www.hafizmfaizan.site
