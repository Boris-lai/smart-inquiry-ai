# Roadmap

This roadmap organizes Smart Inquiry AI into three major stages: MVP, CRM, and SaaS.

The goal is to validate the core inquiry workflow first, then expand into customer relationship management, and only then build SaaS infrastructure.

## Phase 1: MVP

Goal: Prove that AI-assisted inquiry handling creates immediate value for small teams.

### Core Workflow

- Public inquiry form
- Inquiry data storage
- AI output using the initial MVP contract
- AI output failure handling that still creates the inquiry
- Email notification
- Internal dashboard
- Inquiry detail page
- Basic status tracking

### MVP Status Values

- New
- In Progress
- Completed
- Archived

### MVP Deliverables

- Clear inquiry intake experience
- Simple internal review dashboard
- AI output using the initial MVP contract
- Notification when a new inquiry arrives
- Basic documentation for setup and usage

Initial MVP AI output contract:

- summary
- customer_need
- urgency
- missing_information
- suggested_next_action

AI generation failure must never prevent an Inquiry from being created.

Attachment upload is not part of the initial MVP. Attachment remains a future-ready domain for a later file upload feature.

### MVP Success Signal

Users can receive, understand, and follow up on inquiries faster than with email and spreadsheets alone.

## Phase 2: CRM

Goal: Expand from inquiry capture into relationship and opportunity management.

### CRM Features

- Customer profiles
- Contact history
- Inquiry-to-opportunity conversion
- Opportunity pipeline
- Follow-up reminders
- Notes and activity timeline
- Search and filtering
- Tags and categories
- Owner assignment

### AI Enhancements

- Lead qualification suggestions
- Priority scoring
- Suggested next actions
- Reply draft generation
- Customer need extraction
- Duplicate inquiry detection

### CRM Success Signal

Users can manage active opportunities and follow-ups inside Smart Inquiry AI without relying on separate spreadsheets.

## Phase 3: SaaS

Goal: Turn the product into a scalable multi-customer software service.

### SaaS Foundation

- User accounts
- Organization workspaces
- Role-based access
- Multi-tenant data isolation
- Subscription billing
- Usage limits
- Admin settings
- Team invitations

### SaaS Product Features

- Industry-specific inquiry templates
- Custom fields
- Custom status pipelines
- Workflow automation rules
- Email integration
- Calendar integration
- Export and reporting
- Audit logs

### SaaS Operations

- Production deployment
- Monitoring and logging
- Backup strategy
- Security review
- Onboarding flow
- Help documentation
- Pricing and packaging

### SaaS Success Signal

Multiple businesses can independently sign up, configure their workspace, process inquiries, and pay for continued use.

## Roadmap Discipline

Features should be promoted only when the previous stage is usable:

- Do not build CRM complexity before the MVP workflow works.
- Do not build SaaS infrastructure before the product value is validated.
- Do not add automation until the manual workflow is clear.
- Do not optimize advanced analytics before the core data is reliable.
