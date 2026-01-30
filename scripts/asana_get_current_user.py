from scripts._tool_runner import run_tool
from src.tool_impl import get_current_user


if __name__ == "__main__":
    run_tool(get_current_user)
