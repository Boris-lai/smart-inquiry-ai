# Error Format

## Purpose And Scope

This document defines the standard JSON error envelope for the Smart Inquiry AI MVP API.

The API should use one consistent shape for validation errors, not-found errors, conflicts, unsupported status transitions, and internal server errors.

## Error Envelope

```json
{
  "error": {
    "code": "validation_error",
    "message": "One or more fields are invalid.",
    "details": [
      {
        "field": "email",
        "message": "Enter a valid email address."
      }
    ]
  }
}
```

## Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `error.code` | Yes | Machine-readable error code. |
| `error.message` | Yes | Human-readable safe message. |
| `error.details` | No | Field-level validation details or safe contextual details. |

`request_id` or `correlation_id` is intentionally not required for the MVP. It can be added later when request logging and production observability are introduced.

## Field Detail Naming

Field-level error details must use public API names:

- Body fields use the public JSON field name, for example `email`.
- Query parameters use the public parameter name, for example `page_size`.
- Path parameters use the public parameter name, for example `inquiry_id`.
- Nested fields use dot notation, for example `customer.email`.
- Field names use `snake_case`.
- Framework-specific location prefixes such as `body`, `query`, and `path` must not appear in public error responses.

## Do Not Expose

Error responses must not expose:

- stack traces
- SQL errors
- provider API errors
- environment values
- secrets
- internal exception class names
- raw external provider payloads

## Framework Integration Requirements

- FastAPI's default validation response must not be returned directly.
- Request body, query parameter, and path parameter validation errors must be converted into the project's standard error envelope.
- Malformed JSON must also use the standard error envelope.
- Application-generated not-found errors must use the standard error envelope.
- Unexpected exceptions must be logged internally and return only the safe generic `500` response.
- Error messages must not be copied directly from database, framework, AI provider, or email provider exception text.
- All API error responses use `Content-Type: application/json`.

## HTTP Status Codes

| Status | Use |
| --- | --- |
| `200` | Successful read or update. |
| `201` | Successful inquiry submission after Customer and Inquiry transaction commits. |
| `400` | Malformed JSON or semantically invalid request that does not fit field validation. |
| `404` | Resource not found. |
| `409` | Real resource state conflict, including future unsupported status transitions. |
| `422` | Request body, query parameter, or path parameter validation failure. |
| `500` | Unexpected server error with a safe generic message. |

## Error Codes

| Code | HTTP Status | Meaning |
| --- | --- | --- |
| `bad_request` | `400` | Request is malformed or semantically invalid outside field validation. |
| `validation_error` | `422` | One or more request body, query, or path fields failed validation. |
| `not_found` | `404` | Requested resource does not exist. |
| `conflict` | `409` | Request conflicts with current resource state. |
| `unsupported_status_transition` | `409` | Status transition is blocked by a business rule. |
| `internal_server_error` | `500` | Unexpected server failure. |

## Bad Request Example

Status: `400 Bad Request`

```json
{
  "error": {
    "code": "bad_request",
    "message": "The request body could not be processed."
  }
}
```

Malformed JSON should return this response rather than FastAPI's default validation response.

## Validation Error Example

Status: `422 Unprocessable Entity`

```json
{
  "error": {
    "code": "validation_error",
    "message": "One or more fields are invalid.",
    "details": [
      {
        "field": "name",
        "message": "Name is required."
      },
      {
        "field": "email",
        "message": "Enter a valid email address."
      },
      {
        "field": "message",
        "message": "Message is required."
      }
    ]
  }
}
```

## Not Found Error Example

Status: `404 Not Found`

```json
{
  "error": {
    "code": "not_found",
    "message": "Inquiry was not found."
  }
}
```

## Conflict Error Example

Status: `409 Conflict`

```json
{
  "error": {
    "code": "unsupported_status_transition",
    "message": "The requested status transition is not allowed."
  }
}
```

The current MVP allows any status to transition to any other allowed status. This error shape is reserved for a future stricter workflow or another real resource state conflict.

## Internal Server Error Example

Status: `500 Internal Server Error`

```json
{
  "error": {
    "code": "internal_server_error",
    "message": "Something went wrong. Please try again later."
  }
}
```

## Important Behavior Rules

1. Customer lookup or creation and Inquiry creation occur in one database transaction.
2. `POST /api/v1/inquiries` succeeds once that transaction commits.
3. AI generation and notification happen after commit.
4. AI or notification failure must not roll back the Inquiry.
5. Public responses must not leak AI errors or email provider errors.
6. Database IDs are BIGINT integers.
7. Timestamps use UTC ISO 8601 strings in API responses.
8. The API does not support hard deletion in the MVP.
9. Authentication is out of scope for the controlled demo.
10. Dashboard endpoints are internal-only and unsafe for public production deployment without access control.

## Public Submission Error Behavior

If the Customer and Inquiry transaction commits, public submission should return `201 Created` even if later AI or notification processing fails.

The public client should receive only a safe confirmation message and processing state. It must not receive AI diagnostic errors, email provider errors, SQL errors, stack traces, or internal exception names.
