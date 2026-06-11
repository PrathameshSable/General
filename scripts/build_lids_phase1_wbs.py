"""
build_lids_phase1_wbs.py
-------------------------
Generates outputs/lids-phase-1-wbs.xlsx — the detailed Work Breakdown Structure
for the Lids Phase 1 Microsoft Fabric Migration engagement.

Engagement facts (from outputs/lids-phase-1-sow.docx):
- Archetype: Phase 1 Lift & Shift (Bronze + Staging only; Gold/Semantic OUT of scope)
- Duration: 13 weeks, kickoff 15-Jan-2026
- Team: 9 FTE (PM x1, Fabric Architect x1, Fabric Data Engineer x3, Power BI Specialist x2,
        Data Modeller x1, Tester x1)
- SOW commitment: ~585 person-days (9 * 13 * 5)
- Inventory: 456 tables, 312 views, 64 stored procs, 15 schemas
- Capacity: F128 Prod + F64 Dev/Test + F128 Semantic = $25,033/mo
- Milestones: Planning W2, Test Lakehouse+Warehouse W7, Prod Lakehouse+Warehouse W10,
              Phase 1 Complete W13
- Hypercare: 2-week post-go-live (Phase 1 default, cost reconciliation TBD)

Output workbook contains 8 sheets:
1. WBS
2. Resource Loading
3. Risk
4. Assumptions
5. Issue Log
6. Dependencies
7. Holidays
8. SOW - Planned Efforts
"""

from datetime import date
from pathlib import Path
from collections import defaultdict

from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, NamedStyle
)
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "outputs" / "lids-phase-1-wbs.xlsx"

TOTAL_WEEKS = 13  # 13 sprint weeks; Hypercare extends to W15 (tracked but not separately priced)
HYPERCARE_WEEKS = 2
GRID_WEEKS = TOTAL_WEEKS + HYPERCARE_WEEKS  # 15-column week grid

# ---------- Styling ----------
HEADER_FILL = PatternFill("solid", fgColor="004B8D")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
BAND_FILL = PatternFill("solid", fgColor="F2F6FA")
MILESTONE_FILL = PatternFill("solid", fgColor="FFE699")
PHASE_FILL = PatternFill("solid", fgColor="DDEBF7")
ACTIVITY_FILL = PatternFill("solid", fgColor="EDEDED")
RED_FILL = PatternFill("solid", fgColor="F8CBAD")
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")
THIN = Side(style="thin", color="B7B7B7")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)


def _style_header(ws, row, cols):
    for col in range(1, cols + 1):
        c = ws.cell(row=row, column=col)
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = CENTER
        c.border = BORDER


def _autosize(ws, min_w=10, max_w=42):
    for col_cells in ws.columns:
        col_letter = get_column_letter(col_cells[0].column)
        max_len = min_w
        for c in col_cells:
            v = c.value
            if v is None:
                continue
            length = max(len(s) for s in str(v).split("\n"))
            if length > max_len:
                max_len = length
        ws.column_dimensions[col_letter].width = min(max_w, max_len + 2)


# ============================================================
# TASK LIBRARY — Lids Phase 1 detailed WBS
# Schema: (wbs, phase, sprint, activity, task, duration_days,
#          effort_pd, deps, owner, vendor, status, milestone_week_or_none, comments)
# Effort target ~ 585 person-days (9 FTE * 13 weeks * 5)
# ============================================================

PHASE = "PHASE 1 - Foundation & Core Analytics"

TASKS = [
    # =================== SPRINT 1 (W1-W2): Planning & Architecture ===================
    ("1",       PHASE, "Sprint 1", "Planning & Architecture",         "Initial Planning & Architecture Design",                        10, 0,   "",         "Fabric Architect",     "Both",   "Yet to Start", None, "Roll-up"),
    ("1.1",     PHASE, "Sprint 1", "Planning & Architecture",         "Project kickoff and team onboarding",                            2, 6,   "",         "Project Manager",      "Both",   "Yet to Start", None, "Joint kickoff with Lids SPOC"),
    ("1.2",     PHASE, "Sprint 1", "Planning & Architecture",         "Project planning, governance, communication cadence setup",      2, 4,   "1.1",      "Project Manager",      "Santor", "Yet to Start", None, ""),
    ("1.3",     PHASE, "Sprint 1", "Planning & Architecture",         "Discovery: validate inventory (456 tables, 312 views, 64 SPs)",  3, 9,   "1.1",      "Fabric Architect",     "Both",   "Yet to Start", None, "Reconcile against SOW Section 3"),
    ("1.4",     PHASE, "Sprint 1", "Planning & Architecture",         "High-Level Design (HLD) - Medallion + Repoint architecture",     5, 10,  "1.3",      "Fabric Architect",     "Santor", "Yet to Start", None, "Bronze Lakehouse + Bronze Warehouse"),
    ("1.5",     PHASE, "Sprint 1", "Planning & Architecture",         "Low-Level Design (LLD) - schemas, naming, partitioning, CDC",    5, 15,  "1.4",      "Fabric Architect",     "Santor", "Yet to Start", None, "LLD per 15 schemas"),
    ("1.6",     PHASE, "Sprint 1", "Planning & Architecture",         "Architecture review & sign-off (Planning Milestone W2)",         2, 4,   "1.4,1.5",  "Fabric Architect",     "Both",   "Yet to Start", 2,    "Milestone: Planning sign-off W2"),

    # =================== SPRINT 1-2 (W1-W3): Environment Setup ===================
    ("2",       PHASE, "Sprint 1", "Environment Setup",               "Environment Setup & Configuration",                              0, 0,   "",         "Fabric Data Engineer", "Both",   "Yet to Start", None, "Roll-up"),
    ("2.1",     PHASE, "Sprint 1", "Environment Setup",               "Access provisioning, security, AAD groups",                      3, 6,   "1.1",      "Fabric Data Engineer", "Client", "Yet to Start", None, "Lids IT owned"),
    ("2.2",     PHASE, "Sprint 1", "Environment Setup",               "Create Fabric workspaces (Dev, QA, Prod) F128/F64",              2, 4,   "2.1",      "Fabric Data Engineer", "Client", "Yet to Start", None, ""),
    ("2.3",     PHASE, "Sprint 1", "Environment Setup",               "Configure OneLake storage structure & domains",                  2, 4,   "2.2",      "Fabric Architect",     "Santor", "Yet to Start", None, ""),
    ("2.4",     PHASE, "Sprint 2", "Environment Setup",               "Setup CI/CD framework with Azure DevOps - Git repo",             3, 6,   "2.2",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("2.5",     PHASE, "Sprint 2", "Environment Setup",               "Implement deployment pipelines (Dev to Test to Prod)",           3, 9,   "2.4",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("2.6",     PHASE, "Sprint 2", "Environment Setup",               "Environment validation and smoke testing",                       2, 4,   "2.5",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),

    # =================== SPRINT 2-3 (W3-W6): Bronze Lakehouse (Landing) ===================
    ("3",       PHASE, "Sprint 2", "Bronze Lakehouse",                "Bronze Lakehouse (Landing Layer) - Test Env",                    0, 0,   "",         "Fabric Data Engineer", "Santor", "Yet to Start", None, "Roll-up"),
    ("3.1",     PHASE, "Sprint 2", "Bronze Lakehouse",                "Configure Fabric Dataverse Link to D365 Test F&O",               3, 9,   "2.6",      "Fabric Architect",     "Santor", "Yet to Start", None, ""),
    ("3.2",     PHASE, "Sprint 2", "Bronze Lakehouse",                "Create Bronze Lakehouse structure (Test)",                       2, 4,   "3.1",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("3.3",     PHASE, "Sprint 3", "Bronze Lakehouse",                "Ingest 227 landing tables from D365 - Test",                     5, 25,  "3.2",      "Fabric Data Engineer", "Santor", "Yet to Start", None, "3 Fabric Data Engineers parallel"),
    ("3.4",     PHASE, "Sprint 3", "Bronze Lakehouse",                "Create 226 views in Bronze Lakehouse - Test",                    4, 16,  "3.3",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("3.5",     PHASE, "Sprint 3", "Bronze Lakehouse",                "Configure CDC handling and incremental ingestion patterns",      4, 12,  "3.3",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("3.6",     PHASE, "Sprint 3", "Bronze Lakehouse",                "Implement data quality checks & monitoring/alerting - Test",     3, 9,   "3.4,3.5",  "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("3.7",     PHASE, "Sprint 3", "Bronze Lakehouse",                "Bronze Lakehouse SIT - Test (record-count parity)",              3, 9,   "3.6",      "Tester",               "Santor", "Yet to Start", None, "100% record-count match criterion"),

    # =================== SPRINT 3-4 (W5-W8): Bronze Warehouse (Staging) ===================
    ("4",       PHASE, "Sprint 3", "Bronze Warehouse",                "Bronze Warehouse (Staging Layer) - Test Env",                    0, 0,   "",         "Fabric Data Engineer", "Santor", "Yet to Start", None, "Roll-up"),
    ("4.1",     PHASE, "Sprint 3", "Bronze Warehouse",                "Create Fabric Data Warehouse - Test",                            2, 4,   "3.2",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("4.2",     PHASE, "Sprint 3", "Bronze Warehouse",                "Analyze 64 staging stored procedures (T-SQL parity)",            4, 12,  "4.1",      "Fabric Architect",     "Santor", "Yet to Start", None, "Compatibility audit"),
    ("4.3",     PHASE, "Sprint 4", "Bronze Warehouse",                "Refactor 64 stored procedures to Fabric T-SQL/PySpark",          8, 32,  "4.2",      "Fabric Data Engineer", "Santor", "Yet to Start", None, "Heaviest work package"),
    ("4.4",     PHASE, "Sprint 4", "Bronze Warehouse",                "Migrate 229 staging tables to Bronze Warehouse - Test",          5, 20,  "4.1",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("4.5",     PHASE, "Sprint 4", "Bronze Warehouse",                "Create 86 views in Bronze Warehouse - Test",                     3, 9,   "4.4",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("4.6",     PHASE, "Sprint 4", "Bronze Warehouse",                "Implement deduplication & business-rule transformations",        4, 12,  "4.3,4.4",  "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("4.7",     PHASE, "Sprint 4", "Bronze Warehouse",                "Bronze Warehouse SIT - Test (Milestone W7)",                     3, 9,   "4.5,4.6",  "Tester",               "Santor", "Yet to Start", 7,    "Milestone: Test Lakehouse + Warehouse W7"),

    # =================== SPRINT 4-5 (W7-W10): ADF Pipeline Repoint ===================
    ("5",       PHASE, "Sprint 4", "ADF Repoint",                     "ADF Pipeline Repoint to Fabric",                                 0, 0,   "",         "Fabric Data Engineer", "Both",   "Yet to Start", None, "Roll-up - Phase 1 hallmark"),
    ("5.1",     PHASE, "Sprint 4", "ADF Repoint",                     "Inventory & analyze existing ADF pipelines (EDW + ScalziDB)",    3, 9,   "4.1",      "Fabric Architect",     "Both",   "Yet to Start", None, "Joint with Lids ADF SMEs"),
    ("5.2",     PHASE, "Sprint 5", "ADF Repoint",                     "Design repoint patterns - Fabric SQL endpoint source",           3, 9,   "5.1",      "Fabric Architect",     "Santor", "Yet to Start", None, ""),
    ("5.3",     PHASE, "Sprint 5", "ADF Repoint",                     "Repoint ADF pipelines for EDW (Bronze Warehouse source) - Test", 5, 15,  "5.2,4.7",  "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("5.4",     PHASE, "Sprint 5", "ADF Repoint",                     "Repoint ADF pipelines for ScalziDB downstream",                  4, 12,  "5.3",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("5.5",     PHASE, "Sprint 5", "ADF Repoint",                     "Repoint ADF for Non-BI Systems (Bronze Lakehouse source)",       4, 12,  "5.2,3.7",  "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("5.6",     PHASE, "Sprint 5", "ADF Repoint",                     "ADF Repoint SIT - end-to-end integration testing",               3, 9,   "5.3,5.4,5.5","Tester",             "Both",   "Yet to Start", None, "Joint with Lids Integration Teams SPOC"),

    # =================== SPRINT 4-5 (W7-W10): Power BI Repoint ===================
    ("6",       PHASE, "Sprint 4", "Power BI Repoint",                "Power BI Reports Migration",                                     0, 0,   "",         "Power BI Specialist",  "Santor", "Yet to Start", None, "Roll-up - Phase 1 hallmark"),
    ("6.1",     PHASE, "Sprint 4", "Power BI Repoint",                "Inventory Power BI reports on Synapse/Staging",                  3, 6,   "4.1",      "Power BI Specialist",  "Both",   "Yet to Start", None, ""),
    ("6.2",     PHASE, "Sprint 4", "Power BI Repoint",                "Repoint 2 sample reports to Test Bronze Lakehouse + Warehouse",  3, 6,   "6.1,4.7",  "Power BI Specialist",  "Santor", "Yet to Start", None, "SQL endpoint validation"),
    ("6.3",     PHASE, "Sprint 5", "Power BI Repoint",                "Bulk repoint Power BI connection strings to Fabric Warehouse",   6, 24,  "6.2",      "Power BI Specialist",  "Santor", "Yet to Start", None, "2 PBI Specialists parallel"),
    ("6.4",     PHASE, "Sprint 5", "Power BI Repoint",                "Validate report functionality, DAX, data accuracy",              5, 20,  "6.3",      "Power BI Specialist",  "Santor", "Yet to Start", None, ""),
    ("6.5",     PHASE, "Sprint 5", "Power BI Repoint",                "Performance optimization - report query plans",                  3, 9,   "6.4",      "Power BI Specialist",  "Santor", "Yet to Start", None, ""),
    ("6.6",     PHASE, "Sprint 5", "Power BI Repoint",                "Power BI SIT (parallel run vs legacy)",                          3, 6,   "6.5",      "Tester",               "Santor", "Yet to Start", None, ""),

    # =================== SPRINT 5 (W9-W10): Prod Environment Buildout ===================
    ("7",       PHASE, "Sprint 5", "Prod Environment",                "Production Environment Buildout",                                0, 0,   "",         "Fabric Data Engineer", "Santor", "Yet to Start", None, "Roll-up"),
    ("7.1",     PHASE, "Sprint 5", "Prod Environment",                "Configure Fabric Dataverse Link to D365 PROD F&O",               3, 9,   "3.7",      "Fabric Architect",     "Santor", "Yet to Start", None, ""),
    ("7.2",     PHASE, "Sprint 5", "Prod Environment",                "Create 3 Prod Bronze Warehouses (Dev/Test/Prod tiers)",          3, 9,   "7.1",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("7.3",     PHASE, "Sprint 5", "Prod Environment",                "Promote pipelines via CI/CD to Prod",                            3, 9,   "7.2,2.5",  "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("7.4",     PHASE, "Sprint 5", "Prod Environment",                "Production Lakehouse + Warehouse validation (Milestone W10)",    3, 9,   "7.3",      "Tester",               "Santor", "Yet to Start", 10,   "Milestone: Prod Lakehouse + Warehouse W10"),

    # =================== SPRINT 6 (W11-W12): UAT & EDW Model Rationalization ===================
    ("8",       PHASE, "Sprint 6", "UAT & Documentation",             "User Acceptance Testing & Documentation",                        0, 0,   "",         "Tester",               "Both",   "Yet to Start", None, "Roll-up"),
    ("8.1",     PHASE, "Sprint 6", "UAT & Documentation",             "UAT planning & test-case preparation",                           3, 9,   "7.4",      "Tester",               "Santor", "Yet to Start", None, ""),
    ("8.2",     PHASE, "Sprint 6", "UAT & Documentation",             "Execute UAT - Bronze Lakehouse",                                 3, 9,   "8.1",      "Tester",               "Both",   "Yet to Start", None, "Joint with Lids SMEs"),
    ("8.3",     PHASE, "Sprint 6", "UAT & Documentation",             "Execute UAT - Bronze Warehouse (T-SQL parity)",                  3, 9,   "8.1",      "Tester",               "Both",   "Yet to Start", None, ""),
    ("8.4",     PHASE, "Sprint 6", "UAT & Documentation",             "Execute UAT - ADF Repoint end-to-end",                           3, 9,   "8.1",      "Tester",               "Both",   "Yet to Start", None, ""),
    ("8.5",     PHASE, "Sprint 6", "UAT & Documentation",             "Execute UAT - Power BI repointed reports",                       3, 9,   "8.1",      "Tester",               "Both",   "Yet to Start", None, ""),
    ("8.6",     PHASE, "Sprint 6", "UAT & Documentation",             "Defect resolution & retesting",                                  4, 16,  "8.2,8.3,8.4,8.5", "Fabric Data Engineer","Santor", "Yet to Start", None, ""),
    ("8.7",     PHASE, "Sprint 6", "UAT & Documentation",             "DW Data Model Rationalization document",                         5, 15,  "1.5",      "Data Modeller",        "Santor", "Yet to Start", None, "Conceptual/logical/SCD analysis"),
    ("8.8",     PHASE, "Sprint 6", "UAT & Documentation",             "BI Data Dictionary & DAX Migration Guide",                       5, 10,  "1.5",      "Data Modeller",        "Santor", "Yet to Start", None, "8 AAS cubes, 3993 DAX measures"),
    ("8.9",     PHASE, "Sprint 6", "UAT & Documentation",             "Technical documentation (architecture, runbooks)",               3, 9,   "8.7",      "Fabric Architect",     "Santor", "Yet to Start", None, ""),
    ("8.10",    PHASE, "Sprint 6", "UAT & Documentation",             "UAT sign-off",                                                   1, 2,   "8.6",      "Project Manager",      "Both",   "Yet to Start", None, ""),

    # =================== SPRINT 7 (W13): Go-Live & Decommission ===================
    ("9",       PHASE, "Sprint 7", "Go-Live & Cutover",               "Production Go-Live & Cutover",                                   0, 0,   "",         "Fabric Architect",     "Both",   "Yet to Start", None, "Roll-up"),
    ("9.1",     PHASE, "Sprint 7", "Go-Live & Cutover",               "Cutover runbook & readiness review",                             2, 6,   "8.10",     "Project Manager",      "Both",   "Yet to Start", None, ""),
    ("9.2",     PHASE, "Sprint 7", "Go-Live & Cutover",               "Execute production cutover (joint)",                             2, 8,   "9.1",      "Fabric Architect",     "Both",   "Yet to Start", None, ""),
    ("9.3",     PHASE, "Sprint 7", "Go-Live & Cutover",               "Day-1 post-cutover monitoring",                                  2, 6,   "9.2",      "Fabric Data Engineer", "Santor", "Yet to Start", None, ""),
    ("9.4",     PHASE, "Sprint 7", "Go-Live & Cutover",               "Decommission Synapse Landing + Staging SQL (Client owned)",      2, 4,   "9.3",      "Fabric Architect",     "Client", "Yet to Start", None, ""),
    ("9.5",     PHASE, "Sprint 7", "Go-Live & Cutover",               "Phase 1 Complete - sign-off (Milestone W13)",                    1, 3,   "9.4",      "Project Manager",      "Both",   "Yet to Start", 13,   "Milestone: Phase 1 Complete W13"),

    # =================== SPRINT 7 (W14-W15): Hypercare (cost TBD) ===================
    ("10",      PHASE, "Hypercare", "Hypercare",                      "Post Go-Live Hypercare (2 weeks)",                               0, 0,   "",         "Fabric Data Engineer", "Santor", "Yet to Start", None, "Cost reconciliation TBD"),
    ("10.1",    PHASE, "Hypercare", "Hypercare",                      "Hypercare support - issue triage and resolution",               10, 20,  "9.5",      "Fabric Data Engineer", "Santor", "Yet to Start", None, "2 FTE for 2 weeks"),
    ("10.2",    PHASE, "Hypercare", "Hypercare",                      "Hypercare support - Power BI report stabilization",             10, 10,  "9.5",      "Power BI Specialist",  "Santor", "Yet to Start", None, "1 FTE for 2 weeks"),
    ("10.3",    PHASE, "Hypercare", "Hypercare",                      "Lessons learned & knowledge transfer to Lids team",              3, 6,   "10.1,10.2","Project Manager",      "Both",   "Yet to Start", 15,   "Final handover; Phase 2 prep handoff"),
]

# Pre-compute task->weeks mapping (used for resource loading)
# We map sprints to weeks: Sprint 1 = W1-W2, Sprint 2 = W3-W4, Sprint 3 = W5-W6,
# Sprint 4 = W7-W8, Sprint 5 = W9-W10, Sprint 6 = W11-W12, Sprint 7 = W13, Hypercare = W14-W15
SPRINT_WEEK_MAP = {
    "Sprint 1": [1, 2],
    "Sprint 2": [3, 4],
    "Sprint 3": [5, 6],
    "Sprint 4": [7, 8],
    "Sprint 5": [9, 10],
    "Sprint 6": [11, 12],
    "Sprint 7": [13],
    "Hypercare": [14, 15],
}


# ============================================================
# Sheet 1: WBS
# ============================================================
def build_wbs(ws):
    headers = (
        ["WBS", "Phase", "Sprint", "Activity", "Task Name",
         "Duration (Days)", "Effort (Person-Days)", "Dependencies",
         "Owner Role", "Vendor / Client", "Status", "Comments"]
        + [f"W{i}" for i in range(1, GRID_WEEKS + 1)]
    )
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    band = False
    for t in TASKS:
        (wbs_id, phase, sprint, activity, name, dur, eff, deps,
         owner, vendor, status, milestone, comments) = t
        row = [wbs_id, phase, sprint, activity, name, dur, eff, deps,
               owner, vendor, status, comments]
        # week markers
        weeks = [""] * GRID_WEEKS
        if milestone:
            weeks[milestone - 1] = "*"
        row += weeks
        ws.append(row)

        r = ws.max_row
        # Apply fills
        is_rollup = "." not in wbs_id  # top-level rollup rows
        fill = PHASE_FILL if is_rollup else (BAND_FILL if band else None)
        for col in range(1, len(headers) + 1):
            c = ws.cell(row=r, column=col)
            c.border = BORDER
            if fill:
                c.fill = fill
            if is_rollup:
                c.font = Font(bold=True)
            if col >= 13:
                c.alignment = CENTER
                if c.value == "*":
                    c.fill = MILESTONE_FILL
                    c.font = Font(bold=True, color="9C5700")
            elif col == 5 or col == 12:
                c.alignment = LEFT
            else:
                c.alignment = CENTER
        if not is_rollup:
            band = not band

    # Freeze first row and first 5 columns
    ws.freeze_panes = "F2"
    _autosize(ws, min_w=8, max_w=46)
    # Tighten week-grid columns
    for i in range(13, 13 + GRID_WEEKS):
        ws.column_dimensions[get_column_letter(i)].width = 4


# ============================================================
# Sheet 2: Resource Loading
# ============================================================
def build_resource_loading(ws):
    # Aggregate effort per role per week
    # Effort allocation: split each task's effort evenly across its sprint weeks
    role_week_effort = defaultdict(lambda: defaultdict(float))

    for t in TASKS:
        (wbs_id, phase, sprint, activity, name, dur, eff, deps,
         owner, vendor, status, milestone, comments) = t
        if eff == 0:  # roll-up rows
            continue
        weeks = SPRINT_WEEK_MAP.get(sprint, [])
        if not weeks:
            continue
        per_week = eff / len(weeks)
        for w in weeks:
            role_week_effort[owner][w] += per_week

    headers = (
        ["Role", "Total Effort (Days)", "Total Effort (FTE-equiv)"]
        + [f"W{i}" for i in range(1, GRID_WEEKS + 1)]
    )
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    role_order = [
        "Project Manager",
        "Fabric Architect",
        "Fabric Data Engineer",
        "Power BI Specialist",
        "Data Modeller",
        "Tester",
    ]

    band = False
    weekly_totals = [0.0] * GRID_WEEKS
    weekly_role_count = [0] * GRID_WEEKS

    for role in role_order:
        weekly = [role_week_effort.get(role, {}).get(w, 0.0) for w in range(1, GRID_WEEKS + 1)]
        total = sum(weekly)
        fte_equiv = round(total / (GRID_WEEKS * 5.0), 2)
        row = [role, round(total, 1), fte_equiv] + [round(v, 1) if v > 0 else "" for v in weekly]
        ws.append(row)
        r = ws.max_row
        for col in range(1, len(headers) + 1):
            c = ws.cell(row=r, column=col)
            c.border = BORDER
            c.alignment = CENTER if col != 1 else LEFT
            if band:
                c.fill = BAND_FILL
        band = not band
        for i, v in enumerate(weekly):
            weekly_totals[i] += v
            if v > 0:
                weekly_role_count[i] += 1

    # Total row
    total_row = ["Total Effort (Days)", round(sum(weekly_totals), 1),
                 round(sum(weekly_totals) / (GRID_WEEKS * 5.0), 2)] + \
                [round(v, 1) if v > 0 else "" for v in weekly_totals]
    ws.append(total_row)
    r = ws.max_row
    for col in range(1, len(headers) + 1):
        c = ws.cell(row=r, column=col)
        c.fill = HEADER_FILL
        c.font = Font(bold=True, color="FFFFFF")
        c.border = BORDER
        c.alignment = CENTER if col != 1 else LEFT

    # Team size row
    size_row = ["Active Roles (Team Size)", "", ""] + [v if v > 0 else "" for v in weekly_role_count]
    ws.append(size_row)
    r = ws.max_row
    for col in range(1, len(headers) + 1):
        c = ws.cell(row=r, column=col)
        c.fill = ACTIVITY_FILL
        c.font = Font(bold=True)
        c.border = BORDER
        c.alignment = CENTER if col != 1 else LEFT

    ws.freeze_panes = "D2"
    _autosize(ws, min_w=8, max_w=28)
    for i in range(4, 4 + GRID_WEEKS):
        ws.column_dimensions[get_column_letter(i)].width = 6

    # Return total person-days for downstream reconciliation
    return round(sum(weekly_totals), 1)


# ============================================================
# Sheet 3: Risk
# ============================================================
def build_risk(ws):
    headers = ["ID", "Date Raised", "Risk Description", "Consequences",
               "Likelihood", "Impact", "Severity",
               "Mitigation Plan", "Owner", "Status", "Date Closed"]
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    risks = [
        ("R-01", "2026-01-15",
         "Functional Compatibility - T-SQL parity gap between Synapse Serverless and Fabric Warehouse",
         "64 stored procedures may not be 100% portable; refactoring effort overrun",
         "Medium", "High", "High",
         "Pre-migration T-SQL audit in Sprint 1; PySpark notebook fallback for non-portable SPs; staged compatibility testing",
         "Fabric Architect", "Open", ""),
        ("R-02", "2026-01-15",
         "Performance - Fabric Warehouse query performance vs Synapse Serverless baseline",
         "Power BI reports/ADF pipelines may regress; user experience degradation",
         "Medium", "High", "High",
         "Performance baseline before cutover; parallel run; F128 capacity sizing buffer; query plan optimization in Sprint 5",
         "Fabric Architect", "Open", ""),
        ("R-03", "2026-01-15",
         "Data Movement - External table / CDC patterns timing during 227-table ingestion",
         "Bronze Lakehouse SIT slips; downstream ADF/Power BI repoint blocked",
         "Medium", "Medium", "Medium",
         "3 Fabric Data Engineers parallelized on 227-table ingest; CDC validated early in Sprint 2; data quality checks at every layer",
         "Senior Data Engineer", "Open", ""),
        ("R-04", "2026-01-15",
         "Operational - Lids SME / Integration Team SPOC availability",
         "ADF repoint SIT depends on Integration Team participation; cutover delay risk",
         "Medium", "Medium", "Medium",
         "Lids designates one SPOC per side at kickoff; weekly cadence; escalation path via Steering Committee",
         "Project Manager", "Open", ""),
        ("R-05", "2026-01-15",
         "Cost Overrun - F128 + F64 + F128 capacity ($25,033/mo) may exceed approved budget if peak concurrency higher than 10%",
         "Capacity SKU upgrade required; OPEX overrun vs SOW estimate",
         "Low", "Medium", "Low",
         "Monthly capacity utilization review; right-sizing recommendation post-UAT; capacity refinement in Sprint 6",
         "Fabric Architect", "Open", ""),
        ("R-06", "2026-01-15",
         "BI Impact - Power BI report regression after repointing to Fabric Warehouse",
         "Business user dissatisfaction; rollback to Synapse risk; UAT slip",
         "Medium", "High", "High",
         "2 PBI Specialists parallel; sample repoint in Sprint 4 before bulk; DAX validation; parallel run vs legacy in SIT",
         "Power BI Specialist", "Open", ""),
        ("R-07", "2026-01-15",
         "Schedule Risk - 13-week timeline aggressive given 456 tables/312 views/64 SPs",
         "Sprint slip cascades to UAT/Go-Live; Hypercare squeeze",
         "Medium", "High", "High",
         "Buffer week absorbed in Sprint 6 UAT; CI/CD reuse to compress Prod environment buildout; weekly EVM tracking",
         "Project Manager", "Open", ""),
        ("R-08", "2026-01-15",
         "Acceptance Risk - 100% record-count match (legacy vs Fabric) at every layer",
         "UAT sign-off blocked; cutover delay",
         "Low", "High", "Medium",
         "Reconciliation harness built in Sprint 2; automated row-count validators at Bronze/Warehouse SIT; defect resolution buffer in Sprint 6",
         "Tester", "Open", ""),
    ]

    band = False
    for r in risks:
        ws.append(list(r))
        rnum = ws.max_row
        for col in range(1, len(headers) + 1):
            c = ws.cell(row=rnum, column=col)
            c.border = BORDER
            c.alignment = LEFT if col in (3, 4, 8) else CENTER
            if band:
                c.fill = BAND_FILL
            # color severity
            if col == 7:
                if c.value == "High":
                    c.fill = RED_FILL
                    c.font = Font(bold=True, color="9C0006")
                elif c.value == "Medium":
                    c.fill = MILESTONE_FILL
                elif c.value == "Low":
                    c.fill = GREEN_FILL
        band = not band

    ws.freeze_panes = "A2"
    _autosize(ws, min_w=10, max_w=48)


# ============================================================
# Sheet 4: Assumptions
# ============================================================
def build_assumptions(ws):
    headers = ["#", "Date Raised", "Assumption Description", "Reason for Assumption",
               "Action to Validate", "Impact if Assumption Incorrect", "Status"]
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    rows = [
        (1, "2026-01-15",
         "Lids provisions timely access to Fabric, OneLake, Synapse (R/O), D365 Dataverse, ADF, SQL DBs, AAS, Power BI workspaces, Azure DevOps by Day 1",
         "SOW Section 9.2 Required Access",
         "Access checklist validated in Sprint 1 kickoff",
         "Sprint 1 slip; cascading delays to Bronze ingest",
         "Open"),
        (2, "2026-01-15",
         "F128 Prod + F64 Dev/Test + F128 Semantic capacity provisioned and billed monthly ($25,033 + $819 OneLake)",
         "SOW Section 7.2 capacity recommendation",
         "Confirm SKU in Sprint 1 environment setup",
         "Cost overrun; performance shortfall",
         "Open"),
        (3, "2026-01-15",
         "Lids SMEs and Integration Team SPOCs available for discovery, validation, UAT sessions on agreed cadence",
         "SOW Section 9.1 / 9.3 Lids Responsibilities",
         "SPOC roster confirmed at kickoff; weekly availability windows",
         "Schedule slip; UAT extension",
         "Open"),
        (4, "2026-01-15",
         "UAT runs iteratively after each sprint development+SIT; UAT results expected to match SIT",
         "SOW Section 9.4 Collaboration",
         "Sprint 6 UAT plan locked in Sprint 4",
         "UAT bottleneck; Go-Live delay",
         "Open"),
        (5, "2026-01-15",
         "Migration executed remotely with virtual collaboration (no onsite presence assumed)",
         "SOW Section 9.1 Project Assumptions",
         "Microsoft Teams + DevOps Boards confirmed in kickoff",
         "Communication friction; expense overrun if onsite needed",
         "Open"),
        (6, "2026-01-15",
         "Inventory accuracy: 456 tables, 312 views, 64 stored procedures, 15 schemas",
         "SOW Section 3.1 Current State Inventory",
         "Discovery validation task 1.3 in Sprint 1",
         "Effort variance vs SOW; CR required",
         "Open"),
        (7, "2026-01-15",
         "Existing documentation and code repositories accessible; Azure DevOps/GitHub available for CI/CD",
         "SOW Section 9.1 Project Assumptions",
         "Repo access verified in Sprint 1",
         "CI/CD setup blocked",
         "Open"),
        (8, "2026-01-15",
         "Phase 2 prep activities staffed by separate resources from core Phase 1 team",
         "SOW Section 9.1 Project Assumptions",
         "Resource plan confirmed with Lids",
         "Phase 1 team over-allocation",
         "Open"),
        (9, "2026-01-15",
         "No BI is connected to D365 Test environment; Test ADF used for SQL endpoint validation before Prod",
         "SOW Section 9.1 Project Assumptions",
         "Validated in inventory phase",
         "Test/Prod sequencing rework",
         "Open"),
        (10, "2026-01-15",
         "Hypercare 2 weeks post Go-Live; cost reconciliation TBD (not separately priced in SOW)",
         "Phase 1 default + commercial reconciliation pending",
         "Confirm commercial coverage with Lids by Sprint 6",
         "Hypercare effort uncovered; CR may be needed",
         "Open"),
    ]

    band = False
    for r in rows:
        ws.append(list(r))
        rnum = ws.max_row
        for col in range(1, len(headers) + 1):
            c = ws.cell(row=rnum, column=col)
            c.border = BORDER
            c.alignment = LEFT if col in (3, 4, 5, 6) else CENTER
            if band:
                c.fill = BAND_FILL
        band = not band

    ws.freeze_panes = "A2"
    _autosize(ws, min_w=8, max_w=52)


# ============================================================
# Sheet 5: Issue Log
# ============================================================
def build_issue_log(ws):
    headers = ["ID", "Date Raised", "Issue Description", "Impact Description",
               "Impact", "Priority", "Owner", "Status", "Resolution TAT"]
    ws.append(headers)
    _style_header(ws, 1, len(headers))
    ws.append(["(no issues at engagement kickoff)", "", "", "", "", "", "", "", ""])
    for col in range(1, len(headers) + 1):
        c = ws.cell(row=2, column=col)
        c.border = BORDER
        c.alignment = LEFT
        c.font = Font(italic=True, color="808080")
    ws.freeze_panes = "A2"
    _autosize(ws, min_w=12, max_w=40)


# ============================================================
# Sheet 6: Dependencies
# ============================================================
def build_dependencies(ws):
    headers = ["ID", "Date Raised", "Dependency Description", "Owner",
               "Impact", "Status", "Due Date", "Remarks"]
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    deps = [
        ("D-01", "2026-01-15",
         "Lids designates Single Point of Contact (SPOC) for all access, credentials, network requests",
         "Lids", "All workstreams blocked without SPOC", "Open", "2026-01-15 (Day 1)",
         "SOW Section 9.1; named in kickoff"),
        ("D-02", "2026-01-15",
         "Fabric workspaces (Dev/QA/Prod) provisioned with F128/F64 capacity",
         "Lids IT", "Bronze Lakehouse build blocked", "Open", "2026-01-22 (Sprint 1)",
         "Capacity SKUs per SOW Section 7.2"),
        ("D-03", "2026-01-15",
         "D365 Dataverse access for Fabric Dataverse Link configuration (Test & Prod F&O)",
         "Lids", "Bronze Lakehouse ingestion blocked", "Open", "2026-01-22 (Sprint 1)",
         "Test env first, Prod env Sprint 5"),
        ("D-04", "2026-01-15",
         "Read access to Synapse Landing, Staging SQL DBs, EDW SQL DBs",
         "Lids", "Inventory validation and ADF analysis blocked", "Open", "2026-01-22 (Sprint 1)",
         ""),
        ("D-05", "2026-01-15",
         "Integration Team SPOCs from downstream systems (ScalziDB, EDW) for ADF repoint SIT",
         "Lids", "ADF SIT (Sprint 5) blocked", "Open", "2026-02-26 (Sprint 4)",
         "Joint testing required"),
        ("D-06", "2026-01-15",
         "Azure DevOps repository access for CI/CD setup",
         "Lids", "CI/CD framework delayed", "Open", "2026-01-29 (Sprint 2)",
         ""),
        ("D-07", "2026-01-15",
         "Power BI Admin access (tenant + workspaces) for report repoint",
         "Lids", "Power BI repoint workstream blocked", "Open", "2026-02-19 (Sprint 4)",
         ""),
        ("D-08", "2026-01-15",
         "AAS read-only access with Tabular Editor for metadata extraction (DAX + cubes)",
         "Lids", "BI Data Dictionary deliverable blocked", "Open", "2026-03-26 (Sprint 6)",
         "For documentation deliverable"),
        ("D-09", "2026-01-15",
         "Business stakeholders available for UAT sign-off in Sprint 6",
         "Lids", "Phase 1 Go-Live blocked", "Open", "2026-03-26 (Sprint 6)",
         ""),
        ("D-10", "2026-01-15",
         "Microsoft Partner Funding (Azure Accelerate PLF) claim filed before W13",
         "Santor + Lids", "Net invoice reduced by $75K", "Open", "2026-04-15 (Pre Go-Live)",
         "$75K PLF per SOW commercial"),
    ]

    band = False
    for d in deps:
        ws.append(list(d))
        rnum = ws.max_row
        for col in range(1, len(headers) + 1):
            c = ws.cell(row=rnum, column=col)
            c.border = BORDER
            c.alignment = LEFT if col in (3, 5, 8) else CENTER
            if band:
                c.fill = BAND_FILL
        band = not band

    ws.freeze_panes = "A2"
    _autosize(ws, min_w=10, max_w=48)


# ============================================================
# Sheet 7: Holidays
# ============================================================
def build_holidays(ws):
    headers = ["Date", "Day-of-Week", "Holiday Name", "Region"]
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    holidays = [
        ("2026-01-26", "Monday",    "Republic Day",          "India"),
        ("2026-02-16", "Monday",    "Presidents' Day",       "US"),
        ("2026-03-06", "Friday",    "Holi (observance)",     "India"),
        ("2026-04-03", "Friday",    "Good Friday",           "Both"),
        ("2026-04-14", "Tuesday",   "Ambedkar Jayanti",      "India"),
        ("2026-05-25", "Monday",    "Memorial Day",          "US"),
        ("2026-07-03", "Friday",    "Independence Day (obs)","US"),
        ("2026-08-15", "Saturday",  "Independence Day",      "India"),
        ("2026-10-02", "Friday",    "Gandhi Jayanti",        "India"),
        ("2026-10-20", "Tuesday",   "Diwali",                "India"),
        ("2026-10-21", "Wednesday", "Diwali (Padwa)",        "India"),
        ("2026-11-26", "Thursday",  "Thanksgiving",          "US"),
        ("2026-11-27", "Friday",    "Day after Thanksgiving","US"),
        ("2026-12-25", "Friday",    "Christmas",             "Both"),
        ("2027-01-01", "Friday",    "New Year",              "Both"),
    ]

    band = False
    for h in holidays:
        ws.append(list(h))
        rnum = ws.max_row
        for col in range(1, len(headers) + 1):
            c = ws.cell(row=rnum, column=col)
            c.border = BORDER
            c.alignment = LEFT if col == 3 else CENTER
            if band:
                c.fill = BAND_FILL
        band = not band

    ws.freeze_panes = "A2"
    _autosize(ws, min_w=10, max_w=28)


# ============================================================
# Sheet 8: SOW - Planned Efforts
# ============================================================
def build_sow_planned(ws, wbs_total_pd):
    headers = ["Workstream / Sprint", "Role",
               "SOW Committed Days", "WBS Planned Days",
               "Variance (Days)", "Variance %"]
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    # Aggregate WBS planned days per (Activity, Role)
    wbs_by_activity_role = defaultdict(float)
    wbs_by_role = defaultdict(float)
    for t in TASKS:
        (wbs_id, phase, sprint, activity, name, dur, eff, deps,
         owner, vendor, status, milestone, comments) = t
        if eff == 0:
            continue
        wbs_by_activity_role[(activity, owner)] += eff
        wbs_by_role[owner] += eff

    # SOW commitments per role (9 FTE * 13 weeks * 5 days = 585 base; allocate by role)
    # Excluding Hypercare from the SOW commit (Hypercare cost reconciliation TBD)
    BASE_DAYS = 13 * 5  # 65 working days per role
    sow_commit = {
        "Project Manager":      BASE_DAYS * 1,   # 65
        "Fabric Architect":     BASE_DAYS * 1,   # 65
        "Fabric Data Engineer": BASE_DAYS * 3,   # 195
        "Power BI Specialist":  BASE_DAYS * 2,   # 130
        "Data Modeller":        BASE_DAYS * 1,   # 65
        "Tester":               BASE_DAYS * 1,   # 65
    }
    total_sow = sum(sow_commit.values())  # 585

    band = False
    grand_planned = 0.0
    for role, committed in sow_commit.items():
        planned = round(wbs_by_role.get(role, 0.0), 1)
        grand_planned += planned
        variance = round(planned - committed, 1)
        variance_pct = round((variance / committed) * 100, 1) if committed else 0
        ws.append(["Phase 1 (Sprints 1-7)", role, committed, planned, variance, f"{variance_pct}%"])
        r = ws.max_row
        for col in range(1, len(headers) + 1):
            c = ws.cell(row=r, column=col)
            c.border = BORDER
            c.alignment = CENTER if col != 1 and col != 2 else LEFT
            if band:
                c.fill = BAND_FILL
            if col == 6 and abs(variance_pct) > 10:
                c.fill = RED_FILL
                c.font = Font(bold=True, color="9C0006")
        band = not band

    # Grand total row
    grand_var = round(grand_planned - total_sow, 1)
    grand_var_pct = round((grand_var / total_sow) * 100, 1)
    ws.append(["TOTAL Phase 1", "(all roles)", total_sow, round(grand_planned, 1),
               grand_var, f"{grand_var_pct}%"])
    r = ws.max_row
    for col in range(1, len(headers) + 1):
        c = ws.cell(row=r, column=col)
        c.fill = HEADER_FILL
        c.font = Font(bold=True, color="FFFFFF")
        c.border = BORDER
        c.alignment = CENTER if col not in (1, 2) else LEFT

    # Hypercare line (cost reconciliation TBD)
    ws.append([])
    ws.append(["Hypercare (W14-W15)", "Fabric Data Engineer + PBI Specialist",
               "TBD", round(wbs_by_activity_role.get(("Hypercare", "Fabric Data Engineer"), 0)
                            + wbs_by_activity_role.get(("Hypercare", "Power BI Specialist"), 0)
                            + wbs_by_activity_role.get(("Hypercare", "Project Manager"), 0), 1),
               "TBD", "TBD"])
    r = ws.max_row
    for col in range(1, len(headers) + 1):
        c = ws.cell(row=r, column=col)
        c.fill = MILESTONE_FILL
        c.font = Font(bold=True, italic=True, color="9C5700")
        c.border = BORDER
        c.alignment = CENTER if col not in (1, 2) else LEFT

    # Note row
    ws.append([])
    note = "Note: Hypercare 2-week support not separately priced in Phase 1 SOW. Cost reconciliation flagged for Change Request discussion."
    ws.append([note])
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=6)
    c = ws.cell(row=ws.max_row, column=1)
    c.font = Font(italic=True, color="9C5700")
    c.alignment = LEFT
    c.fill = MILESTONE_FILL

    ws.freeze_panes = "A2"
    _autosize(ws, min_w=14, max_w=44)


# ============================================================
# Driver
# ============================================================
def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()

    ws1 = wb.active
    ws1.title = "WBS"
    build_wbs(ws1)

    ws2 = wb.create_sheet("Resource Loading")
    total_pd = build_resource_loading(ws2)

    ws3 = wb.create_sheet("Risk")
    build_risk(ws3)

    ws4 = wb.create_sheet("Assumptions")
    build_assumptions(ws4)

    ws5 = wb.create_sheet("Issue Log")
    build_issue_log(ws5)

    ws6 = wb.create_sheet("Dependencies")
    build_dependencies(ws6)

    ws7 = wb.create_sheet("Holidays")
    build_holidays(ws7)

    ws8 = wb.create_sheet("SOW - Planned Efforts")
    build_sow_planned(ws8, total_pd)

    wb.save(OUTPUT_PATH)
    print(f"Workbook written to: {OUTPUT_PATH}")
    print(f"Total WBS planned person-days: {total_pd}")
    return total_pd


if __name__ == "__main__":
    main()
