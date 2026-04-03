# Pinvestigator MCP Setup Guide

## Required MCP Servers

Pinvestigator requires two MCP servers:

| Server | Header Value | Purpose |
|--------|-------------|---------|
| Presto | `presto-prod` | Query Hive engagement and holdout tables |
| Slack | `slack-prod` | Search channels for launches, experiments, alerts |

## Configuration

MCP servers are configured globally in `~/.claude.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "presto": {
      "type": "http",
      "url": "http://localhost:9092/mcp",
      "headers": {
        "mcp-server": "presto-prod"
      }
    },
    "slack": {
      "type": "http",
      "url": "http://localhost:9092/mcp",
      "headers": {
        "mcp-server": "slack-prod"
      }
    }
  }
}
```

Project-level permissions in `.claude/settings.local.json` must include:

```json
{
  "permissions": {
    "allow": [
      "mcp__presto__*",
      "mcp__slack__*"
    ]
  }
}
```

## Prerequisites

- The MCP proxy must be running on `localhost:9092`. This is typically started by Pinterest's devtools setup.
- Presto access requires valid authentication (JWT via Knox).
- Slack access requires Slack OAuth tokens configured on the MCP gateway.

## Verification

Test MCP connectivity with these queries:

**Presto:**
```
SELECT MAX(dt) FROM homefeed.pinvestigator_engagement
```
Expected: Returns a date string. If connection fails, verify the proxy is running.

**Slack:**
```
get_channel_history(channel="C06K41EHY", oldest="<7 days ago unix ts>", latest="<now unix ts>", inclusive=true, limit=5)
```
Expected: Returns up to 5 Slack messages. If access denied, verify Slack OAuth.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `Bad Request: No valid session ID` | Old Claude Code version | Update to v2.1.30+ |
| Connection refused on :9092 | Proxy not running | Start Pinterest devtools proxy |
| Empty results from Presto | Wrong `dt` filter format or date out of range | Use `DATE 'YYYY-MM-DD'` format; data starts 2025-01-12 |
| Slack returns 0 messages | Channel access not configured | Check Slack OAuth scope on MCP gateway |
