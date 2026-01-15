from app.server import mcp
# from app.config import NWS_API_BASE
from app.http_client import make_nws_request
from app.formatters import format_alert

# @mcp.tool()
# async def get_alerts(state: str) -> str:
#     """
#     Get active weather alerts for a US state.
#     """
#     url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
#     data = await make_nws_request(url)

#     if not data:
#         return "Failed to fetch alerts from weather service."

#     features = data.get("features", [])
#     if not features:
#         return "No active alerts for this state."

#     alerts = [format_alert(feature) for feature in features]
#     return "\n\n---\n\n".join(alerts)

@mcp.tool()
async def get_weather_summary(location: str) -> str:
    data = await make_nws_request(
        "current.json",
        {"q": location}
    )

    if not data:
        return "Unable to fetch weather data."

    current = data["current"]
    loc = data["location"]

    return (
        f"{loc['name']}, {loc['country']}\n"
        f"Condition: {current['condition']['text']}\n"
        f"Temperature: {current['temp_c']}°C\n"
        f"Wind: {current['wind_kph']} km/h\n"
        f"Humidity: {current['humidity']}%"
    )
