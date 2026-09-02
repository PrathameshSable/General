# Fabric Capacity Sizing Reference

How Fabric capacity actually behaves, and a repeatable method for recommending F-SKUs in presales deliverables.
Price table and quick heuristics live in `templates/fabric-domain-reference.md` §2; this file explains the mechanics
behind them.

> Every number in this file is a Microsoft-published figure at time of writing. Guardrails and prices change —
> verify against Microsoft Learn ("Fabric capacity", "Direct Lake overview", "Throttling") and the Azure pricing
> calculator before a number reaches a client document.

---

## 1. Capacity Units (CU)

- An F-SKU is a pool of **Capacity Units**: F2 = 2 CU … F2048 = 2048 CU. Each doubling doubles both throughput and price.
- Every Fabric operation (pipeline run, Spark session, Warehouse query, semantic model query/refresh, KQL ingest,
  Copilot call) consumes CU-seconds, reported per item in the **Fabric Capacity Metrics app**.
- Capacity is shared by all workspaces assigned to it. Workspaces can be moved between capacities without data movement.
- **F64 and above** include the Power BI viewer benefit (consumers need only a free licence) and unlock Copilot;
  below F64, report consumers need Power BI Pro and Copilot requires a separate Copilot capacity arrangement.
- Capacities can be **paused/resumed** (PAYG only), **scaled** up/down in minutes, and **reserved** for one year at
  roughly 40 % discount.

## 2. Smoothing, Bursting, Throttling

| Mechanism | Behaviour | Design implication |
|---|---|---|
| **Bursting** | A job may use more CU than the SKU for short periods | Peaks do not require the peak SKU |
| **Smoothing** | Background operations (pipelines, Spark, refresh) are spread over **24 hours**; interactive operations (queries, report views) over **5 minutes** | Size for the smoothed daily average; push heavy batch into off-peak windows |
| **Overage / carry-forward** | Usage above 100 % accumulates as future debt | Sustained overage leads to throttling, not just slowness |
| **Throttling stages** | ~10 min of overage → interactive delays; ~60 min → interactive rejection; ~24 h → background rejection | Alert well before the first stage; isolate serving from batch |
| **Surge protection** | Capacity admin caps background usage to protect interactive | Enable on shared capacities |
| **Spark autoscale billing** | Optional serverless-style billing for Spark outside the capacity | Consider for spiky data-engineering estates |

## 3. Direct Lake Guardrails (per SKU)

Direct Lake models fall back to DirectQuery (slower, more CU) when a table exceeds these limits. Design Gold tables and
choose the SKU together.

| SKU | Max rows per table | Max model size on disk | Parquet files / row groups per table |
|---|---|---|---|
| F2–F32 | 300 M | 10–40 GB (scales with SKU) | 1,000–5,000 |
| F64 | 1.5 B | 25 GB | 5,000 |
| F128 | 3 B | 50 GB | 5,000 |
| F256 | 6 B | 100 GB | 5,000 |
| F512 | 12 B | 200 GB | 10,000 |
| F1024 / F2048 | 24 B | 400 GB | 10,000 |

Tactics when a model approaches a guardrail: aggregation tables, partition pruning (fewer, larger files), archiving
history to a separate model, or moving that model to a larger serving capacity.

## 4. Sizing Method (use in every deliverable)

### Step 1 — Inventory the load

| Input | Where it comes from | If unknown |
|---|---|---|
| Sources, tables, daily delta GB | Brief / discovery | `[TBD: daily delta volume]` |
| Data at rest (TB) and growth | Brief | `[TBD: data at rest]` |
| Pipelines / notebooks per day and runtime | Legacy ADF/SSIS inventory | Estimate from table counts, mark as assumption |
| Semantic models: count, size, refresh | Power BI admin export / AAS inventory | `[TBD: model inventory]` |
| Report consumers and peak concurrency | Brief / usage metrics | `[TBD: user counts]` |
| Streaming events/sec | Brief | `[TBD]` |
| Copilot / AI usage expectation | Brief | Note F64+ requirement |

### Step 2 — Classify operations

- **Background:** ingestion, Spark transforms, Warehouse loads, model refresh (if Import), MLV refresh, KQL ingest.
- **Interactive:** report queries, Direct Lake queries, SQL endpoint ad-hoc, Copilot prompts.

Background dominates in migration projects; interactive dominates in self-service estates. This decides whether to
separate capacities.

### Step 3 — Choose a starting SKU

Use the heuristics in `templates/fabric-domain-reference.md` §2 as the anchor:

| Profile | Starting SKU |
|---|---|
| POV / assessment sandbox | F4 (trial capacity if available) |
| <1 TB, <50 reports, single domain | F64 |
| 1–10 TB, 50–200 reports, EDW migration | F128 |
| 10–50 TB, multi-domain, hundreds of reports | F256 |
| >50 TB, strict SLA, heavy streaming/AI | F512+ |

Then adjust:
- Largest fact table > rows-per-table guardrail for that SKU → step up or add aggregation tables.
- Copilot / Data Agents in scope → minimum F64 on the serving capacity.
- Heavy nightly Spark (hundreds of GB) → either a larger shared SKU or a separate ingestion capacity that is paused by day.

### Step 4 — Decide topology

| Topology | When | Example (from real SOWs) |
|---|---|---|
| Single capacity | POV, small prod | F64 for everything (LIDS Dev/Test) |
| Prod + Non-Prod | Most implementations | F128 Prod + F64 Dev/Test |
| Prod serving + Prod ingestion + Non-Prod | Executive dashboards must never throttle | F128 Semantic + F128 Data + F64 Dev/Test (LIDS Phase 1: $25,033/mo reserved-basis estate) |
| Per-domain capacities | Charge-back / federated ownership | Domain-assigned capacities, F64 each |

### Step 5 — Model cost

- PAYG hourly × 730 for the first 60–90 days while the profile stabilises; reservation thereafter.
- OneLake storage as a separate line (`$/GB/month`, plus BCDR and cache tiers when applicable).
- Add the standard variability footnote from `templates/common-patterns.md` §1.
- Show funding offsets separately (PLF / Azure Accelerate / ACMA) — see `templates/fabric-domain-reference.md` §8.

Output table for the SOW / handover deck:

| Environment | Workloads | SKU | Monthly PAYG | Monthly Reserved | Storage | Scale trigger |
|---|---|---|---|---|---|---|

### Step 6 — Define the scale trigger and review cadence

- Trigger: sustained >80 % smoothed CU over 7 days, or any interactive-delay throttling event → next SKU.
- Review: weekly during Hypercare, monthly thereafter, using the Capacity Metrics app.

## 5. Worked Examples

**A. Healthcare POV (sample brief, Phase 0)** — Epic delta ~50 M rows/day for one use case, 2 dashboards, Copilot demo.
→ F64 for the POV (Copilot needs F64+; F4 would suffice for pure ingestion), PAYG, paused outside working hours;
storage negligible. Note `[TBD: whether client already owns a Fabric trial or capacity]`.

**B. Phase 1 EDW migration (LIDS pattern)** — D365 + SQL sources, ~2 TB, 100+ reports, AAS models migrating to Direct Lake.
→ F128 Prod data, F128 Prod semantic (separate to protect reporting), F64 Dev/Test; reserve after 90 days.

**C. Multi-domain enterprise (Emory-scale, PHI)** — dual workstream, 4-layer medallion, Purview, private networking.
→ F256 Prod (or 2 × F128 split serving/ingestion), F64 Non-Prod, Private Link; capacity table carries CMK/Private Link
as assumptions with SOW-level setup tasks.

## 6. Common sizing mistakes

- Sizing on the nightly peak instead of the smoothed profile.
- Forgetting that Import-mode refreshes consume CU twice (refresh + query) — a reason to prefer Direct Lake.
- Recommending below F64 when Copilot or free-viewer licensing is expected.
- Ignoring Direct Lake guardrails for the largest fact table.
- Quoting reserved prices as if they were PAYG (or vice versa) — label every figure.
- Conflating Fabric capacity with Power BI Premium Per User licensing.
