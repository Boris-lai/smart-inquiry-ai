# API Contract

## Purpose And Scope

This document defines the MVP REST API contract for Smart Inquiry AI.

The API supports the approved MVP product flow:

1. Customer submits an inquiry.
2. Customer lookup or creation and Inquiry creation are stored transactionally.
3. AI generation occurs after the initial database transaction commits.
4. Notification processing occurs after the initial database transaction commits.
5. Internal dashboard can list, view, and update Inquiry status.

This document is not application code, router code, request schema code, tests, or migration code.

## API Conventions

### Base Path

All MVP endpoints use:

```text
/api/v1
```

### Content Type

- Requests with a body must use `Content-Type: application/json`.
- Responses return `Content-Type: application/json`.

### Date And Time Format

- API timestamps use UTC ISO 8601 strings.
- Example: `2026-07-20T08:30:00Z`

### ID Format

- Database IDs are `BIGINT` integers.
- API path IDs and response IDs are represented as JSON numbers.
- Clients must not assume IDs are globally unique outside this system.

### Naming Conventions

- JSON field names use `snake_case`.
- Status values use lowercase strings.
- Public request fields must not include internal fields such as `status`, AI output, `customer_id`, notification state, `created_at`, or `updated_at`.

## Endpoint Summary

| Method | Path | Audience | Purpose |
| --- | --- | --- | --- |
| `POST` | `/api/v1/inquiries` | Public | Submit a new inquiry. |
| `GET` | `/api/v1/inquiries` | Internal dashboard | List inquiries for dashboard review. |
| `GET` | `/api/v1/inquiries/{inquiry_id}` | Internal dashboard | View one inquiry in detail. |
| `PATCH` | `/api/v1/inquiries/{inquiry_id}/status` | Internal dashboard | Update only the inquiry status. |
| `GET` | `/api/v1/health` | Operational | Minimal health check. |

Internal dashboard endpoints are internal-only for the controlled demo. They are unsafe for public production deployment until access control is introduced.

## POST /api/v1/inquiries

Submits a new public inquiry.

### Request Body

```json
{
  "name": "Alex Chen",
  "email": " Alex@example.com ",
  "phone": "+886912345678",
  "company": "Northstar Studio",
  "preferred_contact_method": "email",
  "inquiry_type": "website redesign",
  "budget_range": "100000-200000 TWD",
  "timeline": "within 2 months",
  "message": "We need help redesigning our company website and improving inquiry conversion."
}
```

### Required Fields

- `name`
- `email`
- `message`

These are required because the approved MVP scope includes customer contact details and request description, and no repository document says they should be optional.

### Optional Fields

- `phone`
- `company`
- `preferred_contact_method`
- `inquiry_type`
- `budget_range`
- `timeline`

`preferred_contact_method` defaults to `email`.

`inquiry_type`, `budget_range`, and `timeline` are approved optional MVP fields.

### Field Rules

| Field | Type | Required | Max Length | Normalization | Notes |
| --- | --- | --- | --- | --- | --- |
| `name` | string | Yes | 120 | Trim whitespace | Must not be blank. |
| `email` | string | Yes | 255 | Trim whitespace and lowercase | Must be a valid email format. Used for Customer lookup. |
| `phone` | string or null | No | 50 | Blank string to `null` | Optional contact detail. |
| `company` | string or null | No | 160 | Blank string to `null` | Optional business context. |
| `preferred_contact_method` | string | No | N/A | Default to `email` | Allowed values: `email`, `phone`. |
| `inquiry_type` | string or null | No | 80 | Blank string to `null` | Approved optional MVP field. |
| `budget_range` | string or null | No | 80 | Blank string to `null` | Approved optional MVP field. |
| `timeline` | string or null | No | 120 | Blank string to `null` | Approved optional MVP field. |
| `message` | string | Yes | 10000 | Preserve original content after boundary validation | Must not be blank. AI must never overwrite it. |

### Cross-Field Contact Validation

- When `preferred_contact_method` is `phone`, `phone` must contain a non-blank valid value.
- If `preferred_contact_method` is `phone` and `phone` is missing, `null`, or blank, return `422 validation_error`.
- The field-level error should identify `phone`.
- When `preferred_contact_method` is omitted, it defaults to `email`.
- Do not require `phone` when `preferred_contact_method` is `email`.

Example error detail:

```json
{
  "error": {
    "code": "validation_error",
    "message": "One or more fields are invalid.",
    "details": [
      {
        "field": "phone",
        "message": "Phone is required when preferred contact method is phone."
      }
    ]
  }
}
```

### Not Allowed In Request

The public client must not submit:

- `id`
- `customer_id`
- `status`
- AI fields
- notification fields
- `created_at`
- `updated_at`

The public client cannot choose the Inquiry status. New submissions always start as `new`.

### Storage Behavior

Customer lookup or creation and Inquiry creation must occur in one database transaction.

1. Normalize email by trimming whitespace and converting it to lowercase.
2. Look up Customer by normalized email.
3. Reuse an existing Customer when found.
4. Create a new Customer when not found.
5. Non-empty submitted `name`, `phone`, and `company` may update an existing Customer.
6. Blank submitted optional values must not erase existing non-empty Customer values.
7. Create the Inquiry with `status = "new"` and `ai_generation_status = "pending"`.
8. Commit the transaction.

AI generation and notification processing happen only after this transaction commits. AI or email failure must never roll back the stored Inquiry.

### Response Behavior

The MVP prefers a synchronous response that confirms storage without waiting for AI or email completion.

The response succeeds once the Customer and Inquiry transaction commits.

AI or notification failure after storage must not turn the successful submission response into a failed inquiry submission. Public responses must not expose AI diagnostic errors or email provider errors.

### Success Response

Status: `201 Created`

```json
{
  "inquiry_id": 101,
  "status": "new",
  "ai_generation_status": "pending",
  "message": "Your inquiry was received successfully."
}
```

### HTTP Status Codes

| Status | Meaning |
| --- | --- |
| `201` | Inquiry was stored successfully. |
| `400` | Malformed JSON or semantically invalid request outside field validation. |
| `422` | Structurally valid JSON with field validation failures. |
| `500` | Unexpected server error. |

## GET /api/v1/inquiries

Lists inquiries for the internal dashboard.

This endpoint is internal-only for local or controlled demo use. It must not be exposed publicly in production until access control exists.

### Query Parameters

| Parameter | Type | Required | Default | Rules |
| --- | --- | --- | --- | --- |
| `page` | integer | No | `1` | Minimum `1`. |
| `page_size` | integer | No | `20` | Minimum `1`, maximum `100`. |
| `status` | string | No | None | One of `new`, `in_progress`, `completed`, `archived`. |
| `ai_generation_status` | string | No | None | One of `pending`, `succeeded`, `failed`. Optional for MVP support triage of failed AI output. |
| `sort` | string | No | `-created_at` | MVP supports `created_at` and `-created_at`; default newest first. |

### Filtering

- `status` filters by Inquiry lifecycle state.
- `ai_generation_status` is justified for MVP because AI failure is allowed and dashboard review may need to identify inquiries without AI output.

### Sorting

- Default sorting is newest first: `-created_at`.
- `created_at` sorts oldest first.
- Unsupported sort values return `400`.

### Pagination

Use page-based pagination.

- `page`: current page number.
- `page_size`: number of items per page.
- Response includes `total`, `page`, `page_size`, and `has_next`.

### Compact List Item

List items should be compact and must not include full message text, full AI analysis, notification history, provider errors, or internal diagnostics.

### Success Response

Status: `200 OK`

```json
{
  "items": [
    {
      "id": 101,
      "status": "new",
      "inquiry_type": "website redesign",
      "customer": {
        "name": "Alex Chen",
        "email": "alex@example.com",
        "company": "Northstar Studio"
      },
      "ai_generation_status": "pending",
      "ai_summary_preview": null,
      "created_at": "2026-07-20T08:30:00Z",
      "updated_at": "2026-07-20T08:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 1,
    "has_next": false,
    "sort": "-created_at"
  }
}
```

### Empty Result Response

Status: `200 OK`

```json
{
  "items": [],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 0,
    "has_next": false,
    "sort": "-created_at"
  }
}
```

### HTTP Status Codes

| Status | Meaning |
| --- | --- |
| `200` | List returned successfully, including empty lists. |
| `400` | Unsupported query parameter value such as invalid sort. |
| `422` | Field validation failure for query parameters. |
| `500` | Unexpected server error. |

## GET /api/v1/inquiries/{inquiry_id}

Returns one inquiry detail for the internal dashboard.

This endpoint is internal-only for local or controlled demo use. It must not be exposed publicly in production until access control exists.

### Path Parameters

| Parameter | Type | Required | Rules |
| --- | --- | --- | --- |
| `inquiry_id` | integer | Yes | Must be a positive BIGINT-compatible integer. |

### Success Response

Status: `200 OK`

```json
{
  "id": 101,
  "status": "new",
  "inquiry_type": "website redesign",
  "budget_range": "100000-200000 TWD",
  "timeline": "within 2 months",
  "message": "We need help redesigning our company website and improving inquiry conversion.",
  "customer": {
    "id": 12,
    "name": "Alex Chen",
    "email": "alex@example.com",
    "phone": "+886912345678",
    "company": "Northstar Studio",
    "preferred_contact_method": "email"
  },
  "ai": {
    "generation_status": "succeeded",
    "summary": "Customer needs a company website redesign focused on inquiry conversion.",
    "customer_need": "Website redesign and conversion improvement.",
    "urgency": "medium",
    "missing_information": "Current website URL and target launch date.",
    "suggested_next_action": "Ask for the current website URL and schedule a discovery call.",
    "generated_at": "2026-07-20T08:30:10Z"
  },
  "notifications": [
    {
      "id": 501,
      "notification_type": "new_inquiry",
      "channel": "email",
      "recipient": "owner@example.com",
      "delivery_status": "sent",
      "provider_name": "resend",
      "provider_message_id": "msg_123",
      "error_message": null,
      "attempted_at": "2026-07-20T08:30:12Z",
      "sent_at": "2026-07-20T08:30:13Z",
      "created_at": "2026-07-20T08:30:12Z",
      "updated_at": "2026-07-20T08:30:13Z"
    }
  ],
  "created_at": "2026-07-20T08:30:00Z",
  "updated_at": "2026-07-20T08:30:13Z"
}
```

### Data Exposure Rules

The detail response may include customer contact information, original message, AI-derived review context, notification attempt history, and timestamps.

It must not expose:

- raw provider payloads
- secrets
- stack traces
- SQL errors
- unsafe internal diagnostics
- internal exception class names
- environment values

### Not Found Behavior

If no Inquiry exists for `inquiry_id`, return `404` using the standard error envelope.

### HTTP Status Codes

| Status | Meaning |
| --- | --- |
| `200` | Inquiry returned successfully. |
| `404` | Inquiry not found. |
| `422` | Invalid path parameter format. |
| `500` | Unexpected server error. |

## PATCH /api/v1/inquiries/{inquiry_id}/status

Updates only the Inquiry status.

This endpoint is internal-only for local or controlled demo use. It must not be exposed publicly in production until access control exists.

### Path Parameters

| Parameter | Type | Required | Rules |
| --- | --- | --- | --- |
| `inquiry_id` | integer | Yes | Must be a positive BIGINT-compatible integer. |

### Request Body

```json
{
  "status": "in_progress"
}
```

### Allowed Status Values

- `new`
- `in_progress`
- `completed`
- `archived`

### Status Transition Rules

Repository documentation does not define a stricter workflow. The MVP uses a simple rule:

- Any allowed status may transition to any other allowed status.
- Updating to the current status is idempotent and returns `200 OK`.
- The endpoint changes only `status` and `updated_at`.

The endpoint must not update customer data, inquiry message, AI output, or notification records.

### Success Response

Status: `200 OK`

```json
{
  "id": 101,
  "status": "in_progress",
  "updated_at": "2026-07-20T09:15:00Z"
}
```

### HTTP Status Codes

| Status | Meaning |
| --- | --- |
| `200` | Status updated or already matched the requested status. |
| `400` | Semantically invalid request outside field validation. |
| `404` | Inquiry not found. |
| `409` | Real resource state conflict if a future rule prohibits a transition. |
| `422` | Field validation failure. |
| `500` | Unexpected server error. |

## GET /api/v1/health

Returns a minimal health response.

This endpoint must not expose infrastructure secrets or detailed dependency diagnostics.

### Success Response

Status: `200 OK`

```json
{
  "status": "ok"
}
```

### HTTP Status Codes

| Status | Meaning |
| --- | --- |
| `200` | API process can respond. |
| `500` | Unexpected server error. |

## AI Behavior

- Every MVP Inquiry starts with `ai_generation_status = "pending"`.
- AI generation starts only after Customer and Inquiry storage commits.
- Successful AI generation updates the AI output fields and sets `ai_generation_status = "succeeded"`.
- Failed AI generation leaves AI output fields empty or unchanged, stores a safe internal error in the database, and sets `ai_generation_status = "failed"`.
- Public submission responses must not expose AI provider errors or diagnostic messages.
- AI failure must never roll back a stored Inquiry.

## Notification Behavior

- Notification processing starts only after Customer and Inquiry storage commits.
- Notification records represent outbound notification attempts.
- Email is the only MVP delivery channel.
- `sent` means the email provider accepted the message request. It does not guarantee final recipient delivery.
- Email provider errors may be stored internally but must not be exposed to the public submission response.
- Notification failure must never roll back a stored Inquiry.
- The MVP does not include retries, queues, delivery webhooks, or notification retry endpoints.

## Data Exposure Rules

- Public inquiry submission responses are intentionally minimal.
- Internal dashboard endpoints may expose customer contact information and original inquiry messages.
- Internal dashboard endpoints are unsafe for public production deployment without access control.
- Public responses must not leak AI errors, email provider errors, SQL errors, stack traces, secrets, environment values, or internal exception names.
- The API does not support hard deletion in the MVP.

## Explicit Out-Of-Scope Items

The MVP API does not include:

- Authentication endpoints
- User endpoints
- Customer administration endpoints
- Notification retry endpoints
- AI retry endpoints
- Delete endpoints
- Analytics endpoints
- Billing endpoints
- Generic CRUD endpoints
- Attachment upload endpoints
- File endpoints
- Organization or workspace endpoints
- Role or permission endpoints
- Webhook endpoints
- Queue or worker management endpoints
