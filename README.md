# Microsoft Fabric Presales Technical Agent Team

A team of four specialized Claude Code subagents that act as a presales technical team for Microsoft Fabric engagements. They produce client-ready SOWs, work breakdown structures, and presales-to-delivery handover decks — grounded in real client SOW templates and project plans.

## The team

| Agent | Role | Inputs | Outputs |
|---|---|---|---|
| `assessment-pov-sow-writer` | Drafts Assessment & POV SOWs for early-stage discovery engagements | Client brief, discovery notes | `assessment-pov-sow.docx`, architecture diagram(s), process flow(s) |
| `implementation-sow-writer` | Drafts full Implementation SOWs for delivery engagements | Client brief (+ assessment SOW if available) | `implementation-sow.docx`, architecture diagram(s), process flow(s) |
| `wbs-architect` | Builds detailed Work Breakdown Structures with task list, durations, dependencies, resource assignments | Either or both SOWs | `wbs.xlsx` with phases, tasks, resources, effort |
| `handover-ppt-builder` | Builds the presales→delivery handover deck | SOW(s) + WBS | `presales-to-delivery-handover.pptx` |

All four agents:
- Have **Microsoft Fabric domain knowledge** baked in (workloads, capacity tiers F2-F2048, OneLake, Medallion architecture, Power BI, Purview, Fabric Data Factory, Real-Time Intelligence).
- Use **real client SOW templates** in `templates/` as their structural reference (extracted from 6 SOWs and 4 project plans).
- Can produce **architecture diagrams** and **process flows** using Mermaid (rendered to PNG and embedded in deliverables).

## How to use

### One-shot pipeline (slash command)

```
/generate-fabric-docs --brief examples/sample-brief.md --track full
```

Tracks:
- `assessment` — runs `assessment-pov-sow-writer` only (produces SOW + one-pager + diagrams)
- `implementation` — runs `implementation-sow-writer` → `wbs-architect` → `handover-ppt-builder`
- `full` — runs both tracks end-to-end

### Individual agents

Invoke any agent directly with a brief; chain outputs manually for finer control.

## Directory layout

```
.claude/
  agents/                  # Agent definitions (system prompts + tools)
  commands/                # Slash commands (orchestration)
scripts/                   # Python helpers (DOCX/XLSX/PPTX builders, diagram rendering)
templates/                 # Extracted reference structures from real SOWs/plans
examples/                  # Sample briefs to test the pipeline
outputs/                   # Generated deliverables (gitignored)
```

## Templates source

The team's structural reference is extracted from these real client documents:

**Assessment / POV SOWs**
- APEX SOW — Assessment and POV
- NYULH POC SOW

**Implementation SOWs**
- Phase 1 Microsoft Fabric Migration SOW
- Phase 2 Microsoft Fabric Migration SOW
- Emory SOW — Data Engineering and Power BI Modernization
- ACME Consulting Services SOW3

**Project plans (WBS reference)**
- High Level Project Plan
- Apex Project Plan V7
- Emory TruvizFabric Implementation Project Plan
- Emory Purview Project Plan

These source documents are NOT committed to the repo — only the extracted structural patterns in `templates/`.

## Requirements

- Python 3.11+ with `python-docx`, `openpyxl`, `python-pptx`, `Pillow`
- Node.js with `@mermaid-js/mermaid-cli` (for diagram rendering)
