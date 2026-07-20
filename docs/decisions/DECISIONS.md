# Decisions

This file records important product and technical decisions for Smart Inquiry AI.

## Decision Format

Each decision should include:

- Date
- Decision
- Context
- Reason
- Consequences

## Decisions

### 2026-07-17: Start With Documentation Before Code

Decision: Establish project documentation before creating application code.

Context: The project needs a clear product direction, staged roadmap, and initial backlog before implementation begins.

Reason: A documented foundation helps prevent premature feature building and keeps MVP, CRM, and SaaS stages separate.

Consequences: No application code is created in this step. Implementation will begin only after product scope and initial planning are clear.

### 2026-07-17: Roadmap Uses MVP To CRM To SaaS

Decision: Organize the roadmap into MVP, CRM, and SaaS stages.

Context: Smart Inquiry AI can grow into a large product, but the first version should remain focused.

Reason: Separating the stages keeps the early product small while preserving a path toward a larger platform.

Consequences: CRM and SaaS features are documented as future stages, not MVP requirements.

### 2026-07-18: Exclude Authentication From First Demo Implementation

Decision: Authentication is excluded from the first demo implementation.

Context: The MVP is intended to validate the inquiry workflow before adding account management, permissions, or collaboration features.

Reason: Access control adds product and engineering complexity that is not required to prove the first controlled demo workflow.

Consequences: The internal dashboard is intended only for local or controlled demo use. Real sensitive customer data must not be used in a public deployment until access control is introduced.

### 2026-07-18: Keep Attachment Upload Outside The Initial MVP

Decision: Attachment upload is not part of the initial MVP.

Context: Attachment is useful for future inquiry workflows, but file upload, storage, preview, and file safety concerns are not required for the first demo.

Reason: Keeping attachments inactive protects MVP simplicity while preserving the domain concept for later expansion.

Consequences: Attachment remains documented as a future-ready domain and should become active only when file upload is introduced.

### 2026-07-18: Define Initial AI Output Contract

Decision: The initial MVP AI output contract is summary, customer_need, urgency, missing_information, and suggested_next_action.

Context: The product needs consistent AI output across product, architecture, domain, and MVP scope documents.

Reason: A small explicit contract makes implementation planning easier and avoids adding scoring or valuation fields before they are needed.

Consequences: potential_value is excluded from the MVP AI output. AI generation failure must never prevent an Inquiry from being created.
