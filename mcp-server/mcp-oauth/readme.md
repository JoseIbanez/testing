# Ref:
https://modelcontextprotocol.io


## Create environment
When the repo was created

```bash
uv init mcp-oauth
cd  mcp-oauth
uv venv

source .venv/bin/activate
uv add mcp anthropic
```

## Update after clone
If you clone this repo, then create the venv, and install python pkgs

```bash
uv venv
source .venv/bin/activate
uv sync
```



# local test
Before configure a real mcp-client



# mcp inspector 

Console 1
```bash
npx @modelcontextprotocol/inspector
```


Console 2
```bash
uv run oauth_server.py
```
