# TODO

Initial backlog for Smart Inquiry AI.

This list is intentionally product-first. Implementation tasks should be added only after the documentation foundation is complete.

## Sprint 1 Overview

### Sprint Goal

Establish the product definition, architecture direction, domain model, and first implementation-ready backlog for Smart Inquiry AI.

### Current Progress

Day 1-5 specification work is complete. Day 6 backend foundation, ORM models, Alembic setup, the initial schema migration, Pydantic API schemas, and standard error handling are in place. Day 7 public inquiry submission now stores Customer and Inquiry records transactionally.

### Current Task

Continue the MVP inquiry workflow without expanding scope.

### Next Milestone

Complete the inquiry submission path, then add AI, email, dashboard, and frontend pieces in separate scoped steps.

## Feature Definition of Done

Every completed feature should include:

- [ ] Implementation
- [ ] Validation/tests
- [ ] Required documentation
- [ ] Review
- [ ] Git commit

## Milestone Definition of Done

Every completed milestone should include:

- [ ] Demo screenshots
- [ ] README update
- [ ] Portfolio update
- [ ] Blog draft
- [ ] YouTube topic or script

## Documentation Foundation

- [x] Create README
- [x] Create PRODUCT document
- [x] Create ROADMAP document
- [x] Create TODO backlog
- [x] Create CHANGELOG
- [x] Create docs directory
- [x] Add documentation index
- [x] Define MVP scope
- [x] Add decision log
- [x] Add glossary

## Product Definition Backlog

- [x] Define exact MVP user flow
- [x] Define inquiry form fields
- [x] Define required and optional customer fields
- [x] Define AI output contract
- [x] Define inquiry status lifecycle
- [x] Define dashboard list content
- [x] Define inquiry detail page content
- [ ] Define notification email content
- [ ] Define MVP success metrics

## Design Backlog

- [ ] Sketch inquiry form layout
- [ ] Sketch dashboard layout
- [ ] Sketch inquiry detail layout
- [ ] Define empty states
- [ ] Define loading states
- [ ] Define error states

## Technical Planning Backlog

- [x] Choose frontend framework
- [x] Choose backend framework
- [x] Choose relational database
- [ ] Choose authentication approach for later phases
- [x] Choose AI provider and model strategy
- [x] Choose email provider strategy
- [x] Define initial data model
- [x] Define API boundaries
- [x] Define environment variables
- [ ] Define deployment target

## MVP Implementation Backlog

- [x] Initialize application project
- [x] Add Customer, Inquiry, and Notification ORM models
- [x] Initialize Alembic and create initial schema migration
- [x] Add Pydantic API schemas
- [x] Add standard API error-handling foundation
- [x] Add public inquiry submission endpoint
- [x] Add Customer lookup/create/update behavior
- [x] Store Customer and Inquiry transactionally
- [ ] Build inquiry form
- [x] Store inquiry submissions
- [ ] Generate AI output
- [ ] Send email notification
- [ ] Build internal dashboard
- [ ] Build inquiry detail view
- [ ] Add basic status update
- [ ] Add basic validation
- [ ] Add dashboard inquiry API endpoints
- [ ] Add MVP setup documentation

## Website Backlog

- [ ] Home Page
- [ ] About Page
- [ ] Projects Page
- [ ] Articles Page
- [ ] Contact Page
- [ ] SEO Metadata

## YouTube Backlog

- [ ] Video 001
- [ ] Script
- [ ] Thumbnail
- [ ] Description
- [ ] Publish

## Portfolio Backlog

- [ ] Case Study
- [ ] Architecture Diagram
- [ ] Screenshots
- [ ] Demo GIF
- [ ] GitHub README Update

## Knowledge Backlog

- [ ] Database Notes
- [ ] API Notes
- [ ] AI Prompt Notes
- [ ] Deployment Notes

## Later Backlog

- [ ] Customer profiles
- [ ] Opportunity pipeline
- [ ] Follow-up reminders
- [ ] AI reply drafts
- [ ] Team accounts
- [ ] Multi-tenant organizations
- [ ] Billing
- [ ] Integrations
- [ ] Analytics
