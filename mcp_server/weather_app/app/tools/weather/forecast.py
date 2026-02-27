from app.server import mcp
# from app.config import NWS_API_BASE
from weather_app.app.utils.http_client import make_nws_request

# @mcp.tool()
# async def get_forecast(latitude: float, longitude: float) -> str:
#     """
#     Get weather forecast for a specific latitude and longitude.
#     """
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_nws_request(points_url)

#     if not points_data:
#         return "Unable to fetch location data."

#     forecast_url = points_data["properties"].get("forecast")
#     if not forecast_url:
#         return "Forecast URL not available for this location."

#     forecast_data = await make_nws_request(forecast_url)
#     if not forecast_data:
#         return "Unable to fetch forecast."

#     periods = forecast_data["properties"].get("periods", [])[:5]

#     output = []
#     for period in periods:
#         output.append(
#             f"{period['name']}:\n"
#             f"Temperature: {period['temperature']}°{period['temperatureUnit']}\n"
#             f"Wind: {period['windSpeed']} {period['windDirection']}\n"
#             f"Forecast: {period['detailedForecast']}"
#         )

#     return "\n\n---\n\n".join(output)

@mcp.tool()
async def get_forecast(location: str, days: int = 3):
    # """
    # Get weather forecast for the next few days.

    # Args:
    #     location: City or place name
    #     days: Number of days to forecast (default 3)
    # """
    data = await make_nws_request(
        "forecast.json",
        {"q": location, "days": days}
    )

    if not data:
        return { "error": "Unable to fetch forecast" }

    forecast_days = []

    for day in data["forecast"]["forecastday"]:
        d = day["day"]
        forecast_days.append({
            "date": day["date"],
            "max_temp": d["maxtemp_c"],
            "min_temp": d["mintemp_c"],
            "condition": d["condition"]["text"]
        })

    return {
        "location": location,
        "days": days,
        "forecast": forecast_days
    }

