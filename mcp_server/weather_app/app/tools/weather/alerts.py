from app.server import mcp
# from app.config import NWS_API_BASE
from weather_app.app.utils.http_client import make_nws_request
from weather_app.app.utils.formatters import format_alert

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
    # """
    # Get current weather for a given city.

    # Args:
    #     location: City name like Hyderabad
    # """
    data = await make_nws_request(
        "current.json",
        {"q": location}
    )

    if not data:
         return {
            "error": "Unable to fetch weather data"
        }

    current = data["current"]
    loc = data["location"]

    return {
        "city": loc["name"],
        "country": loc["country"],
        "condition": current["condition"]["text"],
        "temperature_c": current["temp_c"],
        "wind_kph": current["wind_kph"],
        "humidity": current["humidity"]
    }
