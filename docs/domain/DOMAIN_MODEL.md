# Domain Model

This document defines the first version of the core Smart Inquiry AI domain model.

The goal is to clarify responsibility boundaries. This is not a database schema and does not define tables, columns, indexes, or storage technology.

The MVP should remain intentionally small. This document does not introduce Team, Organization, Workspace, Role, Permission, Subscription, or Billing domains.

## Domain Overview

The active MVP domains are:

- Inquiry
- Customer
- Notification

These domains support the first complete product workflow: a customer submits an inquiry, the team receives useful context, and the inquiry becomes trackable.

Attachment is a future-ready inactive domain. It must not be implemented in the initial MVP.

## Inquiry

An Inquiry represents a customer request submitted to the business.

### Responsibility

The Inquiry domain is responsible for the business meaning and lifecycle of a request.

It should describe:

- What the customer is asking for
- The original message or request details
- Current business lifecycle status
- Derived information associated with the inquiry
- Relationship to customer information
- Whether the request is still active, completed, or archived

### Example Information

- Inquiry title or short description
- Inquiry type
- Message content
- Budget range
- Timeline
- Status
- Created time
- Updated time

AI-generated content, such as summaries or suggested next actions, should be treated as derived information associated with an Inquiry. It should not define the Inquiry domain itself and should not make the domain dependent on a specific AI implementation.

### Derived AI Information

Initial MVP AI output contract:

- summary
- customer_need
- urgency
- missing_information
- suggested_next_action

AI generation failure must never prevent an Inquiry from being created.

### Lifecycle

Initial statuses:

- New
- In Progress
- Completed
- Archived

The Inquiry should remain the central object in the MVP.

## Customer

A Customer represents the person or organization that submitted an inquiry.

### Responsibility

The Customer domain is responsible for contact identity and relationship context.

It should describe:

- Who submitted the inquiry
- How the team can contact them
- Whether they represent a company
- Their relationship to one or more inquiries
- Future CRM context when the product expands

### Example Information

- Name
- Email
- Phone
- Company
- Preferred contact method
- Source channel

### Notes

In the MVP, Customer can stay simple. It does not need to become a full CRM profile yet.

In later phases, Customer may expand to include:

- Interaction history
- Notes
- Tags
- Owner assignment
- Related opportunities
- Account-level information

## Future Domain: Attachment

An Attachment represents a file or external asset submitted with an inquiry.

### Responsibility

The Attachment domain is responsible for connecting supporting materials to an inquiry.

It should describe:

- What file or asset was submitted
- Which inquiry it belongs to
- Basic file metadata
- Whether the file is available for internal review
- Future processing or analysis state

### Example Information

- File name
- File type
- File size
- Storage reference
- Related inquiry
- Uploaded time

### Notes

Attachment upload is outside the initial MVP.

No Attachment model, table, API endpoint, form field, storage integration, or processing flow should be implemented during the initial MVP.

Attachment may become active in a later phase when file handling is intentionally designed.

Future versions may support:

- AI-assisted document review
- Image or PDF summarization
- Virus scanning
- File preview
- External file storage integration

## Notification

A Notification represents a record of an outbound notification attempt associated with an Inquiry.

### Responsibility

The Notification domain is responsible for notification history and delivery state around important inquiry events.

Email is the initial delivery channel. LINE, Slack, and similar tools may become additional delivery channels later. Delivery channels should not define the Notification domain itself.

It should describe:

- What event triggered the notification
- Who should receive it
- Which inquiry it relates to
- Delivery status
- Delivery channel
- When it was created, attempted, or sent

### Example Information

- Notification type
- Recipient
- Channel
- Related inquiry
- Delivery status
- Sent time
- Error message when delivery fails

### Initial Notification Triggers

- New inquiry received
- Notification delivery failed

Future notification triggers may include:

- Follow-up reminder
- Status changed
- Assignment changed
- High-priority inquiry detected

## Domain Relationships

### Inquiry And Customer

An Inquiry is submitted by a Customer.

A Customer may have one or more Inquiries over time.

### Future Inquiry And Attachment

In a later phase, an Inquiry may include zero or more Attachments.

An Attachment would belong to one Inquiry.

### Inquiry And Notification

An Inquiry may trigger one or more Notifications.

A Notification is tied to an outbound notification attempt for a specific Inquiry.

## Domain Rules

- Every Inquiry must belong to exactly one Customer.
- A Customer may exist without any Inquiry.
- In a future file upload phase, an Attachment cannot exist without an Inquiry.
- A Notification cannot exist without an associated Inquiry.
- AI-generated information should never replace the customer's original submission.
- AI generation failure must never prevent an Inquiry from being created.

## Domain Principles

- Keep Inquiry as the center of the MVP.
- Keep Customer lightweight until CRM features are introduced.
- Store original customer input separately from AI-generated interpretation.
- Treat Attachments as future supporting context, not MVP inquiry data.
- Treat Notifications as records of communication attempts, not just side effects.
- Avoid database design until domain responsibilities are clear.
