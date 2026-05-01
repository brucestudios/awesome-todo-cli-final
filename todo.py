#!/usr/bin/env python3
"""
Awesome TODO CLI - A simple command-line TODO application.
"""

import json
import os
import sys
from typing import List, Dict

TODO_FILE = os.path.join(os.path.dirname(__file__), 'todos.json')

def load_todos() -> List[Dict]:
    """Load TODO items from the JSON file."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos: List[Dict]) -> None:
    """Save TODO items to the JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def add_todo(description: str) -> None:
    """Add a new TODO item."""
    todos = load_todos()
    todos.append({
        'id': len(todos) + 1,
        'description': description,
        'completed': False
    })
    save_todos(todos)
    print(f'Added: "{description}"')

def list_todos() -> None:
    """List all TODO items."""
    todos = load_todos()
    if not todos:
        print("No TODOs found.")
        return

    print("\nTODOs:")
    for todo in todos:
        status = "✓" if todo['completed'] else " "
        print(f"{todo['id']}. [{status}] {todo['description']}")

def complete_todo(todo_id: int) -> None:
    """Mark a TODO as complete."""
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            save_todos(todos)
            print(f'Completed TODO {todo_id}: "{todo["description"]}"')
            return
    print(f'TODO with ID {todo_id} not found.')

def remove_todo(todo_id: int) -> None:
    """Remove a TODO item."""
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            removed = todos.pop(i)
            # Reassign IDs
            for idx, t in enumerate(todos, start=1):
                t['id'] = idx
            save_todos(todos)
            print(f'Removed: "{removed["description"]}"')
            return
    print(f'TODO with ID {todo_id} not found.')

def print_help() -> None:
    """Print help message."""
    print(__doc__)
    print("Usage:")
    print("  todo.py add <description>   Add a new TODO")
    print("  todo.py list                List all TODOs")
    print("  todo.py complete <id>       Mark a TODO as complete")
    print("  todo.py remove <id>         Remove a TODO")
    print("  todo.py --help              Show this help message")

def main() -> None:
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: Please provide a description for the TODO.")
            sys.exit(1)
        description = ' '.join(sys.argv[2:])
        add_todo(description)
    elif command == 'list':
        list_todos()
    elif command == 'complete':
        if len(sys.argv) < 3:
            print("Error: Please provide a TODO ID to complete.")
            sys.exit(1)
        try:
            todo_id = int(sys.argv[2])
            complete_todo(todo_id)
        except ValueError:
            print("Error: TODO ID must be a number.")
            sys.exit(1)
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("Error: Please provide a TODO ID to remove.")
            sys.exit(1)
        try:
            todo_id = int(sys.argv[2])
            remove_todo(todo_id)
        except ValueError:
            print("Error: TODO ID must be a number.")
            sys.exit(1)
    elif command in ('--help', '-h'):
        print_help()
    else:
        print(f"Error: Unknown command '{command}'")
        print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()