import json

def normalize_tool_args(args: dict) -> dict:
    if "limit" in args and not isinstance(args["limit"], int):
        args["limit"] = 10

    if "filter" in args and isinstance(args["filter"], str):
        try:
            args["filter"] = json.loads(args["filter"])
        except Exception:
            args["filter"] = {}

    if "data" in args and isinstance(args["data"], str):
        try:
            args["data"] = json.loads(args["data"])
        except Exception:
            args["data"] = {}

    return args
