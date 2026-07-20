# Changelog

All notable changes to Smart Inquiry AI will be documented in this file.

This project follows a simple changelog format during early development.

## [Unreleased]

### Added

- Created initial documentation structure.
- Added project README with vision, scope, users, and document index.
- Added product positioning in PRODUCT.md.
- Added staged roadmap from MVP to CRM to SaaS.
- Added initial TODO backlog.
- Added docs directory with supporting planning documents.
- Added engineering wiki structure under docs/.
- Added architecture, domain, decisions, planning, and daily tracking documents.
- Added root .gitignore for a future Next.js and Python/FastAPI project.
- Added placeholder frontend, backend, and infrastructure directories for planned implementation.
- Added database schema documentation.
- Added Mermaid ER diagram.
- Added REST API contract.
- Added standard API error format.
- Added system architecture document.

### Changed

- Expanded placeholder planning notes into structured project documentation.
- Standardized MVP inquiry lifecycle as New, In Progress, Completed, and Archived.
- Removed attachment upload from the initial MVP scope while keeping Attachment as a future-ready inactive domain.
- Clarified that authentication is excluded from the first demo implementation and the internal dashboard is only for local or controlled demo use.
- Refined Notification as a record of an outbound notification attempt associated with an Inquiry.
- Defined the initial AI output contract as summary, customer_need, urgency, missing_information, and suggested_next_action.
- Clarified that AI generation failure must never prevent an Inquiry from being created.
- Split TODO Definition of Done into feature and milestone completion standards.
- Replaced Sprint 1 planning placeholders with an actionable Sprint 1 plan.
- Updated Day 03 planning notes to reflect completed documentation and product-definition work.
- Updated README links and project structure after documentation reorganization.
- Clarified active MVP domains as Inquiry, Customer, and Notification.
- Clarified Attachment as a future inactive domain.
- Finalized inquiry_type, budget_range, and timeline as approved optional MVP fields.
- Documented cross-field phone validation for preferred phone contact.
- Standardized API routes under `/api/v1`.
- Synchronized planning and progress documents for Day 6 readiness.

### Removed

- Removed potential_value from the MVP AI output contract.
