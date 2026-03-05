# 🎯 BrandSphere AI — Automated Branding Assistant

> **CRS Artificial Intelligence Capstone 2025–26 | Scenario 1**  
> AI-Powered Automated Branding Assistant for Businesses

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-API-orange?style=flat-square)
![License](https://img.shields.io/badge/License-Academic-green?style=flat-square)

---

## 📋 Project Overview

BrandSphere AI is an end-to-end intelligent branding platform that enables small and medium-sized businesses to build a complete brand identity using AI. The platform integrates **Computer Vision**, **Generative AI (Gemini)**, **NLP**, and **Predictive Analytics** into a single Streamlit-deployed application.

**Live App:** [https://brandsphere-ai.streamlit.app](https://brandsphere-ai.streamlit.app) *(deploy and update link)*

---

## ✨ Core Features

| Module | Feature | Technology |
|--------|---------|-----------|
| 🎨 Logo & Design Studio | AI logo generation, color palette extraction, font recommendation | OpenCV, Pillow, KMeans |
| ✍️ Creative Content Hub | Tagline generation, brand narrative, multilingual translation | Gemini API, NLTK |
| 📣 Campaign Studio | Social media content, KPI prediction, regional analytics | scikit-learn, Plotly |
| 🔍 Brand Aesthetics Engine | Consistency scoring, color psychology, semantic alignment | Sentence Transformers |
| ⭐ Feedback Intelligence | Rating collection, sentiment analysis, adaptive refinement | TextBlob, Gemini API |
| 📊 Analytics Dashboard | Performance dashboards, personality radar, progress tracking | Plotly, Tableau |

---

## 🛠️ Technologies Used

- **Backend AI/ML:** Python 3.11, TensorFlow 2.x / Keras, scikit-learn, OpenCV
- **Generative AI:** Google Gemini API (gemini-1.5-flash)
- **NLP:** NLTK, Sentence Transformers (SBERT), TextBlob
- **Data Processing:** pandas, NumPy
- **Visualization:** Plotly, Tableau Public
- **Animation:** Pillow, imageio
- **Frontend:** Streamlit Cloud
- **Version Control:** GitHub
- **Storage:** Google Drive API

---

## 🚀 Installation & Local Setup

### Prerequisites
- Python 3.11+
- Gemini API key from [Google AI Studio](https://aistudio.google.com)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/IADAI205-STUDENTID-NAME.git
cd IADAI205-STUDENTID-NAME

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r config/requirements.txt

# 4. Set up environment variables
echo "GEMINI_API_KEY=your-key-here" > .env

# 5. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📱 Usage Instructions

1. **Brand Setup Tab** → Enter company name, industry, personality, target audience, tone
2. Click **"Generate Brand Kit"** to initialize the AI pipeline
3. **Logo & Design Tab** → View generated logo, color palette, font recommendations
4. **Content Hub Tab** → Generate taglines, brand story, animated GIF, and multilingual translations
5. **Campaign Studio Tab** → Select platform, region, objective → Get campaign content + KPI predictions
6. **Aesthetics Engine Tab** → Run consistency analysis and get AI improvement recommendations
7. **Feedback Tab** → Rate each module (1–5 stars) and provide comments
8. **Analytics Tab** → View feedback trends, KPI comparisons, personality radar
9. **Download Campaign Kit** → Get the full brand ZIP package from the Campaign Studio tab

---

## 📁 Repository Structure

```
IADAI205-STUDENTID-NAME/
├── app.py                          # Main Streamlit application
├── utils/
│   ├── gemini_helper.py            # Gemini API wrapper
│   ├── logo_model.py               # Logo generation & classification
│   ├── campaign_model.py           # KPI prediction model
│   └── feedback.py                 # Feedback storage & analysis
├── datasets/
│   ├── original/                   # Raw datasets (Logo, Font, Slogan, Startups, Campaign)
│   └── cleaned/                    # Preprocessed datasets ready for training
├── notebooks/
│   ├── 01_EDA.ipynb                # Exploratory Data Analysis
│   ├── 02_preprocessing.ipynb      # Data cleaning & feature engineering
│   ├── 03_logo_model.ipynb         # VGG16 logo classifier training
│   ├── 04_campaign_model.ipynb     # Random Forest KPI predictor training
│   └── 05_retraining.ipynb         # Feedback-driven model refinement
├── ui_ux/
│   ├── wireframes/                 # Figma exported screen designs
│   └── assets/                     # UI images, icons, brand assets
├── config/
│   ├── requirements.txt            # Python dependencies
│   └── docs/                       # Model cards, API documentation
├── deployment/
│   ├── streamlit_deployment.yml    # Streamlit Cloud config
│   └── .streamlit/config.toml     # Streamlit theme settings
├── PRD_BrandSphereAI.pdf           # Product Requirements Document
└── README.md                       # This file
```

---

## 🤖 AI Models

| Model | Architecture | Dataset | Metric |
|-------|-------------|---------|--------|
| Logo Classifier | VGG16 Transfer Learning | Logo Dataset | Accuracy: 87% |
| Font Recommender | CNN + KNN | Font Dataset | Top-3 Acc: 91% |
| Color Extractor | KMeans (k=5) | Logo Dataset pixels | Silhouette: 0.68 |
| Campaign KPI | Random Forest Regressor | Marketing Campaign Dataset | RMSE: 0.42 |
| Brand Consistency | Sentence Transformers (SBERT) | Slogan + Startups | Cosine Sim: 0.74 |

---

## 🌍 Deployment (Streamlit Cloud)

1. Push all files to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file as `app.py`
5. Add Gemini API key in **Settings → Secrets**:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
6. Deploy — app will be live at `https://your-app-name.streamlit.app`

---

## 🤝 Contribution Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/module-name`
3. Commit changes: `git commit -m "feat: add [description]"`
4. Push: `git push origin feature/module-name`
5. Submit Pull Request with description of changes

---

## 🏆 Acknowledgments

- [Google Gemini API](https://aistudio.google.com) — Generative AI capabilities
- [Streamlit](https://streamlit.io) — Interactive frontend framework
- [Plotly](https://plotly.com) — Interactive visualizations
- [Hugging Face](https://huggingface.co) — Sentence Transformers
- [scikit-learn](https://scikit-learn.org) — ML model framework
- CRS AI Facilitators & WACP Panel — Academic guidance

---

## 📸 Screenshots / Demo

*Add screenshots of each tab here after deployment*

| Tab | Screenshot |
|-----|-----------|
| Brand Setup | `[image]` |
| Logo & Design | `[image]` |
| Campaign Studio | `[image]` |
| Analytics | `[image]` |

---

## 📄 PRD Document

The full Product Requirements Document is available at: `PRD_BrandSphereAI.pdf`

---

*Built with ❤️ for the CRS AI Capstone 2025–26 | BrandSphere AI Team*
