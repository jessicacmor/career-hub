# Career Development Hub Project Proposal

## Instructions for Claude

Act as my development partner and help me build this project in small, working increments. This proposal is the starting specification. First inspect any existing repository and its instructions, summarize your implementation approach, and start the first milestone. Ask only questions that genuinely block progress. Make reasonable, reversible choices and explain them briefly.

Do not build the entire roadmap at once. Complete and verify each milestone before expanding scope. Keep the application usable throughout development. Explain setup and important decisions in beginner-friendly language so I can understand and maintain the code.

## Purpose and context

I want a personal Career Development Hub that helps me land a role aligned with software development, infrastructure development, Python, automation, and AI-assisted development.

I need something useful throughout my job search. I am an early-career developer with an IT support background and a technical apprenticeship. I have worked on a Python-based full-stack recognition application, collaborated with stakeholders, handled code reviews, and delivered features. Help me describe my own contributions accurately, including collaboration and AI assistance.

Scattered tabs, multiple tracking systems, and long task lists make a job search harder to sustain. The product should reduce decisions and make the next useful action clear. It should also preserve professional contacts, networking history, resume versions, and learning resources.

Success means better decisions, stronger evidence for applications, and consistent follow-through. Application volume alone is not the goal. The application cannot promise interviews or predict hiring outcomes.

## Product principles

- Provide useful job tracking and experience management before adding AI.
- Keep one primary next action visible for each opportunity.
- Separate my career preferences from what my past experience happens to match.
- Treat AI output as an editable draft, with evidence and uncertainty visible.
- Keep personal data portable and under my control.
- Prioritize a working personal tool over an elaborate platform.

## Technical direction and open source requirement

Use Python, Streamlit, and SQLite for the initial application. Use Python's built-in SQLite support unless a concrete need justifies an ORM. Use Ollama for local inference and a configurable local model with an appropriate permissive license, such as a specifically verified Apache-licensed Qwen3 model.

All required application components must use open source licenses; SQLite's public-domain status is acceptable. Model weights must be downloadable and licensed for the intended use. Record software licenses and the exact model license separately. Do not claim that open weights necessarily mean fully open training data or a reproducible training process.

There must be no required paid API, subscription, commercial database, cloud hosting, or proprietary service. Existing hardware, electricity, and internet access are assumed. Runtime must work offline after dependencies and the chosen model are installed; manually entered jobs remain usable without network access.

Claude is the development assistant receiving this brief, not an application runtime dependency. If I later want an entirely open source development workflow, document that a local coding assistant can replace it without changing the app architecture.

Before installing, verify current package compatibility and licenses against official sources. Choose a supported Python version, pin direct dependencies, and provide a reproducible dependency lock or equivalent. Avoid unnecessary frameworks, agent orchestration, vector databases, separate backend services, and containers in the first version.

Use Git for version control. Keep private records, database files, exports, backups, local configuration, and model files out of the repository. Include synthetic sample data for demonstrations.

## Initial user workflow

1. Add a few accomplishments and career preferences.
2. Paste a job description and save its source URL, employer, title, and deadline if known.
3. Review the opportunity manually, then optionally request an AI assessment.
4. Associate relevant accomplishments and contacts with the opportunity.
5. Set a next action and due date.
6. Track application progress and follow-ups.
7. Open Today to see up to three useful actions and mark them complete or reschedule them.

Job descriptions should be pasted initially. A source URL is a reference, not a promise that the app fetches the page.

## Core features

### Experience bank

Create, edit, search, archive, and delete experience entries. Include a title, project or role, dates, situation or problem, my contribution, collaborators or AI assistance, outcome, skills, supporting notes or references, and verification status.

Let me explicitly distinguish confirmed outcomes from estimates or details I still need to verify. Do not turn unverified figures into resume claims. Supporting references can initially be notes or links; file parsing is not required.

### Opportunities and applications

Capture employer, job title, description, URL, location, work arrangement, compensation when provided, date saved, deadline, status, interest, relevant contacts, related accomplishments, and next action.

Suggested statuses: Saved, Exploring, Preparing, Applied, Interviewing, Offer, Rejected, Withdrawn, and Archived. Keep status editable and preserve a simple activity history. Show when a listing or assessment was last checked rather than implying a saved job is still open.

Store salary currency and pay period when compensation is entered. Keep missing information unknown rather than inventing defaults.

### Contacts and networking

Save name, company, role, contact details or profile link, relationship context, notes, and last interaction. Log conversations and link contacts to relevant jobs. Record a follow-up as an action with a due date.

Drafting a message is allowed. Sending messages, submitting applications, and contacting people automatically are outside the initial scope.

### Today

Show up to three suggested actions with a short explanation for each. Let me pin an action, complete it, or reschedule it. Keep the remaining backlog accessible without displaying everything at once.

Use transparent Python rules rather than AI: approaching deadlines, overdue follow-ups, explicit user priority, and actionable opportunities. Exclude completed actions and closed opportunities. If there are fewer than three real actions, show fewer than three. Do not invent work to fill the screen.

### Career preferences

Record preferred roles, skills I want to develop, work arrangement, location constraints, compensation preferences, and dealbreakers. Allow an unknown or flexible value.

A support-heavy role may be technically familiar but poorly aligned with my goals. Show career alignment and evidence of qualification separately.

## Local AI features

Add AI after the core tracker works. Put model access behind one small service interface so the UI and database do not depend directly on Ollama response details.

### Job fit assessment

Use the pasted job description, my preferences, and explicitly selected experience entries. Let me see what information will be sent. Start with manual selection rather than implementing semantic retrieval.

Return a structured result containing:

- Key requirements from the description, each with a short supporting excerpt.
- Relevant experience, identified by stored experience IDs.
- Transferable skills and the reasoning connecting them to the role.
- Gaps, missing information, and questions to investigate.
- Career alignment and any explicit dealbreaker conflicts.
- A qualitative recommendation such as Worth exploring, Reasonable stretch, or Lower priority, with reasons.
- A suggested next action.

Avoid numerical match scores or hiring probabilities. Distinguish facts in the listing, facts I entered, and model inferences. Treat a recommendation as advice I can override.

### Application drafts and interview preparation

Generate role-specific resume bullets, outreach drafts, and interview questions from selected records. Save drafts linked to the opportunity and keep user-edited versions distinct from original model output.

Every factual application claim must map to supporting experience IDs. Never invent credentials, metrics, employers, dates, responsibilities, or outcomes. If evidence is missing, omit the claim or ask for the missing detail. Identify possible overstatements for review.

For interviews, propose questions and help outline answers grounded in selected experiences. Do not invent stories on my behalf.

### Reliability and hardware

Make the model configurable. Check available memory, architecture, and disk space before suggesting a model download; do not assume any particular machine will remain available. Explain the performance tradeoff and test with a small real example before committing to a model.

Handle an unavailable Ollama server, missing model, timeout, oversized input, and invalid structured output without losing user input or breaking the tracker. Validate returned fields and referenced IDs in code. Schema validation cannot prove factual accuracy, so retain human review.

Do not silently truncate a job description or experience selection. Explain the limit and let me reduce input. Store model name, prompt version, generation time, and input record versions or a minimal snapshot with each assessment so stale results are recognizable.

Treat job descriptions and imported text as untrusted data. Their contents cannot change application rules, execute commands, access unrelated records, or trigger tool actions. AI should generate text only.

## Data and application structure

Use separate records for experience, preferences, opportunities, contacts, interactions, actions, drafts, and assessments. Use linking tables where an opportunity has multiple contacts or experience entries. Keep actions in one place rather than duplicating due dates across screens.

Use stable IDs, created and updated timestamps, parameterized SQL, foreign key enforcement, and transactions. Define archive versus permanent deletion behavior and avoid orphaned links. Confirm permanent deletions in the interface.

Keep code organized into UI pages, database access, ordinary business logic, and optional AI services. Use a persistent local data directory independent of the current working directory. Streamlit reruns must not duplicate records, reset unsaved forms unnecessarily, or trigger repeated AI calls.

Document database schema changes and back up existing data before migrations. Use SQLite's backup facilities or another consistent backup method. Provide a tested restore procedure and a versioned JSON export of user records and relationships. CSV exports can be added for individual tables.

The first version uses text records and file references. Managed document uploads and resume file generation are later enhancements.

## Interface direction

Use a calm, readable interface with clear labels, accessible contrast, helpful empty states, and concise feedback. Avoid crowded dashboards, guilt-based streaks, gamification, or excessive notifications.

Navigation should include Today, Opportunities, Experience, People, and Settings. Put drafts and assessments inside the relevant opportunity rather than creating extra top-level pages immediately.

Make saving explicit. Preserve form input on validation or AI errors. Explain why an action is suggested and make it easy to change priorities.

## Privacy and portability

Bind the application to localhost by default. Do not expose it publicly or require authentication for this local single-user scope. Public deployment would require a separate design for authentication, authorization, and data protection.

Use local inference only. Do not silently fall back to cloud models. Do not add analytics, telemetry, or external integrations to the application. Document any dependency telemetry and how it is disabled where applicable.

Do not import confidential employer materials. Use accomplishments I am permitted to retain and sanitized examples. Do not include personal record contents in routine logs. Clearly document that a local SQLite file is not automatically encrypted.

## Delivery milestones and acceptance checks

### Milestone 1 Working foundation

Deliver project setup, navigation, database initialization, experience CRUD, basic opportunity CRUD, and synthetic sample data. Provide short setup instructions and exact commands to start the app.

Acceptance: I can add an experience and job, edit both, restart the app, and find them unchanged. Form reruns do not create duplicates. All of this works without Ollama.

### Milestone 2 Usable job search workflow

Add preferences, contacts, interactions, linked evidence, actions, application stages, search, and Today. Include backup and restore instructions, a working backup mechanism, and versioned JSON export before I rely on real data.

Acceptance: I can link a contact and experience to a job, set a follow-up, see it on Today, complete it, and retain the history. Closed opportunities do not generate suggestions. A backup restores into a separate temporary location with relationships intact.

### Milestone 3 Local job assessment

Add Ollama configuration, local model setup guidance, selected context, structured assessments, input limits, and failure handling.

Acceptance: A real pasted description produces a review referencing valid experience IDs. Unsupported requirements remain gaps. If Ollama is stopped or returns malformed output, the job remains saved and all non-AI features remain usable.

### Milestone 4 Drafting and handoff

Add evidence-linked resume bullets, outreach drafts, interview preparation, saved versions, and an updated README. Include a brief manual walkthrough using synthetic data.

Acceptance: Drafts can be edited and saved without overwriting prior versions. Factual claims have evidence references for review. I can reproduce setup from the documentation and explain the main architecture.

Use focused automated tests for persistence, relationships, action prioritization, backup and restore, AI response validation, and failure handling. Mock model calls for repeatable tests. Also perform a small manual local-model evaluation; mocked tests do not establish output quality. Check the UI for usability and accidental repeated actions.

After each milestone, report what works, how it was verified, known limitations, and the next increment. Continue when checks pass; pause only for a real blocker or a change requiring my decision.

## Later enhancements

After the core workflow proves useful, consider resume file history and document export, PDF or DOCX text extraction, a resource library, semantic experience search, opt-in reminders, and job feeds with documented permitted access.

Automatic scraping, email or calendar access, browser automation, automatic applications, message sending, multiple users, cloud deployment, and autonomous agents are outside the first version. Do not introduce them as hidden prerequisites.

## First action

Inspect the available workspace. Propose the minimal folder structure and implementation sequence, state any assumptions, and implement Milestone 1. If the workspace is empty, initialize a clean project. Begin with ordinary Python and SQLite; leave model installation until Milestone 3 so hardware decisions do not block the useful foundation.
