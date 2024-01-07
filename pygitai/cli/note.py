import click
from pathlib import Path


# # Ensure the cache directory exists
# Path(cache_dir).mkdir(parents=True, exist_ok=True)

# # Define the tasks file path
# tasks_file = os.path.join(cache_dir, "tasks.json")


# def _load_tasks():
#     """Load tasks from the tasks file."""
#     try:
#         with open(tasks_file, "r") as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []


# def save_tasks(tasks):
#     """Save tasks to the tasks file."""
#     with open(tasks_file, "w") as file:
#         json.dump(tasks, file, indent=2)


# @click.argument("task")
# def add(task):
#     """Add a new task to the to-do list."""
#     tasks.append(task)
#     save_tasks(tasks)
#     click.echo(f'Task "{task}" added to the to-do list.')


# def list():
#     """List all tasks in the to-do list."""
#     if tasks:
#         click.echo("To-Do List:")
#         for i, task in enumerate(tasks, start=1):
#             click.echo(f"{i}. {task}")
#     else:
#         click.echo("No tasks in the to-do list.")


# @click.argument("task_number", type=int)
# def remove(task_number):
#     """Remove a task from the to-do list."""
#     if 1 <= task_number <= len(tasks):
#         removed_task = tasks.pop(task_number - 1)
#         save_tasks(tasks)
#         click.echo(f'Task "{removed_task}" removed from the to-do list.')
#     else:
#         click.echo("Invalid task number.")


@click.command("note")
@click.help_option("-h", "--help", help="help page for `git note` command")
def note():
    """
    Command to add devnotes for users

    To manage notes and add ToDo for the branch and projects. The aim is to allow effective management of projects and extendable API which can be used by LLMs and bots for increasing efficiency for one dev and devs working in teams. Hopefully people will like this feature. If you would like it to be removed or propose some changes, please write me an email or raise an issue.
    """

    return NotImplementedError
