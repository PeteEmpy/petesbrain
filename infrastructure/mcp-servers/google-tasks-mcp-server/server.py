"""Google Tasks MCP Server

Provides tools for managing Google Tasks through MCP.
"""

from mcp.server.fastmcp import FastMCP
from googleapiclient.errors import HttpError
from tasks_service import tasks_service
from typing import Optional

mcp = FastMCP("Google Tasks Controller")


@mcp.tool(
    name="list_task_lists",
    description="Lists all task lists in Google Tasks.",
)
def list_task_lists() -> list[dict]:
    """Lists all task lists.

    Returns:
        A list of task lists with their IDs and titles.
    """
    try:
        service = tasks_service()
        results = service.tasklists().list(maxResults=100).execute()
        items = results.get('items', [])

        return [
            {"id": item["id"], "title": item["title"]}
            for item in items
        ]
    except HttpError as err:
        return [{"error": f"Error listing task lists: {str(err)}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {str(e)}"}]


@mcp.tool(
    name="create_task_list",
    description="Creates a new task list in Google Tasks.",
)
def create_task_list(title: str) -> dict:
    """Creates a new task list.

    Args:
        title: The title of the new task list.

    Returns:
        The created task list with its ID and title.
    """
    try:
        service = tasks_service()
        task_list = {"title": title}
        result = service.tasklists().insert(body=task_list).execute()

        return {
            "id": result["id"],
            "title": result["title"],
            "message": f"Task list '{title}' created successfully"
        }
    except HttpError as err:
        return {"error": f"Error creating task list: {str(err)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool(
    name="list_tasks",
    description="Lists all tasks in a specific task list.",
)
def list_tasks(tasklist_id: str, show_completed: bool = False) -> list[dict]:
    """Lists tasks in a task list.

    Args:
        tasklist_id: The ID of the task list.
        show_completed: Whether to show completed tasks (default: False).

    Returns:
        A list of tasks with their details.
    """
    try:
        service = tasks_service()

        params = {
            "tasklist": tasklist_id,
            "maxResults": 100
        }

        if show_completed:
            params["showCompleted"] = True

        results = service.tasks().list(**params).execute()
        items = results.get('items', [])

        tasks = []
        for item in items:
            task = {
                "id": item["id"],
                "title": item["title"],
                "status": item.get("status", "needsAction"),
            }

            if "notes" in item:
                task["notes"] = item["notes"]
            if "due" in item:
                task["due"] = item["due"]

            tasks.append(task)

        return tasks
    except HttpError as err:
        return [{"error": f"Error listing tasks: {str(err)}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {str(e)}"}]


@mcp.tool(
    name="create_task",
    description="Creates a new task in Google Tasks.",
)
def create_task(
    tasklist_id: str,
    title: str,
    notes: Optional[str] = None,
    due: Optional[str] = None
) -> dict:
    """Creates a new task.

    Args:
        tasklist_id: The ID of the task list to add the task to.
        title: The title of the task.
        notes: Optional notes/description for the task.
        due: Optional due date in RFC 3339 format (e.g., "2025-10-29T00:00:00Z").

    Returns:
        The created task with its ID and details.
    """
    try:
        service = tasks_service()

        task = {"title": title}

        if notes:
            task["notes"] = notes
        if due:
            task["due"] = due

        result = service.tasks().insert(
            tasklist=tasklist_id,
            body=task
        ).execute()

        return {
            "id": result["id"],
            "title": result["title"],
            "status": result.get("status", "needsAction"),
            "message": f"Task '{title}' created successfully"
        }
    except HttpError as err:
        return {"error": f"Error creating task: {str(err)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool(
    name="update_task",
    description="Updates an existing task in Google Tasks.",
)
def update_task(
    tasklist_id: str,
    task_id: str,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    status: Optional[str] = None,
    due: Optional[str] = None
) -> dict:
    """Updates a task.

    Args:
        tasklist_id: The ID of the task list.
        task_id: The ID of the task to update.
        title: Optional new title for the task.
        notes: Optional new notes for the task.
        status: Optional status ("needsAction" or "completed").
        due: Optional due date in RFC 3339 format.

    Returns:
        The updated task details.
    """
    try:
        service = tasks_service()

        # Get existing task
        task = service.tasks().get(
            tasklist=tasklist_id,
            task=task_id
        ).execute()

        # Update fields
        if title:
            task["title"] = title
        if notes is not None:
            task["notes"] = notes
        if status:
            task["status"] = status
        if due:
            task["due"] = due

        # Update task
        result = service.tasks().update(
            tasklist=tasklist_id,
            task=task_id,
            body=task
        ).execute()

        return {
            "id": result["id"],
            "title": result["title"],
            "status": result.get("status"),
            "message": "Task updated successfully"
        }
    except HttpError as err:
        return {"error": f"Error updating task: {str(err)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool(
    name="complete_task",
    description="Marks a task as completed in Google Tasks.",
)
def complete_task(tasklist_id: str, task_id: str) -> dict:
    """Marks a task as completed.

    Args:
        tasklist_id: The ID of the task list.
        task_id: The ID of the task to complete.

    Returns:
        Confirmation message.
    """
    try:
        service = tasks_service()

        task = service.tasks().get(
            tasklist=tasklist_id,
            task=task_id
        ).execute()

        task["status"] = "completed"

        result = service.tasks().update(
            tasklist=tasklist_id,
            task=task_id,
            body=task
        ).execute()

        return {
            "id": result["id"],
            "title": result["title"],
            "status": "completed",
            "message": f"Task '{result['title']}' marked as completed"
        }
    except HttpError as err:
        return {"error": f"Error completing task: {str(err)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool(
    name="delete_task",
    description="Deletes a task from Google Tasks.",
)
def delete_task(tasklist_id: str, task_id: str) -> dict:
    """Deletes a task.

    Args:
        tasklist_id: The ID of the task list.
        task_id: The ID of the task to delete.

    Returns:
        Confirmation message.
    """
    try:
        service = tasks_service()

        # Get task title before deleting
        task = service.tasks().get(
            tasklist=tasklist_id,
            task=task_id
        ).execute()

        title = task.get("title", "Unknown")

        service.tasks().delete(
            tasklist=tasklist_id,
            task=task_id
        ).execute()

        return {
            "message": f"Task '{title}' deleted successfully"
        }
    except HttpError as err:
        return {"error": f"Error deleting task: {str(err)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


if __name__ == "__main__":
    print("Starting Google Tasks MCP Server...")
    print("Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.")
    mcp.run(transport="stdio")
