# Fabric Best Practices Reference

Implementation-level guidance behind the Best Practices table in `SKILL.md`. Written so that each item can be lifted
into a SOW "Approach" section, a WBS task, or a handover-deck standards slide.

---

## 1. Workspace and Item Naming

- Workspace: `<env>-<domain>-<layer>` → `prd-finance-gold`, `dev-clinical-bronze`, `tst-shared-models`.
- Items: prefix by type — `lh_` Lakehouse, `wh_` Warehouse, `eh_` Eventhouse, `pl_` pipeline, `nb_` notebook,
  `df_` Dataflow Gen2, `sm_` semantic model, `rpt_` report, `env_` Spark environment, `vl_` Variable Library.
- Tables: `<subject>_<entity>` in Lakehouse schemas (`silver.customer`, `gold.fact_encounter`).
- Owners are Entra groups, never individuals.
- Publish the standard as `naming-standard.md` in Sprint 0; the WBS should carry a task for it.

## 2. Lakehouse vs Warehouse Boundary

- Bronze and Silver: Lakehouse (files + Delta tables, Spark-friendly, schema drift tolerant).
- Gold: Warehouse when the team needs T-SQL DML, multi-table transactions, stored procedures or is migrating from
  Synapse dedicated pools; Gold Lakehouse otherwise.
- Do not mix Gold across both without a reason; Direct Lake works on either.
- Lids "Bronze Warehouse" staging is a non-standard label — normalise to Silver in new designs.

## 3. Delta Maintenance

| Task | Cadence | Notes |
|---|---|---|
| `OPTIMIZE` | Weekly, or after bulk loads | Enable V-Order on serving tables |
| `VACUUM` | Weekly, 7-day retention | Longer if time-travel is a requirement |
| Small-file check | Weekly report | Alert when files/table > 1,000 or avg file < 32 MB |
| Statistics | Automatic in Warehouse; verify | Refresh after large loads |
| Auto Compaction / optimizeWrite | Always on in Spark environments | Reduces small files at source |

## 4. Semantic Models

- One model per subject area; reports live-connect.
- Direct Lake default; Import only for small reference models; DirectQuery for write-back.
- Star schema, integer surrogate keys, hidden keys, date table marked.
- Measures in display folders; descriptions and synonyms populated (Copilot readiness).
- RLS via Entra groups; test with "View as".
- Calculation groups for time intelligence; avoid bi-directional relationships.
- Endorse Promoted → Certified through a documented review gate.

## 5. Refresh & Scheduling

- Pipelines trigger downstream pipelines (Invoke pipeline) rather than everything on independent clocks.
- Stagger schedules (02:05, 02:35 …) to avoid top-of-hour CU spikes.
- Direct Lake needs no refresh; reframing happens on Delta commit — schedule `OPTIMIZE` after the last load, not before.
- Use Activator or pipeline failure paths to notify a Teams channel.

## 6. Environments

- Minimum Dev / Test / Prod workspaces per domain-layer.
- Staged migration variant: Prod-Dev / Prod-Test / Prod-Prod when legacy and Fabric run in parallel (Lids).
- Non-Prod uses masked or synthetic PHI/PII; document in SOW assumptions.
- Non-Prod on a smaller capacity, paused outside working hours if PAYG.

## 7. Source Control & Promotion

- Every workspace connected to Git (Azure DevOps or GitHub); Dev workspace on a feature branch or `develop`.
- PR review before merge; deployment pipeline promotes Dev → Test → Prod with deployment rules.
- Variable Library holds environment-specific values; no hard-coded workspace/lakehouse IDs in notebooks or pipelines.
- Notebooks: parameter cell first; use `notebookutils` for lakehouse paths.
- Tag releases; keep a CHANGELOG in the repo.

## 8. Secrets & Identity

- Connections owned by a workspace identity or service principal, not a consultant's account.
- Azure Key Vault references for any secret that cannot be avoided.
- Consultants get workspace Admin during the engagement (SOW assumption), removed at handover.
- Service principals need tenant settings enabled — list as a Day-1 dependency in the WBS.

## 9. Monitoring

| Signal | Tool | Action |
|---|---|---|
| CU utilisation, throttling | Fabric Capacity Metrics app | Weekly review; Activator alert at 80 % |
| Pipeline / notebook failures | Monitoring hub, pipeline failure path | Teams alert, runbook |
| Query and refresh logs | Workspace Monitoring (Eventhouse) | Slow-query report |
| Spark job diagnostics | Spark UI, Spark Advisor, Log Analytics | Tuning backlog |
| Data quality | Validation notebook results table | Daily summary |
| Lineage / impact analysis | OneLake lineage, Purview | Change assessment |

## 10. Testing

- Bronze: row-count parity per table vs source (100 % match is the standard SOW acceptance criterion).
- Silver: uniqueness, null checks on keys, type checks, SCD integrity.
- Gold: referential integrity fact → dim; measure totals vs legacy.
- Semantic model: DAX measure parity vs AAS/legacy for a signed-off KPI list; RLS tests.
- Reports: visual-level regression baseline before repoint.
- UAT gate per release with named sign-off (Report Owners / Process Owners).

## 11. Documentation Set

| Artifact | Produced by | Notes |
|---|---|---|
| Target architecture diagram | This skill (Mermaid → `scripts/render_diagram.py`) | Embedded in SOW and handover deck |
| ADRs | This skill | One per non-obvious choice |
| Capacity table | This skill | Feeds SOW pricing section |
| Naming standard | Sprint 0 | Referenced by WBS |
| Data dictionary / source-to-target mapping | Data Modeller | Per subject area |
| Runbooks | DevOps / Fabric Data Engineer | Failed load, throttling, scale-up, key rotation |
| Handover deck | `handover-ppt-builder` | Consumes all of the above |

## 12. Migration-Specific Practices

- Discovery as a formal gate with a re-baseline checkpoint (Emory pattern) when legacy logic is undocumented.
- Migrate by subject area (Strangler Fig); run legacy and Fabric in parallel for one cycle; parity sign-off; decommission.
- Repoint Power BI reports to Direct Lake models via connection swap, not report rebuild, unless visuals change.
- Keep a decommission checklist in the WBS (Client-owned).
- Hypercare: 4 weeks, Fabric Data Engineer + Power BI Developer allocation, daily monitoring.
