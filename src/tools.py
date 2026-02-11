from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from src import tool_impl


def _wrap(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload or {}


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(name="asana_get_current_user", description="Get current Asana user profile")
    def asana_get_current_user(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.get_current_user(_wrap(payload))

    @mcp.tool(name="asana_list_workspaces", description="List Asana workspaces")
    def asana_list_workspaces(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.list_workspaces(_wrap(payload))

    @mcp.tool(name="asana_list_projects", description="List projects in a workspace")
    def asana_list_projects(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.list_projects(_wrap(payload))

    @mcp.tool(name="asana_get_task", description="Get a task by gid")
    def asana_get_task(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.get_task(_wrap(payload))

    @mcp.tool(name="asana_search_tasks", description="Search tasks within a workspace")
    def asana_search_tasks(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.search_tasks(_wrap(payload))

    @mcp.tool(name="asana_create_task", description="Create a task")
    def asana_create_task(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.create_task(_wrap(payload))

    @mcp.tool(name="asana_update_task", description="Update a task")
    def asana_update_task(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.update_task(_wrap(payload))

    @mcp.tool(name="asana_delete_task", description="Delete a task")
    def asana_delete_task(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.delete_task(_wrap(payload))

    @mcp.tool(
        name="asana_move_task_to_section",
        description="Add or move a task to a specific section",
    )
    def asana_move_task_to_section(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.move_task_to_section(_wrap(payload))

    @mcp.tool(
        name="asana_create_task_in_section",
        description="Create a task and add it to a specific section",
    )
    def asana_create_task_in_section(payload: Dict[str, Any]) -> Dict[str, Any]:
        return tool_impl.create_task_in_section(_wrap(payload))
