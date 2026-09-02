# Well-Architected Review Checklist for Fabric

Use this checklist in Step 7 of the Architecture Review Workflow. Score each item **Met / Partial / Gap / N/A**, record
tradeoffs, and turn every Gap into either a design change, a WBS task, or a documented risk.

Output format for deliverables:

| Pillar | Item | Status | Evidence / Decision | Follow-up (WBS / Risk / ADR) |
|---|---|---|---|---|

---

## Reliability

- [ ] Every pipeline and notebook is idempotent and re-runnable from any step
- [ ] Incremental loads use watermarks or CDC with success-only checkpointing
- [ ] Rejected data is quarantined, not dropped or silently loaded
- [ ] Serving workloads isolated from batch (capacity or scheduling) so throttling cannot hit dashboards
- [ ] Surge protection configured on shared capacities; throttling alerts exist
- [ ] Gateway clustered (2+ nodes) for on-prem sources
- [ ] RTO / RPO stated using Microsoft-published values; OneLake BCDR decision recorded
- [ ] Git integration on every Prod workspace as item-level recovery
- [ ] Parallel-run and parity sign-off planned before legacy decommission
- [ ] Hypercare period defined (4 weeks default)

## Security

- [ ] Workspace roles assigned to Entra groups with least privilege; no personal Prod admins
- [ ] Automation uses workspace identity / service principals; no secrets in notebooks
- [ ] OneLake security scoped for engineers and shortcuts; RLS/OLS for consumers
- [ ] Sensitivity labels applied; DLP policies for regulated labels
- [ ] Purview scanning of Fabric tenant enabled; PHI/PII classified
- [ ] Non-prod data masked or synthetic
- [ ] Network posture decided (public + controls vs Private Link + Managed VNet) with feature limitations checked
- [ ] CMK decision recorded
- [ ] Audit logs exported to SIEM; retention agreed
- [ ] External sharing / guest access policy documented

## Cost Optimization

- [ ] SKU sized on the smoothed 24-hour profile, not peak
- [ ] Capacity topology justified (isolation vs smoothing efficiency)
- [ ] Reservation plan after profile stabilises; PAYG and reserved prices labelled separately
- [ ] Non-prod capacity paused outside hours or sized down
- [ ] Shortcuts / mirroring used instead of copies where possible
- [ ] Direct Lake instead of Import to avoid duplicated refresh CU
- [ ] Heavy transforms in Spark/T-SQL, not Dataflow Gen2
- [ ] Native Execution Engine / autotune enabled for Spark
- [ ] Storage line items (OneLake, BCDR, cache) quoted separately
- [ ] Funding offsets (PLF / Azure Accelerate / ACMA) confirmed with user, not assumed

## Operational Excellence

- [ ] Naming standard and workspace taxonomy documented before build
- [ ] Domains defined for business ownership where >1 business unit
- [ ] Git integration + deployment pipelines + Variable Library in place
- [ ] Spark Environment pinned and promoted with workspaces
- [ ] Capacity Metrics app reviewed on a cadence; Workspace Monitoring on Prod
- [ ] Alerts via Activator to Teams for failures and CU thresholds
- [ ] Runbooks listed as WBS deliverables
- [ ] Architecture diagram and ADRs produced and versioned
- [ ] Data dictionary / source-to-target mapping per subject area
- [ ] Training / KT plan for client team (skills gap addressed)

## Performance Efficiency

- [ ] Delta tables compacted, V-Ordered, VACUUMed on schedule
- [ ] Partitioning coarse enough to stay within Direct Lake file / row-group guardrails
- [ ] Largest fact table within rows-per-table guardrail for the chosen SKU
- [ ] Gold is a star schema, not snowflaked; aggregation tables for hot KPIs
- [ ] Direct Lake fallback monitored; composite only where justified
- [ ] Schedules staggered; downstream triggered by dependencies
- [ ] Spark pool sizing and autoscale set per workload; NEE enabled
- [ ] Copilot readiness: Certified model, descriptions, synonyms, KPI folders
- [ ] Streaming path (Eventstream → Eventhouse) sized for events/sec and retention
- [ ] Performance baselines captured before migration for regression comparison

---

## Recording tradeoffs

For each Partial / Gap, use the Fabric Tradeoff Matrix in `SKILL.md` to state what was optimised and what was
accepted as a consequence. Example:

> *Single F128 shared by ingestion and serving (Cost) — accepted risk of interactive delays during month-end loads
> (Reliability). Mitigation: surge protection + overnight scheduling; scale trigger to F256 if throttling observed twice
> in a month. Logged as Risk R-04 in the WBS.*
