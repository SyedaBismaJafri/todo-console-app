# API Contract: Todo Console Application

## Overview
This document defines the interface contracts for the todo console application. Since this is a console application, the "API" refers to the command interface and data contracts.

## Command Interface

### Add Task Command
- **Command**: `add`
- **Input**: 
  - title (string, required, max 100 characters)
  - description (string, optional, max 500 characters)
- **Output**: 
  - Success: Task added successfully with ID: {id}
  - Error: Appropriate error message
- **Validation**: 
  - Title must not be empty
  - Title must not exceed 100 characters
  - Description must not exceed 500 characters

### View Tasks Command
- **Command**: `view`
- **Input**: None
- **Output**: 
  - List of all tasks with ID, title, description, and completion status
  - Formatted using Rich library tables and colors
  - If no tasks: "No tasks found. Add some tasks to get started!"

### Update Task Command
- **Command**: `update`
- **Input**: 
  - task_id (integer, required)
  - title (string, optional, max 100 characters)
  - description (string, optional, max 500 characters)
- **Output**: 
  - Success: "Task updated successfully."
  - Error: Appropriate error message
- **Validation**: 
  - Task with ID must exist
  - If title provided: must not be empty and not exceed 100 characters
  - If description provided: must not exceed 500 characters

### Delete Task Command
- **Command**: `delete`
- **Input**: 
  - task_id (integer, required)
- **Output**: 
  - Success: "Task with ID {id} deleted successfully."
  - Error: Appropriate error message
- **Validation**: 
  - Task with ID must exist

### Toggle Task Status Command
- **Command**: `toggle`
- **Input**: 
  - task_id (integer, required)
- **Output**: 
  - Success: "Task with ID {id} marked as {status}."
  - Error: Appropriate error message
- **Validation**: 
  - Task with ID must exist

### Help Command
- **Command**: `help`
- **Input**: None
- **Output**: List of available commands with descriptions

### Quit Command
- **Command**: `quit` or `exit`
- **Input**: None
- **Output**: "Goodbye!"

## Data Contracts

### Task Object
```json
{
  "id": integer,
  "title": string (max 100 chars),
  "description": string (max 500 chars, optional),
  "completed": boolean,
  "created_at": string (ISO 8601 datetime)
}
```

### Error Response
```json
{
  "error": string,
  "code": string
}
```

## Validation Rules
- All string inputs are trimmed of leading/trailing whitespace
- Task IDs are auto-incrementing integers starting from 1
- Task titles are required and must not be empty
- Task titles must not exceed 100 characters
- Task descriptions are optional but must not exceed 500 characters
- Task completion status is a boolean (false by default)