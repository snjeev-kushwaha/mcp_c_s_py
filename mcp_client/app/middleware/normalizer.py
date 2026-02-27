def normalize_mongo_args(args: dict):
    if not isinstance(args.get("filter"), dict):
        args["filter"] = {}

    if not isinstance(args.get("data"), (dict, list)):
        args["data"] = None

    if not isinstance(args.get("update"), dict):
        args["update"] = None

    if not isinstance(args.get("limit"), int):
        args["limit"] = 10

    return args
