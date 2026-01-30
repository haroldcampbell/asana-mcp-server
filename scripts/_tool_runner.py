import argparse
import json
from typing import Any, Callable, Dict


def load_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.payload_file:
        with open(args.payload_file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    if args.payload:
        return json.loads(args.payload)
    return {}


def run_tool(tool_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", help="JSON payload string", default=None)
    parser.add_argument("--payload-file", help="Path to JSON payload file", default=None)
    args = parser.parse_args()

    payload = load_payload(args)
    result = tool_fn(payload)
    print(json.dumps(result, indent=2, sort_keys=True))
