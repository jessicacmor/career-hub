# ADR-NNN: <Short decision title>

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by ADR-NNN
- **Supersedes:** ADR-NNN (only if this replaces an earlier decision)

## Context

What situation or problem forced a decision? What constraints apply (the brief,
hardware, licenses, earlier ADRs)? State facts and evidence, not conclusions.

## Decision

The choice, stated as a rule: "We use X, not Y." Name the alternatives that were
considered and why they lost.

## Consequences

What becomes easier, what becomes harder, and what must now be true elsewhere in
the codebase. Include when the decision should be revisited.

## References

Links to docs, increment folders, or external sources that support this.

---

How to use this template:

- Copy to `docs/adr/NNN-short-title.md`, using the next unused three-digit number.
- One decision per ADR. Record project-wide choices here; choices that only
  matter inside one increment belong in that increment's `README.md`.
- Once accepted, never edit the decision. To reverse it, write a new ADR with
  `Supersedes: ADR-NNN`, and change the old one's status to
  `Superseded by ADR-MMM`.
- Name no individuals — this repository is public.
