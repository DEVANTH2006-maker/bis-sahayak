# BIS Sahayak 🏛️

**AI-Powered Intelligent Assistant for Indian Standards and BIS Services**

> SIH26107 — Ministry of Consumer Affairs, Food & Public Distribution

---

## What is BIS Sahayak?

BIS Sahayak is a Retrieval-Augmented Generation (RAG) chatbot that helps users navigate the complex landscape of Indian Standards (IS) and Bureau of Indian Standards (BIS) services. It answers questions, recommends applicable standards, guides through certification processes, explains hallmarking, and helps find testing labs — all with source-backed citations.

### Key Features

| Feature | Description |
|---------|-------------|
| 🗣️ **Natural Language Q&A** | Ask questions about Indian Standards in plain language (any supported language) |
| 🔍 **Product → Standard Matching** | Describe your product, get recommended IS numbers |
| 📋 **Certification Guide** | Step-by-step walkthroughs for ISI mark, CRS, and Hallmarking |
| 💍 **Hallmarking Help** | HUID verification, purity grades, hallmarking process |
| 🔬 **Lab Lookup** | Find BIS-recognized testing labs by category and city |
| 🌐 **Multilingual** | Hindi, Bengali, Tamil, Telugu, Marathi, and more |
| 📚 **Source Citations** | Every answer shows the document and clause it came from |

---

## Architecture

```
┌─────────────┐     HTTP      ┌───────────────┐
│   Next.js   │ ────────────── │   FastAPI      │
│   Frontend  │               │   Backend      │
│  (React)    │               │   (Python)     │
└─────────────┘               └───────┬───────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                   │
              ┌─────▼─────┐    ┌──────▼──────┐    ┌──────▼──────┐
              │  ChromaDB  │    │   LLM API   │    │ sentence-   │
              │  (Vector   │    │  (OpenAI /  │    │ transformers │
              │   Store)   │    │  Anthropic) │    │ (Embeddings) │
              └─────┬──────┘    └─────────────┘    └─────────────┘
                    │
         ┌──────────┴──────────┐
         │ BIS Standard PDFs   │
         │ Certification Docs  │
         │ Product Mapping     │
         │ Lab Directory       │
         └─────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- An OpenAI or Anthropic API key

### 1. Clone and Setup

```bash
# Backend
cd backend
cp .env.example .env   # Edit .env with your API key
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Ingest Documents

```bash
cd backend
# Place your BIS PDFs in data/standards/ and data/schemes/
python scripts/ingest.py
```

### 3. Start Development Servers

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Docker (One Command)

```bash
docker-compose up --build
```

---

## Project Structure

```
bis-sahayak/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   ├── config.py            # Environment config
│   │   ├── routers/
│   │   │   ├── chat.py          # Main chat endpoint
│   │   │   ├── standards.py     # Standard recommendation API
│   │   │   └── labs.py          # Lab lookup API
│   │   ├── services/
│   │   │   ├── rag.py           # RAG pipeline
│   │   │   ├── llm.py           # LLM client (OpenAI/Anthropic)
│   │   │   ├── embeddings.py    # Embedding service
│   │   │   ├── matcher.py       # Product → Standard matcher
│   │   │   ├── certification.py # Certification & hallmarking guides
│   │   │   ├── labs.py          # Lab search service
│   │   │   └── translator.py    # Multilingual translation
│   │   └── models/
│   │       └── schemas.py       # Pydantic models
│   ├── data/                    # BIS documents & datasets
│   ├── scripts/ingest.py        # Document ingestion pipeline
│   ├── chroma_db/               # ChromaDB vector store
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main chat page
│   │   ├── layout.tsx           # Root layout
│   │   └── labs/page.tsx        # Lab search page
│   ├── components/
│   │   ├── ChatWindow.tsx       # Main chat UI
│   │   ├── MessageBubble.tsx    # Message display
│   │   ├── SourceCitation.tsx   # Citation chips
│   │   ├── QuickActions.tsx     # Quick action buttons
│   │   ├── LanguageToggle.tsx   # Language selector
│   │   ├── LabSearch.tsx        # Lab search panel
│   │   └── TypingIndicator.tsx  # Loading animation
│   └── lib/api.ts               # API client
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Main chat endpoint (supports all modes) |
| `POST` | `/api/standards/recommend` | Get standard recommendations |
| `GET`  | `/api/labs` | Search labs by category/city/state |
| `GET`  | `/api/labs/all` | List all labs |
| `GET`  | `/health` | Health check |

### Chat Request Body

```json
{
  "message": "What does IS 302 say about electrical safety?",
  "language": "en",
  "mode": "general"
}
```

Modes: `general` | `recommend` | `certify` | `hallmark` | `lab`

---

## Data You Need to Collect

### 1. BIS Standard PDFs (15-30)
Download from [bis.gov.in](https://bis.gov.in) across 2-3 categories:
- Electrical (IS 302, IS 1554, IS 694)
- Packaged food (IS 1165, IS 14543)
- Textiles (IS 1966, IS 14878)

Place in `backend/data/standards/`

### 2. Certification Scheme Documents
- ISI Mark scheme overview
- CRS (Compulsory Registration Scheme) guide
- Hallmarking scheme document

Place in `backend/data/schemes/`

### 3. Product → Standard Mapping
Create `backend/data/product_standards_map.csv`:
```csv
product_category,keywords,is_number,title,description
electrical appliances,electrical,appliance,IS 302,Safety of household appliances,...
```

### 4. Lab Directory
Create `backend/data/labs.json` with BIS-recognized labs.

---

## Demo Queries (for presentation)

1. "What does IS 302 say about insulation resistance for household appliances?"
2. "I manufacture cotton t-shirts — which Indian Standards apply?"
3. "How do I get the ISI mark for my electronics product?"
4. "What is HUID and how do I verify my gold jewelry's hallmark?"
5. "Which BIS-recognized labs in Mumbai test electrical products?"
6. (Hindi) "सोने की अंगूठी की hallmarking कैसे करवाएं?"

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, Tailwind CSS |
| Backend | Python 3.11, FastAPI, Pydantic |
| LLM | OpenAI GPT-4o-mini / Anthropic Claude |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) — free, local |
| Vector DB | ChromaDB (persistent, runs in-process) |
| Document Processing | pdfplumber |
| Deployment | Docker, Vercel (frontend), Render (backend) |

---

## Important Disclaimers

- This prototype demonstrates the system on a **representative sample** of BIS standards, not all of them
- Always verify critical compliance details at [bis.gov.in](https://bis.gov.in)
- The assistant provides AI-generated guidance — it does not replace official BIS certification processes

---

**Built with 🇮🇳 for SIH26107**
