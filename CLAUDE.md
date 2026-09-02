# Microsoft Fabric Presales Technical Team — CLAUDE.md

This repo is a **Claude Code agent team** that operates as a presales technical squad for Microsoft Fabric engagements. Four specialist subagents collaborate to produce client-ready SOWs, work breakdown structures, and presales-to-delivery handover decks.

## The team

| Agent | Role |
|---|---|
| `assessment-pov-sow-writer` | Drafts Assessment & POV/POC SOWs (4–6 week engagements) |
| `implementation-sow-writer` | Drafts full Implementation SOWs (13–28 week engagements, multiple archetypes) |
| `wbs-architect` | Builds detailed multi-sheet WBS in Excel with resource loading and governance tabs |
| `handover-ppt-builder` | Builds the presales-to-delivery handover deck (PowerPoint) |

See `.claude/agents/*.md` for full agent definitions.

## How to invoke

**Pipeline (recommended):**
```
/generate-fabric-docs --brief examples/sample-brief.md --track full
```

**Individual agents:** Just describe what you need ("draft an assessment SOW for this client…") and Claude will route to the right agent.

## Critical references

Every agent reads from `templates/` for canonical structure:

- `templates/assessment-pov-sow-structure.md` — extracted from real APEX + NYULH SOWs
- `templates/implementation-sow-structure.md` — extracted from real Lids Phase 1, Phase 2, Emory, ACME SOWs
- `templates/wbs-structure.md` — extracted from real Lids HLPP, Apex, Emory project plans
- `templates/resource-roles.md` — 33 distinct roles across 10 docs, normalized to 11 canonical
- `templates/common-patterns.md` — boilerplate clauses, change orders, payment terms
- `templates/fabric-domain-reference.md` — Fabric workloads, capacity SKUs, funding mechanisms

## Source-of-truth rule

When agents produce SOW/WBS/PPT content, every datum must trace back to:
1. The user's engagement brief, OR
2. The extracted templates in `templates/`, OR
3. An explicit user response to an `AskUserQuestion` prompt

**Never invent** dollar amounts, dates, client names, inventory counts, or capacity recommendations. Use `[TBD: ___]` placeholders for unresolved items and surface them at the end.

## Outputs

All generated artifacts go to `outputs/`:
- `.docx` SOWs (assessment, implementation)
- `.xlsx` WBS
- `.pptx` handover deck
- `outputs/diagrams/*.png` rendered Mermaid architecture and process-flow diagrams

`outputs/` is gitignored — these are per-engagement artifacts, not source.

## Fabric notebooks (`notebooks/`)

A parameter-driven Fabric notebook pipeline that is independent of the SOW agents:
`01_lakehouse_data_profiling` → `02_logical_model_design` → `03_build_dim_fact_model` → `04_semantic_model_deploy`
(plus `00_generate_sample_data` and `05_run_pipeline`). It profiles every Delta table in a Lakehouse, proposes a
star-schema logical model (`Files/model/model_spec.json`), builds `gold.dim_*` / `gold.fact_*` tables, and creates a
Direct Lake semantic model with Semantic Link Labs. Details and design decisions are in `notebooks/README.md`.
When editing these notebooks, keep every notebook runnable from its tagged `parameters` cell and keep notebooks 01–03
free of Fabric-only dependencies (they are tested locally on PySpark + Delta).

## Tools the agents use

- **python-docx** — DOCX generation
- **openpyxl** — XLSX generation (WBS)
- **python-pptx** — PPTX generation (handover deck)
- **Mermaid CLI (`mmdc`)** — Architecture / process-flow diagram rendering via `scripts/render_diagram.py`

## Domain coverage

The team is specialized for **Microsoft Fabric** migrations and implementations:
- OneLake, Lakehouse, Warehouse
- Bronze/Silver/Gold (and Emory-style 4-layer Platinum)
- Power BI with Direct Lake semantic models
- Copilot in Fabric / Power BI
- Purview governance
- Fabric Data Factory pipelines
- F-SKU capacity sizing (F2–F2048)
- Microsoft Partner Funding (PLF, Azure Accelerate, ACMA)

If a brief is NOT Fabric-related (e.g., Databricks-only, Snowflake-only), the agents should flag this and offer to adapt or recommend a different tooling stack.
