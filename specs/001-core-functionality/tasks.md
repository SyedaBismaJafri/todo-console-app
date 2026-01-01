---

description: "Task list template for feature implementation"
---

# Tasks: Core Functionality

**Input**: Design documents from `/specs/001-core-functionality/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python project with Rich dependencies
- [X] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Setup Task model with validation per data-model.md
- [X] T005 [P] Implement TaskService for business logic
- [X] T006 [P] Setup ConsoleUI using Rich library
- [X] T007 Create CLICommands module
- [X] T008 Configure error handling and logging infrastructure
- [X] T009 Setup ApplicationManager to coordinate components

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks with title and description (max 100/500 chars) with validation

**Independent Test**: Users can successfully add a new task with title and description in under 10 seconds with professional UI feedback

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py
- [ ] T011 [P] [US1] Integration test for adding tasks in tests/integration/test_add_task.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Create Task model in src/models/task.py (already implemented)
- [X] T013 [P] [US1] Create TaskService.add_task method in src/services/task_service.py
- [X] T014 [US1] Implement add_task command in src/cli/commands.py
- [X] T015 [US1] Add validation for title length (max 100 chars) in src/models/task.py
- [X] T016 [US1] Add validation for description length (max 500 chars) in src/models/task.py
- [X] T017 [US1] Add error handling for empty titles in src/services/task_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Display all tasks with their status indicators in a professional UI using Rich

**Independent Test**: Users can view all tasks with clear status indicators (completed/incomplete) in a professionally formatted table

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Unit test for TaskService.get_all_tasks in tests/unit/test_task_service.py
- [ ] T019 [P] [US2] Integration test for viewing tasks in tests/integration/test_view_tasks.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Create TaskService.get_all_tasks method in src/services/task_service.py
- [X] T021 [US2] Implement ConsoleUI.display_tasks in src/ui/console_ui.py
- [X] T022 [US2] Implement view_tasks command in src/cli/commands.py
- [X] T023 [US2] Add Rich table formatting for task display in src/ui/console_ui.py
- [X] T024 [US2] Add status indicators (completed/incomplete) in src/ui/console_ui.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Allow users to toggle the completion status of tasks with visual feedback

**Independent Test**: Users can mark tasks as complete/incomplete with 100% success rate and visual feedback

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US3] Unit test for TaskService.toggle_task_status in tests/unit/test_task_service.py
- [ ] T026 [P] [US3] Integration test for toggling task status in tests/integration/test_toggle_task.py

### Implementation for User Story 3

- [X] T027 [P] [US3] Create TaskService.toggle_task_status method in src/services/task_service.py
- [X] T028 [US3] Implement toggle_task_status command in src/cli/commands.py
- [X] T029 [US3] Add visual feedback for status changes in src/ui/console_ui.py
- [X] T030 [US3] Update Task model with status properties in src/models/task.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Allow users to update task title or description by ID with UI confirmation

**Independent Test**: Users can update task details with 100% success rate and UI confirmation

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US4] Unit test for TaskService.update_task in tests/unit/test_task_service.py
- [ ] T032 [P] [US4] Integration test for updating tasks in tests/integration/test_update_task.py

### Implementation for User Story 4

- [X] T033 [P] [US4] Create TaskService.update_task method in src/services/task_service.py
- [X] T034 [US4] Implement update_task command in src/cli/commands.py
- [X] T035 [US4] Add validation for updated title/description in src/services/task_service.py
- [X] T036 [US4] Add UI confirmation for updates in src/ui/console_ui.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Allow users to delete tasks by ID with UI feedback

**Independent Test**: Users can delete tasks with 100% success rate and UI confirmation

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US5] Unit test for TaskService.delete_task in tests/unit/test_task_service.py
- [ ] T038 [P] [US5] Integration test for deleting tasks in tests/integration/test_delete_task.py

### Implementation for User Story 5

- [X] T039 [P] [US5] Create TaskService.delete_task method in src/services/task_service.py
- [X] T040 [US5] Implement delete_task command in src/cli/commands.py
- [X] T041 [US5] Add UI feedback for deletion in src/ui/console_ui.py
- [X] T042 [US5] Handle error cases for non-existent tasks in src/services/task_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Documentation updates in docs/
- [X] T044 Code cleanup and refactoring
- [X] T045 Performance optimization across all stories
- [ ] T046 [P] Additional unit tests (if requested) in tests/unit/
- [X] T047 Security hardening
- [X] T048 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model validation in tests/unit/test_task.py"
Task: "Integration test for adding tasks in tests/integration/test_add_task.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in src/models/task.py (already implemented)"
Task: "Create TaskService.add_task method in src/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence