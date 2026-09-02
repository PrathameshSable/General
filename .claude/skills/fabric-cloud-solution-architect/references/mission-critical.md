# Mission-Critical & Regulated Fabric Design Reference

Guidance for Fabric platforms with strict availability targets or regulated data (HIPAA / HITRUST healthcare, PCI,
GDPR, public sector). Be candid in deliverables about what Fabric offers natively and what must be designed around.

---

## 1. Availability and Resilience — what Fabric gives you

| Concern | Fabric behaviour | Design response |
|---|---|---|
| Regional resilience | Fabric is a regional SaaS; zone redundancy in supported regions; Microsoft manages failover of the service | Document the home region and its zone support in the ADR |
| Cross-region disaster recovery | Optional **OneLake BCDR** replicates OneLake data to the paired region; items themselves are restored by Microsoft in a disaster | State RTO/RPO as Microsoft-published values, do not promise better |
| Item-level backup | No user-driven "restore workspace" today; Git integration is the practical item-level backup | Every Prod workspace Git-connected; Warehouse has restore points (verify retention) |
| Capacity failure / throttling | Overage leads to interactive delays then rejections | Isolate serving capacity; surge protection; scale runbook |
| Gateway failure | On-prem gateway is a customer-managed SPOF unless clustered | Cluster of 2+ nodes; monitoring; documented as client dependency |

No multi-region active-active exists for Fabric items. If the client requires it, the honest answer is: OneLake BCDR for
data, Git for definitions, documented manual re-deployment runbook, and a stated RTO measured in hours.

## 2. Capacity Isolation

- **Prod serving** capacity (semantic models, reports) separate from **Prod ingestion** (pipelines, Spark).
- **Self-service / ad-hoc** workspaces on their own capacity so exploratory queries cannot throttle certified dashboards.
- Surge protection on any shared capacity.
- Spark autoscale billing for bursty engineering to keep Spark out of the interactive budget.
- Scale-up runbook: who approves, how to change SKU, expected propagation time.

## 3. Network

| Control | Use when | Caveat |
|---|---|---|
| Tenant-level Private Link | Policy forbids public endpoints | Some features are limited under Private Link — verify current list before committing in SOW |
| Block public internet access | Same | Test Git integration, Copilot, gateway paths |
| Managed VNet + managed private endpoints | Spark must reach private Azure SQL / Storage / Key Vault | Per-workspace; adds setup tasks |
| VNet data gateway | Dataflows / semantic models to private Azure sources | Managed, no VMs |
| On-prem gateway cluster | On-prem SQL Server, file shares | Customer-managed VMs |
| Trusted workspace access | Shortcuts to firewalled ADLS Gen2 | Workspace identity required |

Budget explicit WBS tasks for network setup and a Day-1 dependency on client network/security teams.

## 4. Data Protection

- **Classification:** Purview scan + auto-labelling; PHI/PII sensitivity labels with DLP policies (block export /
  external share).
- **Masking in non-prod:** dynamic data masking on Warehouse / SQL analytics endpoint; or synthetic data generation
  notebook for Dev/Test. SOW assumption: client approves masking rules.
- **Encryption:** encryption at rest by default; **Customer-Managed Keys** at workspace level for BYOK mandates; key
  rotation runbook.
- **Audit:** Fabric audit logs → Purview audit / SIEM (Sentinel) via Microsoft 365 audit; Workspace Monitoring for query
  logs.
- **Retention & deletion:** document how VACUUM retention, OneLake BCDR copies and Purview retention labels interact with
  right-to-erasure requests.

## 5. Identity

- Entra groups only for workspace roles; no individual Admins on Prod.
- Conditional Access for Fabric / Power BI; MFA mandatory.
- Workspace identity or service principals for all automation and connections.
- Least privilege: Viewer for consumers via apps; Contributor for engineers in Dev only; Admin held by platform team.
- Guest (B2B) access explicitly decided and documented.

## 6. Deployment and Testing

- PR-gated promotion through deployment pipelines; no manual changes in Prod (audit).
- Parity test suite (row counts, measure totals, RLS) run in Test before every promotion.
- Rollback = redeploy previous Git tag; practise it during Hypercare.
- Blue/green by workspace for major semantic model changes: publish new model, swap report connections, retire old.
- Chaos-style checks: pause Non-Prod capacity mid-load to validate idempotent re-run.

## 7. Health Modelling

Composite health = capacity health + pipeline health + model health + data-quality health.

| Layer | Signal | Threshold example |
|---|---|---|
| Capacity | Smoothed CU %, throttling events | >80 % sustained / any throttle |
| Pipelines | Failed runs, runtime vs baseline | Any failure; runtime > 1.5× baseline |
| Semantic models | Direct Lake fallback rate, query p95 | Fallback > 0; p95 > 5 s |
| Data quality | Reject counts, parity test failures | Any parity failure on Gold |
| Freshness | Max load timestamp vs SLA | Older than SLA window |

Surface via a Real-Time Dashboard or Power BI page; alert via Activator to Teams.

## 8. Operational Procedures

Runbooks to hand over (WBS tasks under Documentation):

1. Failed nightly load — diagnose, re-run, notify.
2. Capacity throttling — identify offender in Capacity Metrics, pause/scale, communicate.
3. Capacity scale-up / scale-down — approval, execution, validation.
4. Gateway node failure — failover check, node rebuild.
5. Key rotation (CMK) and secret rotation.
6. Access request / offboarding.
7. Disaster recovery — invoke OneLake BCDR data, redeploy from Git, revalidate.
8. Hypercare cadence — daily stand-up, issue log, exit criteria after 4 weeks.

## 9. Compliance Mapping Cheat-Sheet

| Requirement | Fabric control | Evidence for auditor |
|---|---|---|
| HIPAA access control | Entra + RLS/OLS + OneLake security | Role membership export, RLS test results |
| HIPAA audit | Audit logs → SIEM | Log retention policy |
| HITRUST encryption | Default encryption + CMK | Key Vault configuration |
| PHI minimisation in non-prod | Masking / synthetic data | Masking rule sign-off |
| Data residency | Home region + BCDR pairing | Capacity region record |
| Change control | Git + deployment pipelines | PR history |

Always include compliance-driven items in the SOW as explicit tasks and assumptions; they are the most common source of
schedule variance in regulated engagements.
