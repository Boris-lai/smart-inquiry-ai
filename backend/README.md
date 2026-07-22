# Smart Inquiry AI Backend

FastAPI backend foundation for the Smart Inquiry AI MVP.

## Implemented

- FastAPI application foundation
- Versioned health endpoint at `GET /api/v1/health`
- Typed application settings
- Synchronous SQLAlchemy session foundation
- Customer, Inquiry, and Notification ORM models
- Alembic configuration and initial MySQL schema migration
- Pydantic API schema contracts for the approved MVP inquiry workflow
- Standard API error envelope and FastAPI exception handling foundation
- Public inquiry submission endpoint at `POST /api/v1/inquiries`
- Transactional Customer lookup/create/update and Inquiry storage

Not implemented yet:

- AI generation
- Email notifications
- Notification record creation
- Dashboard behavior

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

Submit a public inquiry:

```text
POST /api/v1/inquiries
```

The endpoint validates the approved public request, matches existing Customers
by normalized lowercase email, updates allowed Customer fields, creates one
Inquiry, and commits Customer plus Inquiry changes in one transaction.

The success response is returned immediately after storage commits:

```json
{
  "inquiry_id": 101,
  "status": "new",
  "ai_generation_status": "pending",
  "message": "Your inquiry was received successfully."
}
```

AI generation and email notification are not implemented yet, and no
Notification record is created by this endpoint during Day 7.

## Database Models

Current active MVP models:

- `Customer`
- `Inquiry`
- `Notification`

Attachment is documented as a future domain only and is not implemented.

The schema uses MySQL-oriented SQLAlchemy metadata:

- `BIGINT UNSIGNED AUTO_INCREMENT` primary keys
- `DATETIME(6)` timestamp columns
- MySQL `ENUM` columns for approved states
- `RESTRICT` foreign-key delete behavior

## Alembic

Alembic reads `DATABASE_URL` through the backend settings object. The local
example value in `.env.example` is not a production secret.

Show migration history:

```bash
alembic history
```

Generate a future revision after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

Apply migrations when MySQL is available:

```bash
alembic upgrade head
```

Downgrade one revision:

```bash
alembic downgrade -1
```

Generate offline SQL without connecting to MySQL:

```bash
alembic upgrade head --sql
```

## Test

```bash
pytest
```

The current test suite validates health, model metadata, migration metadata,
Pydantic schema behavior, standard API error handling, and the public inquiry
submission vertical slice.

Run Ruff:

```bash
ruff check .
```

A real MySQL database with migrations applied is required for manual
end-to-end persistence testing.
