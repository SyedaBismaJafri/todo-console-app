<!-- 
SYNC IMPACT REPORT
Version change: N/A → 1.0.0 (initial version)
List of modified principles: N/A (initial principles defined)
Added sections: All principles and sections are newly defined
Removed sections: N/A
Templates requiring updates: 
- .specify/templates/plan-template.md ✅ compatible (has Constitution Check section)
- .specify/templates/spec-template.md ✅ compatible (no direct principle references)
- .specify/templates/tasks-template.md ✅ compatible (no direct principle references)
- .qwen/commands/*.toml ✅ compatible (reference constitution appropriately)
Follow-up TODOs: 
- RATIFICATION_DATE: needs to be determined and updated in constitution
-->

# todo-console-app Constitution

## Core Principles

### Console-First
Every feature starts as a console application; Applications must be self-contained, independently testable, documented; Clear purpose required - no organizational-only applications

### CLI Interface
Every application exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats

### Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced

### Integration Testing
Focus areas requiring integration tests: New application contract tests, Contract changes, Inter-service communication, Shared schemas

### Observability
Text I/O ensures debuggability; Structured logging required

### Simplicity
Start simple, YAGNI principles

## Additional Constraints
Technology stack requirements, compliance standards, deployment policies

## Development Workflow
Code review requirements, testing gates, deployment approval process

## Governance
All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): needs to be determined | **Last Amended**: 2025-12-31