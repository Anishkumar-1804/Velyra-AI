# Velyra.ai

> **Speak English. Naturally.**  
> *A voice-first, local-first English conversation partner and evaluation engine designed for students, job candidates, and professionals.*

---

## 📑 Table of Contents

- [🌟 Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [📋 Prerequisites](#-prerequisites)
- [⚙️ Installation & Setup](#️-installation--setup)
  - [1. Clone / Download Project](#1-clone--download-project)
  - [2. Environment Configuration](#2-environment-configuration)
  - [3. Backend Setup](#3-backend-setup)
  - [4. Frontend Setup](#4-frontend-setup)
  - [5. Initialize Database & Curriculum](#5-initialize-database--curriculum)
- [🚀 Running the Project](#-running-the-project)
  - [Option A: 1-Click Launch (Recommended)](#option-a-1-click-launch-recommended)
  - [Option B: Manual Development Mode](#option-b-manual-development-mode)
  - [Option C: Production Local Mode](#option-c-production-local-mode)
- [📦 Packaging & Distribution](#-packaging--distribution)
  - [Building Frontend Assets](#building-frontend-assets)
  - [Packaging for Portable Offline Distribution](#packaging-for-portable-offline-distribution)
  - [Deploying to Vercel (Serverless)](#deploying-to-vercel-serverless)
- [🎙️ Configuration & Model Options](#️-configuration--model-options)
- [📂 Project Directory Structure](#-project-directory-structure)
- [❓ Troubleshooting & FAQs](#-troubleshooting--faqs)
- [🔒 Privacy & Data Retention](#-privacy--data-retention)

---

## 🌟 Key Features

* **100% Local & Private:** Runs entirely on your local machine with SQLite, local AI speech models, and open-source models. No signups, no cloud API keys required.
* **Natural Indian English Voices:** High-definition text-to-speech with natural Indian English accents (`en-IN-NeerjaNeural`, `en-IN-PrabhatNeural`) with offline TTS fallbacks.
* **Real Speech-to-Text:** Speech recognition powered by `faster-whisper`, tracking spoken duration, pauses, confidence scores, and speech metrics.
* **Velyra Global Conversation Controller:** Behavioral guardrails ensuring the AI partner stays strictly in character and scenario, deflecting prompt injections and out-of-context topics.
* **Backend Session Guard:** Multi-layer code and prompt boundary validator that intercepts off-topic answers and automatically triggers in-character redirections.
* **Evidence-Based Evaluation:** Real assessments computed from your actual spoken sentences — 0–100 scores across Fluency, Accuracy, Grammar, Vocabulary, Pronunciation (AI Estimate), Comprehension, Naturalness, and CEFR Level (A1–C1).
* **Detailed Speech Corrections & Vocabulary:** Side-by-side table comparing *"What You Said"* vs *"Better Version"* with clear grammatical explanations and naturalness alternatives.
* **Filler Word & Repetition Analytics:** Tracks filler word rate (e.g. *um*, *uh*, *actually*, *basically*, *like*) and repetitive patterns with Recharts visual charts.
* **7 Comprehensive Practice Genres:** 35+ speaking scenarios spanning College Life, Daily Life, Shopping, Travel, Cooking & Food, Casual Talks, and Professional Talks.
* **Warm Sand & Terracotta Aesthetic:** Minimalist design with multi-state responsive microphone controls, live audio waveform visualizers, and progress dashboards.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│               Frontend (React + Vite + Tailwind)       │
│  - Live Audio Recorder (Web Audio API / VAD)           │
│  - Real-time Audio Waveform Visualizer                 │
│  - Interactive Scenario Chatroom & Feedback Dashboard   │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP REST / Multipart Audio
                           ▼
┌────────────────────────────────────────────────────────┐
│               Backend (FastAPI + Python)               │
│  ├── STT Service (faster-whisper + Filler Detection)   │
│  ├── LLM Engine (Qwen / Transformers Local Inference)  │
│  ├── TTS Engine (edge-tts / pyttsx3 Fallback)          │
│  ├── Session Guard (Anti-Injection & Boundary Checker) │
│  ├── Scoring Engine (Mathematical & CEFR Evaluator)    │
│  └── Storage (SQLite + SQLAlchemy ORM)                 │
└────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

Before starting, ensure you have the following installed on your machine:

1. **Python:** Version `3.10` or `3.11` (Python 3.12+ may require building wheels for some audio dependencies).
   - [Download Python](https://www.python.org/downloads/)
   - *Ensure "Add Python to PATH" is checked during installation.*
2. **Node.js:** Version `v18.0.0` or newer (includes `npm`).
   - [Download Node.js](https://nodejs.org/)
3. **Git (Optional):** To clone the repository.
   - [Download Git](https://git-scm.com/)
4. **Hardware Requirements:**
   - **CPU:** Any modern multi-core processor (Intel i5/i7/i9, AMD Ryzen, Apple Silicon M-series).
   - **RAM:** Minimum 8 GB (16 GB recommended for local LLM models).
   - **GPU (Optional):** NVIDIA GPU with CUDA support for accelerated STT and LLM inference.

---

## ⚙️ Installation & Setup

### 1. Clone / Download Project

```bash
# Clone the repository
git clone https://github.com/your-username/velyra-ai.git
cd velyra-ai
```

### 2. Environment Configuration

Create a local environment file by copying the template:

#### Windows (Command Prompt / PowerShell):
```cmd
copy .env.example .env
```

#### Linux / macOS:
```bash
cp .env.example .env
```

You can inspect or customize `.env` as needed:
```env
ENV=development
DEBUG=true
DATABASE_URL=sqlite:///data/velyra.db
STT_MODEL=base.en
LLM_MODEL=Qwen/Qwen2.5-0.5B-Instruct
TTS_VOICE=en-IN-NeerjaNeural
TTS_SPEED=1.0
DEVICE=auto
COMPUTE_TYPE=auto
STORE_AUDIO_LOCALLY=false
AUTO_PLAY_TTS=true
```

### 3. Backend Setup

It is strongly recommended to use a Python virtual environment:

#### Windows:
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install backend dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

#### Linux / macOS:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 4. Frontend Setup

Open a terminal in the `frontend` folder to install dependencies:

```bash
cd frontend
npm install
cd ..
```

### 5. Initialize Database & Curriculum

Run the database seeder to create tables in SQLite and seed the 7 genres and 35+ conversation scenarios:

```bash
python scripts/seed_database.py
```

*Output should indicate:*
```
[Database] Initializing tables...
[Database] Seeding 7 Genres and 35+ Scenarios...
[Database] Database initialized and seeded successfully!
```

---

## 🚀 Running the Project

### Option A: 1-Click Launch (Recommended)

Convenient startup scripts are provided to verify dependencies, seed the database, and launch both backend and frontend servers in one command:

#### Windows:
Double-click `start.bat` or run:
```cmd
start.bat
```

#### Linux / macOS:
Make executable and execute `start.sh`:
```bash
chmod +x start.sh
./start.sh
```

The script will automatically open `http://localhost:5173` in your browser.

---

### Option B: Manual Development Mode

If you prefer running services in separate terminal windows for debugging:

#### Terminal 1 — Backend (FastAPI):
```bash
# Make sure your virtual environment is activated
# Windows: venv\Scripts\activate | Linux/macOS: source venv/bin/activate

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API documentation (Swagger UI) is available at: `http://localhost:8000/docs`*

#### Terminal 2 — Frontend (Vite Dev Server):
```bash
cd frontend
npm run dev
```
*Access the app at: `http://localhost:5173`*

---

### Option C: Production Local Mode

To test a full production build served directly via FastAPI:

1. **Build Frontend:**
   ```bash
   cd frontend
   npm run build
   cd ..
   ```
2. **Start Backend Server:**
   ```bash
   python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
   ```
3. Open `http://localhost:8000` in your browser.

---

## 📦 Packaging & Distribution

### Building Frontend Assets

To bundle the frontend for production:
```bash
cd frontend
npm run build
```
This compiles TypeScript, bundles React components, and minifies assets into `frontend/dist/`.

### Packaging for Portable Offline Distribution

To create a standalone portable bundle for distribution:

1. **Pre-build Frontend:**
   ```bash
   cd frontend
   npm run build
   cd ..
   ```
2. **Pre-seed Database:**
   ```bash
   python scripts/seed_database.py
   ```
3. **Bundle Files for Distribution:**
   Package the following files and folders into an archive (e.g. `velyra-ai-v1.0.0.zip`):
   - `backend/`
   - `frontend/dist/`
   - `data/`
   - `scripts/`
   - `start.bat` & `start.sh`
   - `.env.example`
   - `README.md`
   *(Exclude `node_modules`, `.git`, `.pytest_cache`, and `__pycache__`)*

4. **Recipient Execution:**
   The end user only needs Python and Node.js (or a pre-bundled Python portable environment) and can launch `start.bat` / `start.sh`.

### Deploying to Vercel (Serverless)

The repository includes pre-configured [`vercel.json`](file:///e:/Zyorion%20Technologies/English%20Tutor/vercel.json) and [`api/index.py`](file:///e:/Zyorion%20Technologies/English%20Tutor/api/index.py) for Vercel deployment:

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. Deploy the project:
   ```bash
   vercel
   ```
3. Vercel automatically runs the frontend build script (`cd frontend && npm install && npm run build`) and routes `/api/*` requests to `api/index.py`.

## 🎙️ Configuration & Model Options

You can adjust speech and language model configurations either through the in-app **Settings** page (`/settings`) or in your `.env` file:

| Setting | Options / Examples | Default | Description |
| :--- | :--- | :--- | :--- |
| `STT_MODEL` | `tiny.en`, `base.en`, `small.en` | `base.en` | Whisper model size. `tiny.en` is fastest; `small.en` has higher accuracy. |
| `LLM_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` | `Qwen/Qwen2.5-0.5B-Instruct` | Local HuggingFace conversational model identifier. |
| `TTS_VOICE` | `en-IN-NeerjaNeural`, `en-IN-PrabhatNeural` | `en-IN-NeerjaNeural` | Natural Indian English voice (Female / Male). |
| `TTS_SPEED` | `0.75`, `1.0`, `1.25`, `1.5` | `1.0` | Speech playback rate. |
| `DEVICE` | `auto`, `cuda`, `cpu` | `auto` | Execution hardware. Auto-detects NVIDIA CUDA GPU if available. |
| `COMPUTE_TYPE`| `auto`, `float16`, `int8` | `auto` | Quantization precision. `float16` for GPU, `int8` for CPU. |
| `STORE_AUDIO_LOCALLY` | `true`, `false` | `false` | Whether to save user spoken audio to disk or discard after STT. |

---

## 📂 Project Directory Structure

```
velyra-ai/
├── api/
│   └── index.py                 # Vercel serverless entrypoint
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app initialization & route registration
│   │   ├── config.py            # Device detection (CPU/CUDA) & environment settings
│   │   ├── database.py          # SQLite engine & SQLAlchemy session factory
│   │   ├── models/              # SQLAlchemy database ORM models
│   │   │   ├── genre.py         # Practice genres & scenarios
│   │   │   ├── session.py       # Conversation sessions & turns
│   │   │   ├── evaluation.py    # CEFR scores & grammatical feedback
│   │   │   └── settings.py      # User model & voice preferences
│   │   ├── schemas/             # Pydantic validation schemas
│   │   ├── routers/             # REST endpoints (genres, units, sessions, turns, eval)
│   │   ├── services/            # Core processing logic
│   │   │   ├── stt_service.py   # faster-whisper STT & filler rate calculator
│   │   │   ├── llm_service.py   # Local conversational model inference
│   │   │   ├── tts_service.py   # Natural Indian English TTS & audio caching
│   │   │   ├── session_guard.py # Scenario boundary & anti-injection guardrails
│   │   │   ├── scoring_service.py # CEFR estimation & mathematical metrics
│   │   │   └── evaluation_service.py # Detailed evaluation & feedback generator
│   │   ├── prompts/             # System prompts & evaluator prompts
│   │   └── seed/
│   │       └── curriculum.py    # Complete 7-genre idempotent curriculum
│   └── requirements.txt         # Backend Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI (MicButton, AudioVisualizer, MetricsCard, Logo)
│   │   ├── pages/               # Views (Home, Genres, Scenarios, LiveRoom, Results, Settings)
│   │   ├── hooks/               # Custom hooks (useAudioRecorder, useVAD)
│   │   ├── services/api.ts      # Axios API client
│   │   └── styles/index.css     # Design tokens & warm sand/terracotta palette
│   ├── package.json             # Frontend dependencies & scripts
│   ├── vite.config.ts           # Vite configuration & proxy settings
│   └── tailwind.config.js       # Tailwind CSS configuration
├── data/
│   ├── velyra.db                # SQLite database file
│   └── audio/                   # TTS audio cache directory
├── scripts/
│   └── seed_database.py         # Standalone database initialization script
├── .env.example                 # Example environment variables template
├── start.bat                    # Windows 1-click startup batch script
├── start.sh                     # Linux/macOS 1-click startup shell script
├── vercel.json                  # Vercel deployment configuration
└── README.md                    # Project documentation
```

---

## ❓ Troubleshooting & FAQs

### 1. Browser Microphone Not Working
- Ensure you have granted microphone permissions in your browser.
- In Chrome / Edge: Click the lock icon in the URL bar (`http://localhost:5173`) and set **Microphone** to **Allow**.
- Test using standard 16kHz or 44.1kHz audio input.

### 2. Port `8000` or `5173` is Already in Use
- Change backend port:
  ```bash
  python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8080
  ```
- Change frontend port:
  ```bash
  cd frontend && npm run dev -- --port 3000
  ```
- Update `frontend/src/services/api.ts` if the backend port is modified.

### 3. PyTorch / CUDA GPU Acceleration
- By default, `DEVICE=auto` will detect CUDA if `torch.cuda.is_available()`.
- To run with CUDA on NVIDIA GPUs:
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cu121
  ```
- To force CPU execution on laptops without a discrete GPU, set `DEVICE=cpu` in `.env`.

### 4. Database Reset / Re-seed
- If you wish to reset your practice history and re-seed the curriculum from scratch, run:
  ```bash
  python scripts/seed_database.py
  ```

---

## 🔒 Privacy & Data Retention

- **Zero Cloud Leakage:** All audio transcriptions and evaluations run locally on your system.
- **Audio Lifecycle:** Spoken audio recordings are held in memory during analysis and discarded immediately (unless `STORE_AUDIO_LOCALLY=true` is enabled in settings).
- **Data Export & Deletion:** Practice transcripts and evaluations are saved in your local SQLite database. You can export all session records as JSON/CSV or purge your history directly from the in-app view.

---

## 📄 License & Acknowledgments

Built for learners, job seekers, and professionals looking to build speaking fluency and confidence.  
Powered by FastAPI, React, faster-whisper, edge-tts, and modern open-source AI tools.
