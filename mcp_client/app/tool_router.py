WEATHER_TOOLS = {
    "get_weather_summary",
    "get_forecast",
}

DB_TOOLS = {
    "mongo_crud",
    "create_collection",
    "get_db_schema",
    "get_total_collections",
}

WALLET_TOOLS = {
    "get_wallet_balance",
}


def detect_domain(query: str) -> str:
    q = query.lower()

    if "weather" in q or "forecast" in q:
        return "weather"

    if "db" in q or "user" in q or "db" in q or "collection" in q:
        return "db"

    if "wallet" in q or "balance" in q:
        return "wallet"

    return "general"


def filter_tools(all_tools, domain: str):
    if domain == "weather":
        return [t for t in all_tools if t.name in WEATHER_TOOLS]

    if domain == "db":
        return [t for t in all_tools if t.name in DB_TOOLS]

    if domain == "wallet":
        return [t for t in all_tools if t.name in WALLET_TOOLS]

    return []
