from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from src.asana_client import AsanaClient, AsanaError
from src.logging_utils import audit
from src.logging_utils import redact_dict
import os
from src.logging_utils import setup_logging


_LOGGER = None


def get_logger():
    global _LOGGER
    if _LOGGER is None:
        log_file = os.getenv("LOG_FILE", "logs/asana-mcp.log")
        log_level = os.getenv("LOG_LEVEL", "INFO")
        _LOGGER = setup_logging(log_file, log_level)
    return _LOGGER


def ok(data: Any) -> Dict[str, Any]:
    return {"status": "ok", "data": data}


def err(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload = {"code": code, "message": message}
    if details:
        payload["details"] = details
    return {"status": "error", "error": payload}


@lru_cache
def get_client() -> AsanaClient:
    return AsanaClient()


class ListWorkspacesInput(BaseModel):
    opt_fields: Optional[str] = None


class GetCurrentUserInput(BaseModel):
    opt_fields: Optional[str] = None


class ListProjectsInput(BaseModel):
    workspace_gid: str = Field(min_length=1)
    archived: Optional[bool] = None
    limit: Optional[int] = Field(default=None, ge=1, le=100)
    opt_fields: Optional[str] = None


class GetTaskInput(BaseModel):
    task_gid: str = Field(min_length=1)
    opt_fields: Optional[str] = None


class SearchTasksInput(BaseModel):
    workspace_gid: str = Field(min_length=1)
    text: Optional[str] = None
    assignee: Optional[str] = None
    projects: Optional[str] = None
    completed_since: Optional[str] = None
    limit: Optional[int] = Field(default=None, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_ascending: Optional[bool] = None
    opt_fields: Optional[str] = None


class CreateTaskInput(BaseModel):
    name: str = Field(min_length=1)
    workspace: Optional[str] = None
    projects: Optional[list[str]] = None
    notes: Optional[str] = None
    assignee: Optional[str] = None
    due_on: Optional[str] = None
    start_on: Optional[str] = None
    parent: Optional[str] = None


class UpdateTaskInput(BaseModel):
    task_gid: str = Field(min_length=1)
    name: Optional[str] = None
    workspace: Optional[str] = None
    projects: Optional[list[str]] = None
    notes: Optional[str] = None
    assignee: Optional[str] = None
    due_on: Optional[str] = None
    start_on: Optional[str] = None
    parent: Optional[str] = None


class DeleteTaskInput(BaseModel):
    task_gid: str = Field(min_length=1)


def list_workspaces(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = ListWorkspacesInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.list_workspaces", data)
    try:
        response = get_client().request("GET", "/workspaces", params=data or None)
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})


def get_current_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = GetCurrentUserInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.get_current_user", data)
    try:
        response = get_client().request("GET", "/users/me", params=data or None)
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})


def list_projects(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = ListProjectsInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.list_projects", data)
    workspace_gid = data.pop("workspace_gid")
    try:
        response = get_client().request(
            "GET",
            f"/workspaces/{workspace_gid}/projects",
            params=data or None,
        )
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})


def get_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = GetTaskInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.get_task", data)
    task_gid = data.pop("task_gid")
    try:
        response = get_client().request(
            "GET",
            f"/tasks/{task_gid}",
            params=data or None,
        )
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})


def search_tasks(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = SearchTasksInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.search_tasks", data)
    workspace_gid = data.pop("workspace_gid")
    try:
        response = get_client().request(
            "GET",
            f"/workspaces/{workspace_gid}/tasks/search",
            params=data or None,
        )
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})


def create_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = CreateTaskInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.create_task", data)
    try:
        response = get_client().request("POST", "/tasks", payload={"data": data})
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})


def update_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = UpdateTaskInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.update_task", data)
    task_gid = data.pop("task_gid")
    try:
        response = get_client().request(
            "PUT",
            f"/tasks/{task_gid}",
            payload={"data": data},
        )
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})


def delete_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = DeleteTaskInput(**payload).model_dump(exclude_none=True)
    audit(get_logger(), "asana.delete_task", data)
    task_gid = data.get("task_gid")
    try:
        response = get_client().request("DELETE", f"/tasks/{task_gid}")
        return ok(response)
    except AsanaError as exc:
        return err("asana_error", str(exc), {"status_code": exc.status_code, "details": redact_dict(exc.details)})
