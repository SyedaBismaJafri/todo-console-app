# Data Model: Core Functionality

## Task Entity

### Attributes
- **id**: int (unique identifier, auto-generated)
- **title**: str (required, max 100 characters, standard text characters)
- **description**: str (optional, max 500 characters)
- **completed**: bool (default: False)
- **created_at**: datetime (auto-generated timestamp)

### Validation Rules
- Title must not be empty
- Title must not exceed 100 characters
- Description must not exceed 500 characters
- ID must be unique within the application session

### State Transitions
- Task starts as incomplete (completed=False)
- Task can be toggled to completed (completed=True)
- Task can be toggled back to incomplete (completed=False)

## TaskService

### Responsibilities
- Create new tasks with auto-generated IDs
- Retrieve tasks by ID
- Update task details with validation
- Delete tasks by ID
- Toggle task completion status
- List all tasks

### Validation Requirements
- Validate title is not empty before adding/updating
- Validate title does not exceed 100 characters before adding/updating
- Validate description does not exceed 500 characters before adding/updating
- Validate task exists before updating/deleting