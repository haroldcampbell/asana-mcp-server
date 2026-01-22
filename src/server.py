from mcp.server.fastmcp import FastMCP

from src.config import get_settings
from src.logging_utils import setup_logging
from src.tools import register_tools


def create_server() -> FastMCP:
    settings = get_settings()
    setup_logging(settings.log_file, settings.log_level)
    mcp = FastMCP("asana-mcp")
    register_tools(mcp)
    return mcp


if __name__ == "__main__":
    server = create_server()
    server.run()
