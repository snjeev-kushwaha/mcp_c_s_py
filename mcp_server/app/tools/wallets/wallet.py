from app.server import mcp
from app.utils.http_client import make_api_call

@mcp.tool()
async def get_wallet_balance(sv_id: str, wallet_name: str) -> str:
    """
    Get wallet balance for a service account and wallet.

    Args:
        sv_id: Service account ID
        wallet_name: Wallet identifier
    """
    url = f"http://localhost:6000/wallets/{sv_id}/{wallet_name}/balance-enquiry"
    data = await make_api_call(url)

    if not data:
        return { "error": "Failed to fetch wallet balance" }

    return {
        "sv_id": sv_id,
        "wallet_name": wallet_name,
        "available_balance": data.get("availableBalance")
    }