# 🚀 OMR Evaluation System


## 📁 Project Structure

```
Innomatics-Hackathon/
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
│
├── frontend/                      # Frontend application
│   ├── app.py                    # Main Streamlit application
│   ├── setup_db.py               # Database initialization script
│   │
│   ├── components/               # Page components
│   │   ├── __init__.py
│   │   ├── dashboard.py          # Dashboard page
│   │   ├── upload.py             # Upload page
│   │   ├── results.py            # Results page
│   │   ├── analytics.py          # Analytics page
│   │   └── audit.py              # Audit page
│   │
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── config.py             # Page config & CSS styling
│       ├── database.py           # Database operations with caching
│       └── navigation.py         # Sidebar navigation
│
├── database/                     # Database layer
│   ├── models.py                 # SQLite models and operations
│   └── omr_system.db            # SQLite database file (auto-generated)
│
├── uploads/                      # File uploads directory
└── venv/                        # Virtual environment (auto-generated)
```

##  Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup Commands

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd Innomatics-Hackathon
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate    
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database (first time only)**
   ```bash
   cd frontend
   python setup_db.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Alternative Run Commands

**From project root:**
```bash
streamlit run frontend/app.py
```

**From frontend directory:**
```bash
cd frontend
streamlit run app.py
```

## � Access

Once running, open your browser to:
```
http://localhost:8501
```

---
