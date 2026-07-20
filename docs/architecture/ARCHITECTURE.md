# Architecture

## High-Level Architecture

Smart Inquiry AI is planned as a modular web application with separate frontend, backend, and infrastructure layers.

At the product definition stage, this document describes system responsibilities only. It does not define implementation details, frameworks, databases, or deployment tooling.

### Frontend

Responsible for user-facing screens and interactions.

Primary responsibilities:

- Public inquiry form
- Internal inquiry dashboard
- Inquiry detail view
- Status update interface
- Displaying AI summaries and notification state

### Backend

Responsible for business logic, domain rules, data access, and integrations.

Primary responsibilities:

- Accept inquiry submissions
- Validate inquiry data
- Manage inquiry lifecycle
- Coordinate AI output generation
- Trigger notifications
- Expose data to the frontend

### AI Service

Responsible for transforming raw inquiry content into useful business context.

In the MVP, AI Service is a logical responsibility inside the system. It does not need to be deployed as a separate service.

Primary responsibilities:

- Generate inquiry summaries
- Extract customer needs
- Identify missing information
- Suggest next actions
- Return the initial MVP AI output contract
- Fail without preventing inquiry creation
- Support future lead qualification features

### Notification Service

Responsible for recording and sending outbound notification attempts for inquiries.

In the MVP, Notification Service is a logical responsibility inside the system. It does not need to be deployed as a separate service.

Primary responsibilities:

- Record outbound notification attempts
- Send new inquiry notifications through the configured delivery channel
- Support future follow-up reminder notifications
- Track notification delivery state

### Storage

Responsible for keeping product data persistent and queryable.

Primary responsibilities:

- Store inquiries
- Store customer information
- Store notification records
- Support future CRM and SaaS expansion

## MVP Deployment Shape

The MVP should use the simplest deployment shape that can support the core inquiry workflow.

Required MVP components:

- One frontend application
- One backend application
- One relational database
- One external AI provider
- One external email provider

The MVP does not require:

- Microservices
- Message brokers
- Kubernetes
- Event buses
- Multi-tenant infrastructure
- Dedicated background workers
- Authentication
- Role-based permissions
- Multi-user collaboration

The first demo implementation excludes authentication. The internal dashboard is intended only for local or controlled demo use. Real sensitive customer data must not be used in a public deployment until access control is introduced.

Initial MVP AI output contract:

- summary
- customer_need
- urgency
- missing_information
- suggested_next_action

## System Flow

### MVP Inquiry Flow

1. A customer opens the public inquiry form.
2. The customer submits contact details and inquiry details.
3. The backend validates the submitted information.
4. The backend creates an inquiry record.
5. The AI service attempts to generate the initial MVP AI output.
6. The backend preserves the inquiry even if AI generation fails.
7. The notification service records and sends an outbound notification attempt.
8. The inquiry appears in the internal dashboard.
9. A team member reviews the inquiry detail page.
10. The team member updates the inquiry status.

### Internal Review Flow

1. A team member opens the dashboard.
2. The frontend requests inquiry data from the backend.
3. The backend returns inquiry records with AI-generated context, status, and customer context.
4. The team member opens an inquiry detail view.
5. The team member reviews the original message, AI-generated context, and notification history.
6. The team member decides the next follow-up action.

## Future Expansion Notes

The architecture should stay simple during MVP, but avoid choices that block future CRM and SaaS stages.

### CRM Expansion

Future CRM features may require:

- Customer profile history
- Opportunity pipeline
- Follow-up reminders
- Notes and activity timelines
- Assignment to team members
- Search, filters, and tags
- Inquiry-to-opportunity conversion
- Authentication
- Role-based permissions
- Multi-user collaboration

### SaaS Expansion

Future SaaS features may require:

- User accounts
- Organization workspaces
- Role-based permissions
- Multi-tenant data isolation
- Subscription billing
- Usage limits
- Admin settings
- Audit logs

### Integration Expansion

Future integrations may include:

- Attachments
- File upload and file preview
- Email providers
- Calendar tools
- Website form embeds
- CRM exports
- Messaging tools
- File storage providers

### Architecture Principles

- Keep the MVP workflow small and understandable.
- Separate domain logic from interface concerns.
- Treat AI output as assistance, not the source of truth.
- Keep raw inquiry data available alongside AI-generated summaries.
- Never let AI generation failure block inquiry creation.
- Design domain boundaries before designing database tables.
- Add SaaS complexity only after the single-team workflow is useful.
