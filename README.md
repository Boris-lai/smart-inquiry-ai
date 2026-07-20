# Smart Inquiry AI

Smart Inquiry AI is an AI-powered inquiry intake and workflow automation platform for small and medium-sized businesses.

The project helps teams collect customer inquiries, structure messy request details, generate AI-assisted summaries, and move opportunities into a repeatable follow-up workflow.

## Vision

Turn scattered customer inquiries into organized, actionable business workflows.

Many service businesses receive new opportunities through website forms, email, messaging apps, referrals, and manual spreadsheets. Important context is often fragmented, follow-up depends on memory, and teams lose time rewriting the same summaries, qualification notes, and replies.

Smart Inquiry AI aims to become a lightweight operating layer between customer demand and internal execution.

## Product Overview

The initial product starts with inquiry capture:

1. A customer submits an inquiry.
2. The system stores structured inquiry data.
3. AI attempts to generate structured inquiry context.
4. The team receives a notification.
5. The inquiry appears in a simple dashboard for review and follow-up.

Over time, this foundation expands into CRM features, automation rules, collaboration tools, and a multi-tenant SaaS product.

## Core Idea

Smart Inquiry AI begins with a simple workflow: receive an inquiry, structure the information, generate useful context, notify the team, and track the follow-up state.

## Target Users

- Small and medium-sized businesses
- Design studios
- Web agencies
- Consulting firms
- Service providers that handle custom quotes
- Teams that still manage leads through email, spreadsheets, and manual notes

## Problems To Solve

- Inquiries arrive from multiple channels and are hard to organize.
- Teams manually rewrite customer needs into summaries.
- Important opportunities can be missed or forgotten.
- Sales and delivery context is scattered across email, chat, and spreadsheets.
- Small teams need CRM-like workflow without heavy enterprise software.

## MVP Scope

The MVP focuses on proving the core inquiry workflow:

- Public inquiry form
- Inquiry storage
- AI output using the initial MVP contract
- Email notification
- Internal inquiry dashboard
- Basic status tracking

The MVP should stay intentionally small. It should validate whether AI-assisted inquiry handling saves time and improves follow-up quality.

## Current Status

Product planning is complete for the approved MVP specification.

Architecture, domain, database, and API contracts are approved. Application implementation has not started yet.

The next phase is Day 6 backend foundation.

## Roadmap

The product roadmap is organized into three major stages:

- MVP: Capture, summarize, notify, and review inquiries.
- CRM: Manage customers, opportunities, follow-ups, notes, and pipeline states.
- SaaS: Support accounts, teams, billing, multi-tenant data, templates, integrations, and scalable operations.

See [ROADMAP.md](ROADMAP.md) for the full staged plan.

## Project Structure

Current project structure:

- `frontend/`: Reserved for the future frontend application.
- `backend/`: Reserved for the future backend application.
- `infrastructure/`: Reserved for future deployment and infrastructure planning.
- `docs/`: Supporting product and planning documentation.
- `docs/architecture/`: Architecture documentation.
- `docs/api/`: API documentation.
- `docs/database/`: Database documentation.
- `docs/domain/`: Domain model and shared terminology.
- `docs/decisions/`: Decision records.
- `docs/learning/`: Learning notes.
- `docs/meeting-notes/`: Meeting notes.
- `docs/website/`: Website planning.
- `docs/youtube/`: YouTube planning.
- `docs/portfolio/`: Portfolio planning.
- `planning/`: Sprint and daily development tracking.
- `README.md`: Project landing page and overview.
- `PRODUCT.md`: Product definition and positioning.
- `ROADMAP.md`: Product roadmap.
- `TODO.md`: Product and engineering backlog.
- `CHANGELOG.md`: Project change history.

The frontend, backend, and infrastructure directories are implementation placeholders until Day 6 begins. Implementation details will be added only after the MVP specification freeze.

## Documentation

- [PRODUCT.md](PRODUCT.md): Product positioning, users, problems, and product principles.
- [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md): High-level architecture, MVP deployment shape, and future expansion notes.
- [docs/architecture/SYSTEM_ARCHITECTURE.md](docs/architecture/SYSTEM_ARCHITECTURE.md): MVP system architecture and request flow.
- [docs/domain/DOMAIN_MODEL.md](docs/domain/DOMAIN_MODEL.md): Core domains, relationships, and business rules.
- [docs/database/DATABASE_SCHEMA.md](docs/database/DATABASE_SCHEMA.md): MVP relational database schema.
- [docs/database/ER_DIAGRAM.md](docs/database/ER_DIAGRAM.md): Mermaid ER diagram and relationship rules.
- [docs/api/API_CONTRACT.md](docs/api/API_CONTRACT.md): MVP REST API contract.
- [docs/api/ERROR_FORMAT.md](docs/api/ERROR_FORMAT.md): Standard API error envelope and error handling rules.
- [ROADMAP.md](ROADMAP.md): Development phases from MVP to CRM to SaaS.
- [TODO.md](TODO.md): Initial backlog and execution checklist.
- [CHANGELOG.md](CHANGELOG.md): Project change history.
- [planning/Sprint-01.md](planning/Sprint-01.md): Sprint 1 working document.
- [planning/daily/Day-03.md](planning/daily/Day-03.md): Daily progress tracking template.
- [docs/README.md](docs/README.md): Documentation index.
- [docs/decisions/DECISIONS.md](docs/decisions/DECISIONS.md): Product and technical decision log.
- [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md): MVP boundaries and non-goals.
- [docs/domain/GLOSSARY.md](docs/domain/GLOSSARY.md): Shared terminology.

## Development Workflow

The project workflow is documentation-first and milestone-driven:

1. Define product direction.
2. Review architecture boundaries.
3. Clarify the domain model.
4. Maintain the backlog.
5. Plan the sprint.
6. Begin implementation only after the MVP specification is frozen.
7. Document each completed feature.
8. Review architecture impact before expanding scope.
9. Commit completed work.
10. Update portfolio, blog, and YouTube tracking where relevant.

## Development Principles

Build in clear stages:

1. Define product direction.
2. Validate the MVP workflow.
3. Add CRM depth only after the core workflow is useful.
4. Convert to SaaS after the single-team product is stable.

This keeps the project focused and prevents premature complexity.

## Contribution Guidelines

Smart Inquiry AI is currently at the MVP specification freeze stage.

Contributions should follow these guidelines:

- Keep MVP scope small and focused.
- Prefer clear documentation before implementation.
- Do not introduce CRM or SaaS complexity into MVP work.
- Keep architecture changes aligned with [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md).
- Keep domain changes aligned with [docs/domain/DOMAIN_MODEL.md](docs/domain/DOMAIN_MODEL.md).
- Update [TODO.md](TODO.md) when new work is identified.
- Update [CHANGELOG.md](CHANGELOG.md) for notable changes.

## License

License: TBD
