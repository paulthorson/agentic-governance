#!/usr/bin/env python3
"""Agent-side checks for the hardened macOS install (ADR-0013).

Run as an ordinary user (NOT the service user, NOT root) against a hardened
install. Talks to the MCP server over HTTP exactly as an agent would.

Env:
  URL      http://127.0.0.1:<port>/mcp
  BEARER   transport token (operator hands it to agents)
  ENG      worker token (team-a, roles engineer, principal rt-a)
  CRIT     reviewer token (team-a, review:engineer, principal rt-b)
  TWIN     reviewer token sharing the worker's principal (rt-a)

Prints PASS/FAIL lines; exits 1 if anything failed.
"""
import asyncio
import json
import os
import sys
import urllib.error
import urllib.request

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ["URL"]
BEARER = os.environ["BEARER"]
ENG, CRIT, TWIN = os.environ["ENG"], os.environ["CRIT"], os.environ["TWIN"]
FAILS = 0


def check(name, cond, detail=""):
    global FAILS
    if cond:
        print(f"PASS: {name}")
    else:
        FAILS += 1
        print(f"FAIL: {name} {detail}")


def http_status(headers):
    req = urllib.request.Request(URL, data=b"{}", method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def unwrap(result):
    sc = getattr(result, "structuredContent", None)
    if isinstance(sc, dict):
        return sc["result"] if set(sc) == {"result"} else sc
    for c in result.content or []:
        text = getattr(c, "text", None)
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"_text": text}
    return {}


async def main():
    check("no bearer token is rejected (401)", http_status({}) == 401)
    check("wrong bearer token is rejected (401)", http_status({"Authorization": "Bearer nope"}) == 401)

    async with streamablehttp_client(URL, headers={"Authorization": f"Bearer {BEARER}"}) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name for t in (await s.list_tools()).tools}
            check("ticket tools exposed", {"ticket_claim_next", "ticket_submit", "ticket_verdict", "ticket_verify"} <= tools)
            check("no operator tools over MCP",
                  not any(k in name for name in tools for k in ("clear_veto", "resolve", "override", "integrity_accept", "agent_add")),
                  str(sorted(tools)))

            async def call(tool, **args):
                return unwrap(await s.call_tool(tool, args))

            res = await call("ticket_create", title="e2e", stage="engineer", team="team-a",
                             end_stage="engineer", agent_token=ENG)
            check("create with worker token", res.get("status") == "created", res)

            res = await call("ticket_create", title="anon", stage="engineer", team="team-a")
            check("create without token refused", res.get("status") == "refused", res)

            res = await call("ticket_claim_next", role="engineer", team="team-a", agent_token="not-a-token")
            check("bogus agent token refused", res.get("status") == "refused", res)

            res = await call("ticket_claim_next", role="engineer", team="team-a", agent_id="eng-1")
            check("claim by name without token refused", res.get("status") == "refused", res)

            res = await call("ticket_claim_next", role="engineer", agent_token=ENG)
            check("worker claims with its token", res.get("status") == "claimed", res)
            tid = (res.get("ticket") or {}).get("identifier", "T-1")

            res = await call("ticket_submit", ticket=tid, summary="did it", deliverable="the work", agent_token=ENG)
            check("worker submits with deliverable", res.get("status") == "submitted", res)

            res = await call("ticket_claim_next", role="engineer", mode="review", agent_token=TWIN)
            check("same-principal reviewer gets nothing", res.get("status") == "empty", res)

            res = await call("ticket_claim_next", role="engineer", mode="review", agent_token=CRIT)
            check("independent reviewer claims", res.get("status") == "claimed", res)
            sub = (res.get("ticket") or {}).get("submission") or {}
            check("reviewer sees the deliverable", sub.get("deliverable") == "the work", sub)
            check("review is blind (no worker summary)", "summary" not in sub and "did it" not in json.dumps(res), sub)

            res = await call("ticket_verdict", ticket=tid, verdict="PASS", agent_token=CRIT)
            check("reviewer PASS closes the ticket",
                  res.get("status") == "recorded" and (res.get("ticket") or {}).get("state") == "done", res)

            res = await call("overturn_verdict", ticket=tid, reason="an agent tries")
            check("overturn_verdict refused over MCP", res.get("status") == "refused", res)

            res = await call("ticket_verify")
            check("integrity verifies over MCP", res.get("ok") is True, res)

    print(f"client summary: {FAILS} failure(s)")
    sys.exit(1 if FAILS else 0)


asyncio.run(main())
