# 📄 NLP Resume Screener

> An AI-powered resume analysis tool that matches resumes against job descriptions using Natural Language Processing and LLM-generated career feedback.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red?style=flat-square&logo=streamlit)
![spaCy](https://img.shields.io/badge/spaCy-3.7.4-09A3D5?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧠 What Is This?

Most resume screeners just classify resumes into job categories. This one goes further.

Upload your resume, paste a job description — and get back a **match score**, a **skill gap breakdown**, and **AI-generated career advice** tailored specifically to your profile and the role you're targeting.

Built from the ground up using a modular NLP pipeline — no black boxes, no magic buttons.

---

## ✨ Features

- **Resume Parsing** — supports PDF, DOCX, and TXT formats
- **Text Cleaning Pipeline** — removes noise, URLs, emails, stopwords, and lemmatizes text
- **Skill Extraction** — matches 70+ skills across 7 categories using a curated skills library
- **Three-Layer Similarity Scoring**
  - TF-IDF cosine similarity (keyword matching)
  - Semantic similarity via Sentence Transformers (meaning-based)
  - Skill overlap score (direct skill comparison)
- **Skill Gap Analysis** — identifies missing skills ranked by priority (Critical → Nice to Have)
- **Category Coverage Bars** — visual breakdown of coverage per skill category
- **AI Career Feedback** — powered by Groq's LLaMA 3, generates personalized:
  - Overall assessment
  - Strengths to highlight
  - Critical action plan
  - Quick wins
  - Honest career advice

---

## 🏗 Project Architecture

```
resume_screener/
│
├── app/
│   ├── main.py                  ← Streamlit frontend
│   └── ui_components.py         ← Reusable UI elements
│
├── src/
│   ├── parser.py                ← PDF/DOCX/TXT text extraction
│   ├── cleaner.py               ← Text preprocessing pipeline
│   ├── extractor.py             ← Skill & entity extraction
│   ├── similarity.py            ← TF-IDF + semantic scoring
│   ├── gap_analyzer.py          ← Gap analysis & prioritization
│   └── ai_feedback.py           ← Groq LLaMA 3 feedback generation
│
├── data/
│   ├── raw/                     ← Local datasets (not pushed to GitHub)
│   └── processed/               ← Cleaned outputs
│
├── notebooks/
│   └── 01_eda_resume_dataset.ipynb
│
├── sample_data/
│   ├── sample_resume.pdf        ← Test resume
│   └── sample_jd_data_analyst.txt
│
├── tests/
│   └── test_parser.py
│
├── .env                         ← API keys (never pushed)
├── .gitignore
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## ⚙️ How The Pipeline Works

```
User uploads Resume (PDF/DOCX/TXT)
            +
User pastes Job Description
            ↓
┌─────────────────────────────┐
│  1. PARSER                  │  Extracts raw text from file
│  2. CLEANER                 │  Removes noise, lemmatizes
│  3. EXTRACTOR               │  Pulls skills, titles, entities
│  4. SIMILARITY              │  Computes 3-layer match score
│  5. GAP ANALYZER            │  Identifies & prioritizes gaps
│  6. AI FEEDBACK             │  Groq LLaMA 3 career advice
└─────────────────────────────┘
            ↓
Match Score + Skill Breakdown + AI Feedback
```

---

## 🚀 Getting Started (Local Setup)

### Prerequisites

- Python 3.11
- A free [Groq API key](https://console.groq.com)
- Git

---

### Step 1 — Clone The Repository

```bash
git clone https://github.com/YOUR_USERNAME/nlp-resume-screener.git
cd nlp-resume-screener
```

---

### Step 2 — Create A Virtual Environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Mac/Linux
python -m venv .venv
source .venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Download The spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

---

### Step 5 — Set Up Your API Key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at [console.groq.com](https://console.groq.com)

---

### Step 6 — Run The App

```bash
python -m streamlit run app/main.py
```

Open your browser at `http://localhost:8501`

---

## 🧪 Quick Test (Without Resume)

Don't have a resume file handy? Use the provided sample files:

1. Download [`sample_data/sample_resume.pdf`](sample_data/sample_resume.pdf)
2. Copy any job description from [`sample_data/`](sample_data/)
3. Upload the resume and paste the JD into the app
4. Hit **Analyze Resume**

---

## 📦 Download Full Datasets (Optional)

The raw datasets are not included in this repo due to size. They are only needed if you want to run the EDA notebooks locally.

Install the Kaggle API:
```bash
pip install kaggle
```

Set up your Kaggle token:
```
1. Go to kaggle.com → Account → API → Create New Token
2. Place kaggle.json in:
   Windows → C:/Users/YOUR_NAME/.kaggle/kaggle.json
   Mac/Linux → ~/.kaggle/kaggle.json
```

Download datasets:
```bash
python download_data.py
```

**Dataset Sources:**
- Resumes: [kaggle.com/datasets/gauravduttakiit/resume-dataset](https://kaggle.com/datasets/gauravduttakiit/resume-dataset)
- Job Postings: [kaggle.com/datasets/arshkon/linkedin-job-postings](https://kaggle.com/datasets/arshkon/linkedin-job-postings)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| NLP | spaCy, NLTK |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Similarity | scikit-learn (TF-IDF + Cosine) |
| AI Feedback | Groq API (LLaMA 3.3 70B) |
| Document Parsing | pdfplumber, python-docx, PyPDF2 |
| Frontend | Streamlit |
| Environment | python-dotenv |

---

## 📊 Match Score Breakdown

The final match score is a weighted combination of three signals:

```
TF-IDF Similarity    25%  →  Exact keyword overlap
Semantic Similarity  50%  →  Meaning-based comparison
Skill Overlap        25%  →  Direct skill matching
─────────────────────────
Final Score         100%
```

| Score Range | Label |
|---|---|
| 80% and above | Excellent Match 🟢 |
| 60% – 79% | Good Match 🟡 |
| 40% – 59% | Partial Match 🟠 |
| Below 40% | Low Match 🔴 |

---

## 🔐 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |

Never commit your `.env` file. It is already excluded in `.gitignore`.

---

## 🤝 Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your branch: `git push origin feat/your-feature`
5. Open a Pull Request

---

## 📁 Skill Categories Covered

| Category | Examples |
|---|---|
| Programming Languages | Python, R, SQL, Java, Scala |
| Data Science | Machine Learning, NLP, Deep Learning, EDA |
| ML Frameworks | scikit-learn, PyTorch, TensorFlow, spaCy |
| Data Tools | pandas, NumPy, Matplotlib, Tableau |
| Databases | PostgreSQL, MongoDB, Snowflake, BigQuery |
| Cloud & DevOps | AWS, GCP, Docker, Git, FastAPI |
| Soft Skills | Communication, Leadership, Problem Solving |

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Sheikh Syeed**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [linkedin.com/in/YOUR_PROFILE](https://linkedin.com/in/YOUR_PROFILE)

---

> Built as a portfolio project for Data Science internship readiness.
> Feedback and suggestions are welcome!
