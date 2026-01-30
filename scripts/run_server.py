import sys


try:
    from src.server import main as server_main
except ModuleNotFoundError as exc:
    if exc.name == "mcp":
        print(
            "Missing dependency: mcp. Install with `uv sync` (or `uv sync --group dev`).",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    raise


def main() -> None:
    server_main()


if __name__ == "__main__":
    main()
