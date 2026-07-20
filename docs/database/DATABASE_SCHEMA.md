# Database Schema

## Purpose And Scope

This document defines the MVP relational database schema for Smart Inquiry AI.

The schema is designed for the first controlled demo implementation. It supports the core inquiry workflow:

1. A customer submits an inquiry.
2. The inquiry is stored with the original customer message.
3. AI output is stored as derived context when available.
4. An outbound notification attempt is recorded.
5. The internal dashboard can review and update inquiry status.

This document is implementation-ready, but it is not application code, a migration file, or an ORM model.

## Database Assumptions

- Database engine: MySQL 8.x.
- Storage engine: InnoDB.
- Character set: `utf8mb4`.
- Collation: `utf8mb4_unicode_ci` or a compatible project-wide default.
- Timestamps are stored in UTC.
- The first demo excludes authentication.
- The internal dashboard is for local or controlled demo use only.
- Real sensitive customer data must not be used in a public deployment until access control is introduced.
- Active MVP entities are limited to Customer, Inquiry, and Notification.
- Attachment is future-ready but inactive and is not included as an active MVP table.

## ID Strategy

Use `BIGINT UNSIGNED AUTO_INCREMENT` primary keys for all MVP tables.

Reason:

- Simple to understand and debug during the MVP.
- Native and efficient in MySQL.
- Avoids UUID formatting, storage, and indexing complexity before the product needs distributed ID generation.
- Keeps all active tables on one consistent ID strategy.

The MVP must not mix UUID and auto-increment ID strategies.

## Table: customers

Purpose: stores the person who submitted an inquiry.

Primary key:

- `id`

### Columns

| Column | Suggested MySQL Type | Nullable | Default | Constraints | Business Reason |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGINT UNSIGNED` | Required | Auto-increment | Primary key | Stable internal identifier for a customer. |
| `name` | `VARCHAR(120)` | Required | None | Not empty at application validation layer | Identifies the person submitting the inquiry. |
| `email` | `VARCHAR(255)` | Required | None | Unique, normalized lowercase by application | Primary contact channel and simple MVP identity key. |
| `phone` | `VARCHAR(50)` | Nullable | `NULL` | None | Optional contact method for businesses that prefer calling. |
| `company` | `VARCHAR(160)` | Nullable | `NULL` | None | Optional business context without creating a CRM account model. |
| `preferred_contact_method` | `ENUM('email', 'phone')` | Required | `'email'` | Must match available MVP contact methods | Helps the team choose the first follow-up channel. |
| `created_at` | `DATETIME(6)` | Required | Current UTC timestamp | None | Records when the customer record was first created. |
| `updated_at` | `DATETIME(6)` | Required | Current UTC timestamp on create and update | None | Records when customer contact details last changed. |

### Unique Constraints

- `uq_customers_email` on `email`

Reason: in the MVP, email is the simplest stable way to associate multiple inquiries with the same customer.

### Customer Identity And Email Handling

- Normalize submitted email before lookup by trimming whitespace and converting it to lowercase.
- Reuse an existing Customer when the normalized email already exists.
- Create a new Customer when the normalized email does not exist.
- Keep the unique email constraint for the MVP.
- When reusing an existing Customer, non-empty submitted `name`, `phone`, and `company` values may update the existing Customer.
- Blank submitted values must not erase existing non-empty Customer values.
- `preferred_contact_method` may update the existing Customer only when the submitted value is non-empty and valid.

### Indexes

- Primary key index on `id`.
- Unique index on `email`.
- Optional non-unique index on `created_at` if customer administration becomes necessary.

## Table: inquiries

Purpose: stores one submitted customer inquiry and its lifecycle state.

Primary key:

- `id`

Foreign keys:

- `customer_id` references `customers.id`

### Columns

| Column | Suggested MySQL Type | Nullable | Default | Constraints | Business Reason |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGINT UNSIGNED` | Required | Auto-increment | Primary key | Stable internal identifier for an inquiry. |
| `customer_id` | `BIGINT UNSIGNED` | Required | None | Foreign key to `customers.id` | Every inquiry must belong to exactly one customer. |
| `inquiry_type` | `VARCHAR(80)` | Nullable | `NULL` | Blank strings normalize to `NULL` | Approved optional MVP field for lightweight dashboard filtering and triage. |
| `budget_range` | `VARCHAR(80)` | Nullable | `NULL` | Blank strings normalize to `NULL` | Approved optional MVP field for customer-provided budget context without pricing logic. |
| `timeline` | `VARCHAR(120)` | Nullable | `NULL` | Blank strings normalize to `NULL` | Approved optional MVP field for customer-provided timing context. |
| `message` | `TEXT` | Required | None | Not empty at application validation layer | Preserves the original submitted inquiry message. |
| `status` | `ENUM('new', 'in_progress', 'completed', 'archived')` | Required | `'new'` | Must use the approved MVP lifecycle | Tracks the business lifecycle of the inquiry. |
| `ai_summary` | `TEXT` | Nullable | `NULL` | None | Stores the AI-generated summary when generation succeeds. |
| `ai_customer_need` | `TEXT` | Nullable | `NULL` | None | Stores the AI-generated interpretation of the customer's need. |
| `ai_urgency` | `ENUM('low', 'medium', 'high', 'unknown')` | Nullable | `NULL` | Must be one of the supported urgency values when present | Gives the dashboard a simple triage signal without adding lead scoring. |
| `ai_missing_information` | `TEXT` | Nullable | `NULL` | None | Captures information the team may need to ask for during follow-up. |
| `ai_suggested_next_action` | `TEXT` | Nullable | `NULL` | None | Gives the reviewer a suggested next step while preserving human judgment. |
| `ai_generated_at` | `DATETIME(6)` | Nullable | `NULL` | None | Records when AI output was generated successfully. |
| `ai_generation_status` | `ENUM('pending', 'succeeded', 'failed')` | Required | `'pending'` | Must reflect current AI generation state | Allows inquiry creation to succeed before AI generation completes. |
| `ai_generation_error` | `TEXT` | Nullable | `NULL` | None | Stores a safe diagnostic message when AI generation fails. |
| `created_at` | `DATETIME(6)` | Required | Current UTC timestamp | None | Records when the inquiry was submitted. |
| `updated_at` | `DATETIME(6)` | Required | Current UTC timestamp on create and update | None | Records when inquiry status or derived context last changed. |

### Indexes

- Primary key index on `id`.
- `idx_inquiries_customer_id` on `customer_id`.
- `idx_inquiries_status_created_at` on `status`, `created_at`.
- `idx_inquiries_created_at` on `created_at`.
- `idx_inquiries_ai_generation_status` on `ai_generation_status`.

Reasons:

- `customer_id` supports customer-to-inquiry lookup.
- `status, created_at` supports the dashboard's primary list view.
- `created_at` supports recency sorting.
- `ai_generation_status` supports finding failed AI generation attempts during review.

## Table: notifications

Purpose: stores a record of an outbound notification attempt associated with an inquiry.

Notification is a communication record. It is not the service responsible for sending email.

Primary key:

- `id`

Foreign keys:

- `inquiry_id` references `inquiries.id`

### Columns

| Column | Suggested MySQL Type | Nullable | Default | Constraints | Business Reason |
| --- | --- | --- | --- | --- | --- |
| `id` | `BIGINT UNSIGNED` | Required | Auto-increment | Primary key | Stable internal identifier for a notification attempt. |
| `inquiry_id` | `BIGINT UNSIGNED` | Required | None | Foreign key to `inquiries.id` | Every notification attempt belongs to one inquiry. |
| `notification_type` | `VARCHAR(80)` | Required | `'new_inquiry'` | Not empty at application validation layer | Identifies why the notification attempt exists without using a single-value enum. |
| `channel` | `VARCHAR(40)` | Required | `'email'` | Not empty at application validation layer | Email is the MVP delivery channel; other channels can be added later without changing a single-value enum. |
| `recipient` | `VARCHAR(255)` | Required | None | Not empty at application validation layer | Records who the notification was addressed to. |
| `delivery_status` | `ENUM('pending', 'sent', 'failed')` | Required | `'pending'` | Must match supported delivery states | Tracks whether the outbound attempt succeeded or failed. |
| `provider_name` | `VARCHAR(80)` | Nullable | `NULL` | None | Records the external email provider name when known. |
| `provider_message_id` | `VARCHAR(255)` | Nullable | `NULL` | Unique with `provider_name` when present | Helps trace or de-duplicate provider-level delivery records. |
| `error_message` | `TEXT` | Nullable | `NULL` | None | Stores a safe diagnostic message when delivery fails. |
| `attempted_at` | `DATETIME(6)` | Nullable | `NULL` | None | Records when the outbound attempt was made. |
| `sent_at` | `DATETIME(6)` | Nullable | `NULL` | None | Records when the email provider accepted the message request. |
| `created_at` | `DATETIME(6)` | Required | Current UTC timestamp | None | Records when the notification record was created. |
| `updated_at` | `DATETIME(6)` | Required | Current UTC timestamp on create and update | None | Records when delivery state last changed. |

### Unique Constraints

- `uq_notifications_provider_message` on `provider_name`, `provider_message_id`

Reason: prevents duplicate records for the same provider message when provider identifiers are available. MySQL allows multiple `NULL` values in unique indexes, so local pending or failed records without a provider ID remain valid.

### Indexes

- Primary key index on `id`.
- `idx_notifications_inquiry_id` on `inquiry_id`.
- `idx_notifications_delivery_status` on `delivery_status`.
- `idx_notifications_created_at` on `created_at`.

Reasons:

- `inquiry_id` supports inquiry detail notification history.
- `delivery_status` supports reviewing failed or pending notification attempts.
- `created_at` supports chronological audit views.

## Status Enum Definitions

### Inquiry Status

Use lowercase database values that map directly to the repository-approved lifecycle:

| Database Value | Product Label | Meaning |
| --- | --- | --- |
| `new` | New | Inquiry has been submitted and has not yet been actively handled. |
| `in_progress` | In Progress | Inquiry is being reviewed or followed up. |
| `completed` | Completed | Inquiry has reached a useful end state for the MVP workflow. |
| `archived` | Archived | Inquiry is retained for history but no longer active. |

## AI Output Contract

Selected MVP fields:

- `ai_summary`
- `ai_customer_need`
- `ai_urgency`
- `ai_missing_information`
- `ai_suggested_next_action`
- `ai_generated_at`
- `ai_generation_status`
- `ai_generation_error`

These fields are stored on `inquiries` because AI output is derived context for reviewing an inquiry, not a separate MVP business object.

Fields intentionally not included:

- `potential_value`: excluded from the approved MVP AI output contract.
- AI prompt metadata: useful later, but not necessary for the first demo.
- AI provider response JSON: avoided to keep the schema simple and queryable.

## AI Failure Behavior

Inquiry creation must succeed even when AI generation fails.

Rules:

- Create the customer record first when needed.
- Create the inquiry record with original submitted data.
- Customer lookup or creation and Inquiry creation must occur in one database transaction.
- Customer lookup or creation and Inquiry creation must either both succeed or both roll back.
- Commit the Customer and Inquiry transaction before starting AI generation or email notification.
- Attempt AI generation only after the Customer and Inquiry transaction has committed.
- If AI generation succeeds, store the selected AI output fields and set `ai_generation_status` to `succeeded`.
- If AI generation fails, keep AI output fields `NULL`, set `ai_generation_status` to `failed`, and store a safe `ai_generation_error`.
- AI failure must never roll back the stored Inquiry.
- Do not overwrite `message` or any original customer input with AI-generated text.

### AI Generation State Transitions

- `pending` -> `succeeded`
- `pending` -> `failed`

Every MVP Inquiry is expected to trigger AI generation. No optional AI execution state is included because current approved MVP documentation does not require optional AI execution.

## Inquiry Submission Transaction Rule

The initial inquiry submission storage flow must use a database transaction for only the Customer and Inquiry write path:

1. Normalize submitted email.
2. Look up an existing Customer by normalized email.
3. Create or update the Customer according to the Customer identity rules.
4. Create the Inquiry associated with that Customer.
5. Commit the transaction.

If any Customer or Inquiry write fails before commit, both must roll back.

After commit:

- AI generation may run and update AI output fields.
- Email notification may run and create or update Notification records.
- AI failure must not roll back the stored Inquiry.
- Email notification failure must not roll back the stored Inquiry.

## Notification Delivery Status Definitions

| Database Value | Meaning |
| --- | --- |
| `pending` | Notification record exists, but delivery has not completed yet. |
| `sent` | Email provider accepted the message request. This does not guarantee final recipient delivery. |
| `failed` | Delivery attempt failed or provider returned an error. |

Email is the only active MVP delivery channel. Additional channels such as LINE or Slack are future expansion items.

The MVP does not include delivery webhooks, final recipient delivery tracking, `delivered_at`, retries, queues, or background worker tables.

## Timestamp Strategy

- Use UTC for all timestamps.
- Use `DATETIME(6)` for timestamp columns.
- Use `created_at` on every active table.
- Use `updated_at` on every active table.
- Use domain-specific timestamps only when they describe a meaningful business or integration event:
  - `ai_generated_at`
  - `attempted_at`
  - `sent_at`

## Data Integrity Rules

- Every Inquiry must belong to exactly one Customer.
- A Customer may exist without any Inquiry.
- Every Notification must belong to exactly one Inquiry.
- A Notification cannot exist without an associated Inquiry.
- AI-generated information must never replace the customer's original submission.
- Inquiry creation must not depend on AI generation success.
- Attachment cannot be implemented as an active MVP table.
- Deleting customers or inquiries should be restricted while dependent records exist.
- Use the `archived` inquiry status instead of soft deletion for MVP history retention.

## Foreign Keys And Deletion Rules

| Relationship | Foreign Key | Delete Rule | Reason |
| --- | --- | --- | --- |
| Customer to Inquiry | `inquiries.customer_id` -> `customers.id` | `RESTRICT` | Prevents orphaned inquiry records and preserves customer submission history. |
| Inquiry to Notification | `notifications.inquiry_id` -> `inquiries.id` | `RESTRICT` | Prevents orphaned notification history. |

The MVP should avoid hard deletion flows. If an inquiry should no longer appear as active, use `status = 'archived'`.

## Explicit Out-Of-Scope Items

The MVP schema must not include:

- `attachments` as an active table
- Attachment upload fields on active MVP tables
- `organization_id`
- `workspace_id`
- Billing or subscription tables
- Assignment or owner fields
- Tags
- Workflow engine tables
- Authentication or permission tables
- User accounts
- Multi-tenant infrastructure concepts
- Event sourcing tables
- Message broker or queue tables
- Separate AI business domain tables
- Separate notification service tables beyond the notification attempt record
