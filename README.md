# The Evolution of Todo: Phase I

A simple, in-memory Python console application for managing todo tasks.

## Overview

This is a console-based todo application that allows users to:
- Add new tasks with title and description
- View all tasks with status indicators
- Mark tasks as complete/incomplete
- Update task details
- Delete tasks

## Technology Stack

- Python 3.13+
- UV Package Manager
- Rich library for professional UI
- Standard Library (for in-memory storage in Phase I)

## Setup Instructions

1. Ensure you have Python 3.13+ installed on your system
2. Install UV package manager if you don't have it:
   ```bash
   pip install uv
   ```
3. Clone or download this repository
4. Navigate to the project directory
5. Install dependencies:
   ```bash
   uv sync
   ```
   Or if you prefer pip:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Usage

To run the application:

### Using uv (recommended):
```bash
uv run todo-app
```

### Using the installed command (after pip install -e .):
```bash
todo-app
```

### Using Python module directly:
```bash
python -m src.todo_app
```

## Project Structure

```
todo-console-app/
├── specs/                    # Specification files
│   └── basic-task-management.md
├── src/                      # Source code
│   ├── todo_app.py           # Main application entry point
│   ├── manager.py            # Application manager
│   ├── cli/                  # Command-line interface
│   │   └── commands.py
│   ├── models/               # Data models
│   │   └── task.py
│   ├── services/             # Business logic
│   │   └── task_service.py
│   └── ui/                   # User interface
│       └── console_ui.py
├── README.md                 # This file
└── .specify/                 # Spec-Kit Plus configuration
```

## Core Functionalities

1. **Add Task**: Add a new task with title and description
2. **View Tasks**: Display all tasks with status indicators
3. **Mark Complete/Incomplete**: Toggle the status of a task
4. **Update Task**: Modify the title or description of a task
5. **Delete Task**: Remove a task by its unique ID

## Development

This project follows a spec-driven development approach. All features are first specified in the `/specs` directory before implementation.

## Contributing

1. Review the specification in `/specs/basic-task-management.md`
2. Follow the existing code style and patterns
3. Ensure all functionality matches the specification
