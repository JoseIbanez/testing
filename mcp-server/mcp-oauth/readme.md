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

## Secrets
Configure mcp-agent secrets:

```bash 

mkdir -p ~/.config/mcp

cat <<EOF > ~/.config/mcp/elastic_mpn
{
  "username": "....",
  "password": "...." 
}
EOF

cat <<EOF > ~/.config/mcp/jira
{
"auth_token": "O...C"
}
EOF

```


# local test
Before configure a real mcp-client

```bash
export ES_URL=https://beceea2874d94e448c312e0450bde5fc.eu-west-1.aws.found.io:9243
export JIRA_URL=https://jira.tools.aws.vodafone.com

uv run oauth_server.py



uv  --directory ~/Projects/aviva/k8s-hello-world/mcp-mpn-server/ run mcp_server.py
```


# mcp inspector 

Console 1
```bash
npx @modelcontextprotocol/inspector
```


Console 2
```bash
uv run oauth_server.py
```
