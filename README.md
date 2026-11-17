# Luna Writer 🌙

**Luna Writer** is a full-stack English reading, writing, and educational assessment platform. It enables English language learners and authors to explore realistic writing across four dedicated categories, compose and upload documents in an intuitive Writing Studio, and receive Cambridge B1 (PET) suitability evaluations with actionable feedback.

---

## 🏗️ Architecture & Technology Stack

The project adheres to a separated full-stack structure:

- **Frontend:** Semantic HTML5, CSS3 (Modern SaaS design system, Bento-grid layouts, CSS Custom Properties), and modular vanilla JavaScript.
- **Backend:** Python 3 with **FastAPI**.
- **Database:** **MongoDB** (with `motor` async driver and `pymongo`), featuring a resilient auto-detecting embedded engine fallback.

### Why FastAPI?
1. **Asynchronous Non-Blocking Performance:** Matches MongoDB's async `motor` driver, allowing high concurrency for reading libraries and AI reviews.
2. **Schema Integrity:** Native integration with **Pydantic V2** enforces rigorous validation for user drafts, file uploads, and CEFR scoring models.
3. **Interactive Documentation:** Automatically generates interactive OpenAPI Swagger UI at `http://127.0.0.1:8000/docs`.
4. **Clean Modular Routing:** `APIRouter` cleanly organizes writings, reviews, bookmarks, uploads, and settings into distinct modules.

---

## 📂 Project Structure

```
antigravity writer/
├── backend/
│   └── app/
│       ├── config.py             # Environment configuration & constraints
│       ├── database.py           # MongoDB connection manager & embedded JSON fallback
│       ├── main.py               # FastAPI application entrypoint & static mount
│       ├── models/
│       │   ├── writing.py        # Pydantic models for Writings, Bookmarks & Settings
│       │   └── review.py         # AI B1 assessment schemas & observations
│       ├── routers/
│       │   ├── writings.py       # CRUD & category filtering (/stories, /letters, etc.)
│       │   ├── reviews.py        # /api/reviews/evaluate & history
│       │   ├── bookmarks.py      # /api/bookmarks toggle & listing
│       │   ├── uploads.py        # Secure file parsing (.txt, .md, .docx, .json)
│       │   ├── settings.py       # User appearance & reading settings persistence
│       │   └── status.py         # Real-time health, MongoDB & AI status
│       └── services/
│           ├── b1_evaluator.py   # Cambridge B1 rubric engine & optional LLM connector
│           └── seed_data.py      # Pre-seeded sample stories, letters, articles & emails
├── frontend/
│   ├── index.html                # Semantic HTML5 shell
│   ├── css/
│   │   ├── main.css              # Design system, themes, bento layout & typography
│   │   ├── reader.css            # Dedicated reader modal & text-to-speech styling
│   │   ├── studio.css            # Writing studio, prompt drawer & upload dropzone
│   │   ├── review.css            # CEFR B1 report card, dial & diff cards
│   │   └── settings.css          # Theme swatches, font pickers & live preview
│   └── js/
│       ├── api.js                # Documented REST API fetch client
│       ├── state.js              # Central reactive store & preference synchronizer
│       ├── router.js             # SPA routing for all category & workspace paths
│       ├── components/
│       │   ├── card.js           # Writing card component with bookmarking
│       │   ├── readerModal.js    # Dedicated reading view with TTS & formatting controls
│       │   ├── reviewModal.js    # B1 evaluation report with interactive sentence acceptance
│       │   └── toast.js          # Accessible toast notifications
│       └── pages/
│           ├── home.js           # Bento-grid showcase & instant sentence tester
│           ├── category.js       # Distinct category views with search & filters
│           ├── studio.js         # Writing studio, file uploader & Cambridge prompts
│           ├── myWriting.js      # Drafts, Published, Bookmarks & Review history tabs
│           └── settings.js       # Customization settings with live preview
├── uploads/                      # Upload workspace
├── .env.example                  # Environment template
├── .env                          # Local active environment
├── requirements.txt              # Python dependencies
├── run.py                        # Server runner script
├── test_suite.py                 # Automated integration test suite
└── README.md                     # Documentation
```

---

## 🧭 Pages & Navigation Map

- **Home (`/`):** Features an introduction to Luna Writer, bento-grid dashboard, quick stats, featured pieces, an instant Cambridge B1 sentence analyzer, and links to all four categories.
- **Stories (`/stories`):** Creative narratives and slice-of-life accounts with filters for level (A2, B1, B2), length (<300, 300-600, >600 words), and topic.
- **Letters (`/letters`):** Formal and semi-formal correspondence, letters of complaint, gratitude, and inquiry.
- **Articles (`/articles`):** Informative articles addressing student habits, urban transit, and language acquisition.
- **Emails (`/emails`):** Authentic everyday email correspondence for work, travel, and neighbourhood events.
- **Writing Studio (`/studio`):** Distraction-free editor with live word count, character count, reading time, upload dropzone, Cambridge B1 exam prompts, preview mode, and draft saving.
- **My Writing (`/my-writing`):** Unified dashboard with tabs for `Drafts`, `Published`, `Bookmarks`, and `Past B1 Reviews`.
- **Customization Settings (`/settings`):** Live preview customization for themes, brand accent colors, typography, font size, line spacing, reading column width, interface density, and card styles.

---

## 📖 Reading Library & Reader Controls

Clicking any card opens a **Dedicated Reading View** with:
- **Adjustable Text Size:** `A-` and `A+` controls.
- **Line Spacing:** `Compact (1.5x)`, `Normal (1.8x)`, and `Relaxed (2.1x)`.
- **Reading Width:** `Narrow (640px)`, `Medium (780px)`, and `Wide (920px)`.
- **Web Speech Audio Playback:** Listen to the text read aloud with pronunciation pacing (`0.85x`, `1.0x`, `1.15x`).
- **Interactive Bookmarking:** Save pieces for later study.
- **AI Review Shortcut:** Directly launch a Cambridge B1 evaluation from the reader.

---

## ✍️ Writing Studio & File Uploads

- **Supported Document Formats:** `.txt`, `.md`, `.docx`, `.json`.
- **Size Limit:** 2 MB.
- **Extraction:** Native XML parsing extracts titles and content from Word `.docx` documents and Markdown files automatically.
- **Cambridge B1 Exam Prompts:** Built-in writing prompts for Story Starters, Formal Letters, School Articles, and Friendly Emails.
- **Status & Visibility:** Works default to `private draft`. Users can change visibility to `public` or update status to `published` at any time.

---

## 🤖 Cambridge B1 Educational AI Review

When requested, the review evaluates text against CEFR B1 benchmarks:
1. **Estimated Level & Verdict:** `A2 (Below B1)`, `B1 (Suitable for B1)`, `B2 (Above B1 - Slightly Advanced)`.
2. **Suitability Score:** Visual circular dial (0–100).
3. **Four Specific Observation Categories:**
   - **Vocabulary:** Lexical profile, everyday topic words, phrasal verbs, idioms vs archaic words.
   - **Grammar:** Control over past simple, past continuous, present perfect, conditionals, modal verbs, and passive voice.
   - **Sentence Length & Rhythm:** Mean sentence length (ideal: 12–20 words), sentence variety, readability ease.
   - **Organization & Cohesion:** Paragraph structure and transition markers (`however`, `although`, `in addition`, `finally`).
4. **Interactive Sentence Suggestions:** Provides specific sentence improvements. Clicking **Accept Suggestion** automatically updates the sentence inside the Writing Studio editor.
5. **Educational Disclaimer:** *“Educational estimate based on CEFR B1 benchmarks; not an official Cambridge Assessment English exam result or guarantee.”*
6. **AI Service Modes:**
   - **Demonstration & Heuristic Mode:** Built-in rule-based linguistic engine (active by default when no API key is set).
   - **Live LLM Integration:** Connect your Google Gemini API key (`GEMINI_API_KEY`) or OpenAI key (`OPENAI_API_KEY`) in `.env` for generative AI reviews.

---

## ⚙️ Configuration & MongoDB Setup

### 1. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configuration variables:
```ini
HOST=127.0.0.1
PORT=8000
DEBUG=true

# MongoDB Configuration
# Local MongoDB: mongodb://localhost:27017
# Or MongoDB Atlas: mongodb+srv://<user>:<password>@cluster.mongodb.net
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=luna_writer

# Optional AI API Key (leave blank to use the built-in Cambridge B1 heuristic engine)
GEMINI_API_KEY=
OPENAI_API_KEY=
AI_MODEL_NAME=gemini-1.5-flash

MAX_UPLOAD_SIZE_BYTES=2097152
ALLOWED_EXTENSIONS=.txt,.md,.docx,.json
```

### 2. MongoDB Dual-Engine Architecture
- **When MongoDB is running:** Connects via `motor` async client, creates indexes on `category`, `level`, `created_at`, and `writing_id`, and stores all records in MongoDB.
- **When MongoDB is not running:** Automatically activates the **High-Fidelity Embedded Database Engine**, persisting collections to `.data/luna_embedded_db.json`. The site remains fully interactive and functional without errors.

---

## 🚀 How to Run Luna Writer

### 1. Install Dependencies
```bash
# Activate your virtual environment
.\.venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Run Integration Tests
Verify all 11 endpoints, database logic, AI evaluator, and uploads:
```bash
python test_suite.py
```

### 3. Start the Server
```bash
python run.py
```
Or with Uvicorn directly:
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Open in Browser
- **Application URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Documentation (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Docs (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
