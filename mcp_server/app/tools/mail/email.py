from app.server import mcp
import httpx

@mcp.tool()
async def send_email(
    to: str,
    subject: str,
    body: str,
) -> str:
    """
    Send an email using the mail microservice.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email content (plain text)
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:4001/send-mail",
                json={
                    "to": to,
                    "subject": subject,
                    "text": body,
                },
                timeout=10
            )

        data = response.json()

        if data.get("success"):
            return "Email sent successfully."
        else:
            return f"Mail failed: {data.get('error')}"

    except Exception as e:
        return f"Mail service error: {str(e)}"