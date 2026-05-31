"""
Vaaniverse RAG Chatbot Backend
Free Stack: Ollama + LangChain + Chroma
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain.schema import Document

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
OLLAMA_MODEL = "mistral"  # Free, lightweight model
EMBEDDINGS_MODEL = "nomic-embed-text"  # Free embeddings
CHROMA_PATH = "./chroma_db"
SUPABASE_URL = "https://fbdfmozeqmjunmhnesbv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZiZGZtb3plcW1qdW5taG5lc2J2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkyNDgxMjAsImV4cCI6MjA5NDgyNDEyMH0.WTz11nlIfEDuwY5SU8IRAHaVZIbkWNbAiE9w5xSwdwM"
MAKE_WEBHOOK = "https://hook.eu1.make.com/yrevc45uuonvga6q2anaf4arekjvqcmp"
TEAM_EMAIL = "cxo@vaaniverse.com"

# ─────────────────────────────────────────────
# VAANIVERSE KNOWLEDGE BASE (RAG Content)
# ─────────────────────────────────────────────
KB_CONTENT = """
VAANIVERSE - Company Overview
Vaaniverse is a Fractional CMO and growth strategy firm serving SaaS companies and startups.
We help build unbeatable market positioning, generate quality leads, and scale revenue without full-time CMO cost.

WHO WE ARE:
We work with SaaS founders and B2B companies ($0.2M+ ARR) who are burned by agencies, have no clear marketing direction, and need executive-level marketing leadership without the full-time cost.

WHAT WE DO:
1. Fractional CMO Leadership - Strategic marketing oversight and guidance
2. Market Positioning & Research - Blue Ocean strategy for competitive advantage
3. Brand Strategy - Narrative, storytelling, premium pricing positioning
4. Go-to-Market Strategy - Multi-channel execution (online + offline)
5. Performance Marketing - Google Ads, Meta Ads, LinkedIn, SEO, paid advertising
6. Sales Enablement - Sales toolkit, collateral, CRM setup, training
7. AI Integration - Custom AI agents, marketing automation, workflow automation
8. PR & Influencer Marketing - Media relations, thought leadership, partnerships
9. Analytics & Reporting - CAC, CPL, ROI, predictive analytics

SERVICE PACKAGES:

GROWTH STARTER - ₹1,25,000/month
Best For: Startups with 1-10 employees, annual revenue ₹50L - ₹2Cr
Includes:
- Fractional CMO oversight (20-25 hrs/month)
- Quarterly marketing roadmap
- Social media strategy (2 platforms)
- Content calendar (8-10 posts/month)
- Monthly performance reports
- Bi-weekly strategy calls
- Email/WhatsApp support (24-48 hour response)

GROWTH ACCELERATOR (RECOMMENDED) - ₹1,50,000/month
Best For: Scaling businesses with 10-50 employees, annual revenue ₹5Cr - ₹25Cr
Everything in Starter PLUS:
- Extended strategic oversight
- Revenue growth strategy
- 4-5 platform social media management
- Enhanced content (15-20 posts/month)
- Paid advertising (Google/Meta) up to ₹2,00,000/month
- Landing page optimization
- CRM basic setup
- Weekly strategy calls
- Bi-weekly performance reports
- Sales toolkit development

GROWTH DOMINATOR - ₹2,10,000/month
Best For: Enterprise companies with 50+ employees, annual revenue ₹10Cr+
Everything in Accelerator PLUS:
- Full Fractional CMO engagement (80-100 hrs/month)
- Board-level reporting
- Geographic expansion strategy
- Omnichannel management (8+ platforms)
- Premium content (25-30 pieces/month)
- Multi-channel paid ads (Google, Meta, LinkedIn)
- PR, media, and influencer marketing
- Custom AI agent development
- Advanced marketing automation
- White-glove service (daily availability)

OPTIONAL ADD-ONS:
- Creative Design Package: ₹30,000/month
- Additional AI Agent: ₹40,000/month
- Video Production: ₹50,000/month
- Advanced Paid ORM: ₹35,000/month

PAYMENT TERMS:
- Monthly retainer billed in advance
- Minimum 3-month commitment
- 10% discount for 6-month advance payment
- 15% discount for 12-month advance payment
- GST applicable

OUR APPROACH:
- Blue Ocean Strategy: Create uncontested market space instead of competing in crowds
- 365-Day Guarantee: Significant results within one year
- Premium Positioning: Position for premium pricing without objections
- Repeatable Frameworks: You get success frameworks you can replicate
- Niche Approach: Strategies customized extremely targeted for your specific niche

HOW WE WORK:
Step 1: Deep diagnostic and revenue mapping
Step 2: Design brand narrative
Step 3: Marketing roadmap alignment
Step 4: Market execution and experimentation
Step 5: Scale with repeatable systems

CONTACT INFORMATION:
Email: cxo@vaaniverse.com
Phone: +91 6353422903
Website: vaaniverse.com
Location: Vadodara, Gujarat, India

TEAM:
- Heema (MD, Co-Founder): Growth, Marketing & GTM Expert. 9+ years scaling SaaS from zero to millions
- Chhaya (CEO, Co-Founder): Marketing & Positioning Expert. 3+ years driving SaaS growth across 10 countries

IDEAL CLIENT PROFILE:
- Growth-oriented SaaS/B2B companies
- $0.2M+ annual revenue
- Founder-led or no full-time CMO
- Burned by agencies, need strategic clarity
- Ready to invest in sustainable growth systems
- Want data-driven, measurable results
"""

# ─────────────────────────────────────────────
# INITIALIZE RAG SYSTEM
# ─────────────────────────────────────────────
def init_rag():
    """Initialize Ollama, embeddings, and Chroma vector store"""
    try:
        # Initialize embeddings
        embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL)

        # Split knowledge base into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        docs = text_splitter.split_text(KB_CONTENT)

        # Create Document objects
        documents = [Document(page_content=doc) for doc in docs]

        # Create or load Chroma vector store
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=CHROMA_PATH,
            collection_name="vaaniverse"
        )

        return vectorstore, embeddings
    except Exception as e:
        print(f"❌ RAG init error: {e}")
        return None, None

vectorstore, embeddings = init_rag()

# ─────────────────────────────────────────────
# RAG QUERY FUNCTION
# ─────────────────────────────────────────────
def query_rag(user_query):
    """Query RAG system and return answer"""
    if not vectorstore:
        return "I'm having trouble connecting to my knowledge base. Please contact our team directly at cxo@vaaniverse.com"

    try:
        # Retrieve relevant documents
        results = vectorstore.similarity_search(user_query, k=3)
        context = "\n".join([doc.page_content for doc in results])

        # Initialize LLM
        llm = Ollama(model=OLLAMA_MODEL, temperature=0.3)

        # Create prompt template
        template = """You are Vaaniverse's helpful chatbot assistant.
Based ONLY on the provided knowledge base below, answer the user's question.

If the question cannot be answered from the knowledge base, respond with:
"I don't have that information. Please contact our team at cxo@vaaniverse.com for more details."

Never make up information. If unsure, always direct to team email.

KNOWLEDGE BASE:
{context}

USER QUESTION: {question}

ANSWER (be helpful, concise, and professional):"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm

        response = chain.invoke({
            "context": context,
            "question": user_query
        })

        return response
    except Exception as e:
        print(f"❌ Query error: {e}")
        return f"I'm having trouble processing your question. Please contact our team at {TEAM_EMAIL}"

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        user_query = data.get('message', '').strip()
        visitor_info = data.get('visitor', {})

        if not user_query:
            return jsonify({"error": "Empty message"}), 400

        # Get RAG response
        answer = query_rag(user_query)

        # Log to Supabase (optional)
        try:
            import requests
            requests.post(
                f"{SUPABASE_URL}/rest/v1/chat_logs",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "user_message": user_query,
                    "bot_response": answer,
                    "visitor_email": visitor_info.get('email'),
                    "visitor_name": visitor_info.get('name'),
                    "timestamp": datetime.now().isoformat()
                }
            )
        except:
            pass  # Logging failed, continue anyway

        return jsonify({
            "response": answer,
            "status": "success"
        })

    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({
            "response": f"Sorry, I encountered an error. Please contact {TEAM_EMAIL}",
            "error": str(e)
        }), 500

@app.route('/api/lead', methods=['POST'])
def create_lead():
    """Create lead from form submission"""
    try:
        data = request.json
        lead_data = {
            "name": data.get('name'),
            "email": data.get('email'),
            "company": data.get('company'),
            "source": "Vaaniverse RAG Chatbot",
            "timestamp": datetime.now().isoformat()
        }

        # Send to Make.com webhook
        try:
            import requests
            requests.post(MAKE_WEBHOOK, json=lead_data)
        except:
            pass

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "rag_ready": vectorstore is not None
    })

# ─────────────────────────────────────────────
# START SERVER
# ─────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
