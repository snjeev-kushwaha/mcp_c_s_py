# Python 3.11.4
# server
python -m venv venv
source venv/bin/activate
pip show mcp
pip install -r requirements.txt

# client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# when we develop mcp client and server we have use folder structure like this
C:\mcp
 ├─ venv\
 ├─ mcp_client\
 └─ mcp_server\
