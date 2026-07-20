# Smart Inquiry AI - System Architecture

> Version: v1.0
> Status: MVP specification freeze

## System Overview

```text
                     Smart Inquiry AI

 Customer
    |
    v
+-------------------+
| Inquiry Form      |
| (Next.js planned) |
+---------+---------+
          |
          | POST /api/v1/inquiries
          v
+------------------------------+
| FastAPI Backend              |
|------------------------------|
| - Input Validation           |
| - Business Rules             |
| - Database Transaction       |
| - AI Coordination            |
| - Email Coordination         |
+----+--------------+----------+
     |              |
     |              |
     v              v
+---------+    +----------------------+
| MySQL   |    | External AI Provider |
+---------+    +----------------------+
     |
     v
+---------------------+
| Notification Record |
+---------------------+
     |
     v
External Email Provider

                 ^
                 |
         GET / PATCH /api/v1/inquiries
                 |
+----------------+----------------+
| Internal Dashboard              |
| Local or controlled demo only   |
+---------------------------------+
```

The internal dashboard is not safe for public production deployment until access control is introduced.

## Approved Relationships

```text
Customer (1)
    |
    v
Inquiry (many)
    |
    v
Notification (many)
```

- Customer has a 1-to-many relationship with Inquiry.
- Inquiry has a 1-to-many relationship with Notification.
- AI output is stored as derived information on Inquiry for the MVP.
- Notification is a database record of an outbound notification attempt, not the email delivery service itself.

## Public Inquiry Request Flow

```text
1. Public inquiry request reaches FastAPI.
2. Validate input.
3. Begin database transaction.
4. Normalize customer email.
5. Find, create, or update Customer.
6. Create Inquiry with:
   - status = new
   - ai_generation_status = pending
7. Commit the Customer and Inquiry transaction.
8. Confirm successful storage with 201 Created.
9. AI generation occurs only after the transaction commits.
10. Email notification occurs only after the transaction commits.
11. AI or notification failure must never roll back the stored Inquiry.
```

The public response does not wait for AI generation or email delivery to complete.

## Internal Dashboard Flow

```text
Dashboard
    |
    | GET /api/v1/inquiries
    | GET /api/v1/inquiries/{inquiry_id}
    | PATCH /api/v1/inquiries/{inquiry_id}/status
    v
FastAPI Backend
    |
    v
MySQL
```

The dashboard can list inquiries, view inquiry details, review AI-derived context, inspect notification attempts, and update inquiry status.

## MVP Scope

Included:

- Public inquiry form
- Inquiry storage
- Customer lookup or creation
- AI output using the approved MVP contract
- Email notification attempt record
- Internal dashboard
- Inquiry status update

Not included:

- CRM
- Billing
- Organization or workspace model
- Authentication for the first controlled demo
- Attachment upload
- Workflow engine
- SaaS multi-tenancy
- Queues
- Workers
- Microservices
- Redis
- Kafka
- Event buses
- Distributed systems

## Future Roadmap

```text
MVP
 |
 v
Inquiry Management
 |
 v
CRM
 |
 v
Workflow Automation
 |
 v
Multi-tenant SaaS
```
