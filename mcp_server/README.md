# MCP + Claude Desktop on Windows 11
↓
# Python FastMCP server behavior
↓
# Server disconnected issue
↓
# Absolute vs relative paths
{
  "mcpServers": {
    "weather": {
      "command": "C:/mcp/mcp_server/venv/Scripts/python.exe",
      "args": [
        "-u",
        "C:/mcp/mcp_server/main.py"
      ],
      "cwd": "C:/mcp/mcp_server"
    }
  }
}
↓
# Run python main.py
# NWS (US-only) vs WeatherAPI (global)
# Get Hyderabad (HYD) alerts

# connect mongodb and try to create collection
# write promt like ---
Create a users table with name, email, age, isActive and createdAt
# then claude calls:
create_collection()

# If we want to perform operation like insert, update, delete and get
# then prompt like ----
Add a user named John, age 30, email john@test.com
Show all users older than 25
Update John's age to 31
Delete all inactive users

# Final Recommendation (what I’d do) (openai)
# Today
Single venv
Explicit python path
Logging + debug prints
# Next
Dockerize MCP server
TCP-based MCP connection
# Real Production
One MCP server per container
ENV-based config
Kubernetes / ECS
Health checks
Observability


# How to use jira tools
User says: Log 3 hours on DEV-102
User says:
Agent: Log 3 hours on DEV-102

User says:
Show pending tasks of sanjeev@example.com
User says:
Agent: Show pending tasks of sanjeev@example.com

