# Quickstart Guide: Todo Console Application

## Prerequisites
- Python 3.11 or higher
- pip package manager
- uv package manager (optional but recommended)

## Setup

### Option 1: Using uv (recommended)
```bash
# Install uv if you don't have it
pip install uv

# Clone the repository
git clone <repository-url>
cd todo-console-app

# Install dependencies
uv sync

# Run the application
uv run python src/todo_app.py
```

### Option 2: Using pip
```bash
# Clone the repository
git clone <repository-url>
cd todo-console-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/todo_app.py
```

## Usage

Once the application is running, you'll see a prompt where you can enter commands:

```
> help
```
Shows available commands.

```
> add
```
Prompts you to enter a task title and description.

```
> view
```
Displays all tasks with their status (completed/incomplete).

```
> update
```
Prompts you to enter a task ID and new details.

```
> delete
```
Prompts you to enter a task ID to delete.

```
> toggle
```
Prompts you to enter a task ID to toggle its completion status.

```
> quit
```
Exits the application.

## Example Workflow

1. Add a task:
   ```
   > add
   Enter task title: Buy groceries
   Enter task description: Milk, bread, eggs, fruits
   Task added successfully with ID: 1
   ```

2. View all tasks:
   ```
   > view
   [Displays all tasks with their status]
   ```

3. Mark a task as complete:
   ```
   > toggle
   Enter task ID to toggle: 1
   Task with ID 1 marked as complete.
   ```

## Troubleshooting

- If you get an import error for 'rich', make sure you've installed the dependencies with `pip install -r requirements.txt`
- If the application doesn't start, verify you're using Python 3.11 or higher
- For any command, if you enter invalid input, the application will show an appropriate error message