import argparse
import logging
import os

from mcp.server.fastmcp import FastMCP

from src.config import get_settings
from src.logging_utils import setup_logging
from src.tools import register_tools
from src.version import VERSION


def create_server() -> FastMCP:
    settings = get_settings()
    mcp = FastMCP("asana-mcp")
    register_tools(mcp)
    return mcp


def _print_banner(log_file: str, log_level: str) -> None:
    print(f"Asana MCP server starting (log_file={log_file}, log_level={log_level})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Asana MCP Server")
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit.",
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Validate configuration and exit.",
    )
    args = parser.parse_args()

    if args.version:
        print(VERSION)
        return

    log_file = os.getenv("LOG_FILE", "logs/asana-mcp.log")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    setup_logging(log_file, log_level)

    settings = get_settings()
    logger = logging.getLogger("asana_mcp")

    if args.health_check:
        logger.info("Health check ok.")
        print("ok")
        return

    _print_banner(settings.log_file, settings.log_level)
    logger.info("Asana MCP server starting.")
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
