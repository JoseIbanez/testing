

# Ref:
https://modelcontextprotocol.io/quickstart/client


# Create environment
uv init mcp-mpn-server
cd mcp-mpn-server
uv venv

source .venv/bin/activate
uv add mcp anthropic elasticsearch==7


# Update after clone
uv venv
source .venv/bin/activate
uv sync



# local test
