import os.path
import json
from data_structures.task_tree import TaskTree

def load() -> TaskTree:
    """Load saved tasks from file."""
    tasks = TaskTree()

    if os.path.exists('saved_tasks.json'):
        with open('saved_tasks.json', 'r') as f:
            try:
                tasks = TaskTree.from_JSON_object(json.load(f))
            except ValueError as e:
                print(f"Error loading tasks, tasks.json may have been corrupted and is no longer valid:\n{e}")

    return tasks

def save(tasks: TaskTree) -> None:
    """Save tasks to file."""
    with open('saved_tasks.json', 'w') as f:
        json.dump(tasks.as_JSON_object(), f, indent=3)