def format_alert(feature: dict) -> str:
    props = feature.get("properties", {})

    return (
        f"Event: {props.get('event', 'Unknown')}\n"
        f"Area: {props.get('areaDesc', 'Unknown')}\n"
        f"Severity: {props.get('severity', 'Unknown')}\n"
        f"Description: {props.get('description', 'No description')}\n"
        f"Instructions: {props.get('instruction', 'None')}"
    )
