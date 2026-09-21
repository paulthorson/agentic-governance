# Multi-project local registry

**Project:** Standing AG (cross-project) 
**Filed:** 2026-09-21 (Standing AG — anonymized process lock) 
**Status:** DRAFT until Chief of Staff ACCEPT merge cites a merged SHA 
**Kind:** process lock / repository operating practice 
**Lock name:** `MULTI_PROJECT_LOCAL_REGISTRY` 
**Check / sensor:** public framework git stays generic; filled project indexes stay in the product repository 
**Required artifact (product repo):** a local project index in that same repository (for example `PROJECTS.md` or an equivalent context map) 
**Metric:** public framework tips that list personal product names or private product paths = **0** (hold) 
**Scope:** any product or work repository that holds more than one distinct project or user-facing surface. Not OpenClaw briefs.

## Bottom line

When one product repository holds several distinct projects or user-facing
surfaces, the installer keeps a local project index **in that repository**.
The public framework records only this generic rule and a placeholder
template. Personal product names, private paths, and other personal data stay
in the product repository.

## Practice

1. If a product or work repository contains more than one distinct project or
   user-facing surface, maintain a local project index in **that** repository.
   Do not maintain the filled index in public Agentic Governance git.
2. Each entry records four fields: project name, path(s), a short purpose, and
   relationships to other projects in the same repository.
3. When a new distinct project or surface is added to a shared repository, add
   or update the matching entry the same day.
4. Public Agentic Governance documents only this rule and the template shape.
   Examples use placeholders such as `Project A` and `path/to/a/`.

## Template shape

Copy [`docs/templates/product-repo-projects.md`](../../../docs/templates/product-repo-projects.md)
into the product repository and replace placeholders there.

| Project | Path(s) | Purpose | Related projects |
|---|---|---|---|
| Project A | `path/to/a/` | Short purpose for surface A | Depends on Project B |
| Project B | `path/to/b/` | Short purpose for surface B | Serves Project A |

## Privacy boundary

This lock **extends** the existing vanilla / working-agreement / feedback
anonymize rule. It does not replace that rule.

For framework purposes, treat the following as personal data:

- operator personal projects
- personal product names
- private product paths
- other operator personal information (names, emails, host paths, secrets)

Public framework git captures anonymized generic learnings and operating
patterns only. A tip that lands personal product names or private product
paths into public Agentic Governance is a miss.

## Agent lock

- **Id:** `MULTI_PROJECT_LOCAL_REGISTRY`
- **Who stamps:** Chief of Staff (primary public-git vanilla gate). Quality
  records a miss on public framework text under review. Adversary may
  challenge. Product teams keep the filled index in the product repository.
- **FAIL:** (1) a shared product/work repository with multiple distinct
  projects or surfaces has no local index and no same-day update after a new
  surface is added; (2) public Agentic Governance git lists personal product
  names, private product paths, or other operator personal data.
- **Stack:** Amends `WORKING_AGREEMENT_FLEET` vanilla lock +
  `COS_FEEDBACK_TO_IMPROVE` anonymize — **not** a second source of truth.
- **P0:** Keep private operator data out of public AG git.
- **Cite:** this standing note + Chief of Staff harness + Quality harness P0 +
  `docs/templates/product-repo-projects.md` + LIVE
  [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17`
  + LIVE [#98](https://github.com/paulthorson/agentic-governance/pull/98) @
  `fe27c4b`.
