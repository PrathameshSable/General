---
description: Run the Microsoft Fabric presales pipeline (Assessment/POV SOW, Implementation SOW, WBS, handover deck) end-to-end from an engagement brief
argument-hint: --brief <path> --track <assessment|implementation|full>
---

You are orchestrating the Microsoft Fabric presales technical team. Run the pipeline based on the user's arguments.

## Arguments

Parse from `$ARGUMENTS`:
- `--brief <path>` — path to the engagement brief (defaults to `examples/sample-brief.md`)
- `--track <assessment|implementation|full>` — which pipeline to run (defaults to `full`)
- `--engagement-slug <slug>` — short identifier for output filenames (defaults to slugified client name)

## Pipelines

### `--track assessment`
Run only the Assessment & POV SOW agent. Produces:
- `outputs/<slug>-assessment-pov-sow.docx`
- `outputs/diagrams/<slug>-target-architecture.png`
- `outputs/diagrams/<slug>-process-flow.png`

Optionally: `outputs/<slug>-one-pager.pptx` if the user asks for it.

### `--track implementation`
Run sequentially:
1. `implementation-sow-writer` → `outputs/<slug>-implementation-sow.docx` + diagrams
2. `wbs-architect` → `outputs/<slug>-wbs.xlsx`
3. `handover-ppt-builder` → `outputs/<slug>-handover.pptx`

### `--track full`
Run sequentially:
1. `assessment-pov-sow-writer` → assessment SOW + diagrams
2. `implementation-sow-writer` → implementation SOW + diagrams (consumes assessment outputs)
3. `wbs-architect` → combined Assessment + Implementation WBS in a single workbook
4. `handover-ppt-builder` → handover deck covering the full engagement

## Orchestration rules

- **Run agents sequentially, not in parallel** — each agent's output is an input to the next. Spawn each as a sub-agent via the Agent tool, passing the brief path, prior outputs, and the engagement slug.
- **Check each agent's output exists** before invoking the next. If a file is missing, halt and report.
- **Pass `[TBD: ___]` placeholders forward.** Don't have the next agent fill them — surface them at the end for the user to resolve in one pass.
- **At the end**, show:
  - List of all generated artifacts (relative paths)
  - Summary of pricing and resourcing
  - Consolidated list of `[TBD: ___]` placeholders to resolve
  - Suggested next step (review docs, schedule handover, etc.)

## Brief format

The brief is a Markdown file. Expected sections (the agents will read it):
- Client name and context
- Business drivers and pain points
- Source systems in scope
- Strategic objectives
- Constraints (budget, timeline, compliance)
- Stakeholders

See `examples/sample-brief.md` for the canonical shape.
