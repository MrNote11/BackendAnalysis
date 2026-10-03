# BackendAnalysis

An automated financial market analytics and stock intelligence platform built with **Django 5.1**, **TimescaleDB**, **Celery**, and **Jupyter**. The system ingests time-series stock quotes from multiple market data providers, performs technical analysis, schedules automated sync jobs, and generates AI-driven market recommendations.

---

## Key Features

- **Time-Series Market Storage**: Leverages **TimescaleDB** hypertables for optimized financial time-series querying, aggregations, and high-volume quote storage.
- **Multi-Source Market Data Ingestion**: Robust client integrations with **Polygon.io** and **Alpha Vantage** with automated response transformation and batch loading.
- **Automated Task Scheduling**: Asynchronous background quote syncing and batch processing using **Celery**, **Redis**, and **django-celery-beat**.
- **Quantitative Technical Indicators**:
  - Simple & Daily Moving Averages (SMA / DMA)
  - Volume Trends & Price Targets
  - Relative Strength Index (RSI)
- **AI-Powered Decision Engine**: Generative market reasoning and structured recommendations powered by the **OpenAI API**.
- **Jupyter Research Suite**: Comprehensive notebook pipeline (`nbs/`) for data exploration, API experimentation, indicator testing, and algorithmic prototyping.

---

## Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Backend Framework** | Django 5.1 | Web application framework and admin portal |
| **Database** | TimescaleDB (PostgreSQL 15) | Relational + time-series data storage |
| **Task Queue & Broker** | Celery + Redis | Asynchronous job execution and periodic scheduling |
| **Market Data APIs** | Polygon.io & Alpha Vantage | Market quotes, candles, and ticker metadata |
| **AI / LLM** | OpenAI API | Quantitative & natural-language trading recommendations |
| **Data Science / Analysis** | Jupyter Notebooks, Pandas | Interactive analysis and algorithm backtesting |
| **Containerization** | Docker & Docker Compose | Multi-container setup for local TimescaleDB & Redis |

---

## Project Structure

```text
BackendAnalysis/
├── compose.yaml                # Docker Compose config (TimescaleDB & Redis)
├── manage.py                   # Django root management script
├── requirements.txt            # Python dependencies
├── .env.sample                 # Environment configuration template
├── nbs/                        # Jupyter Notebooks for analysis & prototyping
│   ├── 1 - Hello World Load dotenv.ipynb
│   ├── 2 - Hello World Polygon.ipynb
│   ├── 3 - Hello World Alpha Vantage.ipynb
│   ├── 4 - Transform Polygon Response.ipynb
│   ├── 5 - Transform Alpha Vantage Response.ipynb
│   ├── 6 - Polygon API Client.ipynb
│   ├── 7 - Alpha Vantage API Client.ipynb
│   ├── 8 - Django Setup.ipynb
│   ├── 9 - Helper API Clients.ipynb
│   ├── 10 - Load Stock Quotes into Django.ipynb
│   ├── 11 - Batch and Bulk Load Stock Quotes.ipynb
│   ├── 12 - Stock Sync.ipynb
│   ├── Analyze - 1 - Moving Averages.ipynb
│   ├── Analyze - 2 - Daily Moving Averages.ipynb
│   ├── Analyze - 3 - Volume Trend and Price Target.ipynb
│   ├── Analyze - 4 - Analyze Stocks - Relative Strength Index.ipynb
│   ├── Analyze - 5 - Stocks Services.ipynb
│   ├── Decide - 1 - Logic-based Recommendation.ipynb
│   ├── Decide - 2 - LLM-based Recommendation.ipynb
│   └── Putting it all together.ipynb
└── src/                        # Django Application Source
    ├── cfehome/                # Core Django project configuration & settings
    │   ├── celery.py           # Celery application configuration
    │   ├── settings.py         # App settings (TimescaleDB, Redis, Celery)
    │   └── urls.py             # URL routing
    ├── helpers/                # External API client wrappers (Polygon, Alpha Vantage)
    └── market/                 # Stock quotes model, migrations, and analysis services
```

---

## Getting Started

### Prerequisites

- **Python 3.11+** or **3.12**
- **Docker Desktop** (or Docker Engine + Compose)
- **Git**
- API Keys:
  - [Polygon.io API Key](https://polygon.io/)
  - [Alpha Vantage API Key](https://www.alphavantage.co/)
  - [OpenAI API Key](https://platform.openai.com/) (optional, for LLM recommendations)

---

### Installation & Setup

#### 1. Clone the Repository
```bash
git clone git@github.com:MrNote11/BackendAnalysis.git
cd BackendAnalysis
```

#### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```
*(On Windows: `.\venv\Scripts\activate`)*

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Copy `.env.sample` to `.env` and fill in your credentials:
```bash
cp .env.sample .env
```
Edit `.env` to include your API keys and configuration:
```ini
SECRET_KEY="your-secure-secret-key"
DEBUG=True
ALLOWED_HOSTS="localhost,127.0.0.1"

# Database & Cache (matches compose.yaml)
DATABASE_URL="postgresql://postgres:postgres@localhost:5431/postgres"
REDIS_URL="redis://localhost:6878"

# Provider Keys
ALPHA_VANTAGE_API_KEY="your_alpha_vantage_api_key"
POLYGON_API_KEY="your_polygon_api_key"
OPENAI_API_KEY="your_openai_api_key"
```

#### 5. Launch TimescaleDB and Redis Containers
```bash
docker compose up -d
```
This starts:
- **TimescaleDB** on port `5431`
- **Redis** on port `6878`

#### 6. Run Database Migrations
```bash
python manage.py migrate
```

#### 7. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

---

## Running the Application

### Start the Django Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/admin` to access the admin dashboard.

### Run Celery Worker (Asynchronous Tasks)
In a separate terminal (with virtual environment active):
```bash
celery -A cfehome worker -l info
```
*(On Windows: `celery -A cfehome worker -l info --pool=solo`)*

### Run Celery Beat (Periodic Scheduling)
To enable periodic market sync tasks:
```bash
celery -A cfehome beat -l info
```

### Launch Jupyter Notebooks
For research, data transformation, and backtesting:
```bash
jupyter notebook
```
Navigate to the `nbs/` directory to run the analytical notebooks.

---

## Running Analysis Services

You can invoke market analysis routines through Django management shell or custom scripts:

```bash
python manage.py shell
```

```python
from market.services import analyze_stock_symbol
from helpers.clients import get_polygon_client

# Example: Run stock analysis
results = analyze_stock_symbol(symbol="AAPL")
print(results)
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
