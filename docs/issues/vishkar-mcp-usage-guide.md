# VISHKAR MCP Usage Guide

## Overview

All VISHKAR MCP operations should use **Vercel-hosted endpoints** via curl.
Local stdio MCP servers have been removed from `~/.claude/mcp.json`.

## API Key

```
pk_GvylygppALsYfwAIB4sl9WfyEYawntO_doAYHELdDeM
```

## Vercel MCP Endpoints

| MCP | Endpoint | Auth |
|-----|----------|------|
| Project Registry | `https://project-registry-henna.vercel.app/api/mcp` | None |
| Enhanced Context | `https://enhanced-context-mcp.vercel.app/api/mcp` | X-API-Key |
| JIRA | `https://jira-mcp-pi.vercel.app/api/mcp` | Bearer |
| Confluence | `https://confluence-mcp-six.vercel.app/api/mcp` | Bearer |
| Story Crafter | `https://storycrafter-mcp.vercel.app/api/mcp` | X-API-Key |

## Usage Examples

### JIRA - Search Issues
```bash
curl -s -X POST "https://jira-mcp-pi.vercel.app/api/mcp" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer pk_GvylygppALsYfwAIB4sl9WfyEYawntO_doAYHELdDeM" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_issues","arguments":{"jql":"project = V2"}},"id":1}'
```

### JIRA - Create Issue
```bash
curl -s -X POST "https://jira-mcp-pi.vercel.app/api/mcp" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer pk_GvylygppALsYfwAIB4sl9WfyEYawntO_doAYHELdDeM" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"create_issue","arguments":{"projectKey":"V2","issueType":"Epic","summary":"[E2] SDLC Pipeline","description":"17-Step SDLC workflow orchestration"}},"id":1}'
```

### JIRA - Link Story to Epic (Next-Gen Projects)
```bash
# Use update_issue with parentKey to set epic parent
curl -s -X POST "https://jira-mcp-pi.vercel.app/api/mcp" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer pk_GvylygppALsYfwAIB4sl9WfyEYawntO_doAYHELdDeM" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"update_issue","arguments":{"issueKey":"V2-13","parentKey":"V2-9"}},"id":1}'
```

### JIRA - Link Issues (General)
```bash
# Use link_issues for non-parent relationships (Relates, Blocks, etc.)
curl -s -X POST "https://jira-mcp-pi.vercel.app/api/mcp" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer pk_GvylygppALsYfwAIB4sl9WfyEYawntO_doAYHELdDeM" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"link_issues","arguments":{"sourceKey":"V2-2","targetKey":"V2-1","linkType":"Relates"}},"id":1}'
```

### Enhanced Context - Get SDLC Guidance
```bash
curl -s -X POST "https://enhanced-context-mcp.vercel.app/api/mcp" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: pk_GvylygppALsYfwAIB4sl9WfyEYawntO_doAYHELdDeM" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_sdlc_guidance","arguments":{"section":"overview"}},"id":1}'
```

### Confluence - Create Page
```bash
curl -s -X POST "https://confluence-mcp-six.vercel.app/api/mcp" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer pk_GvylygppALsYfwAIB4sl9WfyEYawntO_doAYHELdDeM" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"create_page","arguments":{"spaceKey":"V2","title":"Test Page","content":"<p>Content here</p>"}},"id":1}'
```

## Project Configuration

- **JIRA Project Key**: `V2`
- **Confluence Space Key**: `V2`
- **JIRA Host**: `https://bounteous.jira.com`
- **Confluence URL**: `https://bounteous.jira.com/wiki`

## Why Not Local MCP Servers?

1. **Consistency**: Everyone uses the same Vercel-hosted endpoints
2. **No Docker required**: No local containers to manage
3. **Centralized config**: API key from Project Registry works everywhere
4. **Single source of truth**: VISHKAR ecosystem is the authoritative source

## Backup Location

Previous local MCP config backed up to:
`~/.claude/mcp.json.backup.*`
