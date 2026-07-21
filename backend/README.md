# Smart Inquiry AI Backend

FastAPI backend foundation for the Smart Inquiry AI MVP.

## Local Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

The example database URL is for local development only:

```text
mysql+pymysql://smart_inquiry:smart_inquiry@localhost:3306/smart_inquiry_ai
```

## Run

```bash
uvicorn app.main:app --reload
```

Health check:

```text
GET /api/v1/health
```

## Test

```bash
pytest
```

