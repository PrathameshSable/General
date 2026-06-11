#!/usr/bin/env python3
"""Build the Lids Phase 1 — Microsoft Fabric Migration — Presales-to-Delivery Handover Deck.

Produces outputs/lids-phase-1-handover.pptx (Standard Handover Deck variant, ~17 slides;
the Phase 2/Emory Modular Release Plan slide is intentionally omitted).

Source artifacts:
  - outputs/lids-phase-1-sow.docx           (verbatim scope, acceptance, commercial)
  - outputs/lids-phase-1-wbs.xlsx           (resource loading heatmap, risks, deps, milestones)
  - outputs/diagrams/lids-phase1-target-architecture.png
  - outputs/diagrams/lids-phase1-data-flow.png
  - outputs/diagrams/lids-phase1-cicd.png

Every datum on the deck is traced back to one of the above artifacts or to the
engagement-facts pack passed in the handover brief. No invented numbers.
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu


def _emu(val) -> Emu:
    """Coerce any length-like (Inches, Emu, or raw int EMU) into an Emu."""
    if isinstance(val, Emu):
        return val
    if hasattr(val, "emu"):
        return Emu(val.emu)
    return Emu(int(val))

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "outputs" / "lids-phase-1-handover.pptx"
DIAG = REPO / "outputs" / "diagrams"
ARCH_PNG = DIAG / "lids-phase1-target-architecture.png"
FLOW_PNG = DIAG / "lids-phase1-data-flow.png"
CICD_PNG = DIAG / "lids-phase1-cicd.png"

# -----------------------------------------------------------------------------
# Brand palette / typography
# -----------------------------------------------------------------------------
NAVY = RGBColor(0x00, 0x4B, 0x8D)        # primary brand dark blue
NAVY_DK = RGBColor(0x00, 0x33, 0x66)     # title bar
ACCENT = RGBColor(0xF2, 0xA8, 0x1D)      # amber accent
TEXT = RGBColor(0x22, 0x22, 0x22)
MUTED = RGBColor(0x66, 0x66, 0x66)
LIGHT_BG = RGBColor(0xF4, 0xF6, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xC0, 0x39, 0x2B)
AMBER = RGBColor(0xE6, 0x9A, 0x12)
GREEN = RGBColor(0x2E, 0x8B, 0x57)
GREY_BORDER = RGBColor(0xCC, 0xCC, 0xCC)
HEAT_0 = RGBColor(0xF6, 0xF8, 0xFB)
HEAT_1 = RGBColor(0xCC, 0xE0, 0xF2)
HEAT_2 = RGBColor(0x88, 0xB6, 0xDA)
HEAT_3 = RGBColor(0x44, 0x8A, 0xC0)
HEAT_4 = RGBColor(0x00, 0x4B, 0x8D)

FONT = "Calibri"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

FOOTER_TEXT = "Santor Technologies — Confidential | Lids Phase 1 Fabric Migration — Presales → Delivery Handover"

# -----------------------------------------------------------------------------
# Engagement facts (from handover brief + SOW + WBS — see module docstring)
# -----------------------------------------------------------------------------
CLIENT = "Lids Holdings, Inc."
ENGAGEMENT = "Phase 1 Microsoft Fabric Migration"
ARCHETYPE = "Phase 1 Lift & Shift (Bronze + Staging only)"
START_DATE = "15-Jan-2026"
DURATION = "13 weeks implementation + 2 weeks Hypercare"
GROSS_FEE = 185_040
IMPL_FEE = 176_040
TRAINING_FEE = 9_000
PLF_FUNDING = 75_000
NET_FEE = GROSS_FEE - PLF_FUNDING
EXPENSE_CAP = 10_000
PAYMENT_TERMS = "Net 60"
CAPACITY_MONTHLY = 25_033
ONELAKE_MONTHLY = 819

# WBS Resource Loading sheet — exact values
RESOURCE_LOADING_HEADER = [
    "Role", "Total Days", "FTE-eq",
    "W1","W2","W3","W4","W5","W6","W7","W8","W9","W10","W11","W12","W13","W14","W15",
]
RESOURCE_LOADING_ROWS = [
    ("Project Manager",      27,  0.36, [5,   5,   0,   0,    0,    0,    0,    0,    0,    0,   1,    1,   9,   3,   3]),
    ("Fabric Architect",     111, 1.48, [21,  21,  4.5, 4.5,  6,    6,    4.5,  4.5,  9,    9,   4.5,  4.5, 12,  0,   0]),
    ("Fabric Data Engineer", 271, 3.61, [5,   5,   11.5,11.5, 33,   33,   36.5, 36.5, 28.5, 28.5,8,    8,   6,   10,  10]),
    ("Power BI Specialist",  75,  1.00, [0,   0,   0,   0,    0,    0,    6,    6,    26.5, 26.5,0,    0,   0,   5,   5]),
    ("Data Modeller",        25,  0.33, [0,   0,   0,   0,    0,    0,    0,    0,    0,    0,   12.5, 12.5,0,   0,   0]),
    ("Tester",               87,  1.16, [0,   0,   0,   0,    4.5,  4.5,  4.5,  4.5,  12,   12,  22.5, 22.5,0,   0,   0]),
]
TOTAL_PD = sum(r[1] for r in RESOURCE_LOADING_ROWS)  # 596

# Per-role variance vs SOW commitment (WBS sheet 'SOW - Planned Efforts')
ROLE_VARIANCE = [
    ("Project Manager",        65,  27,  -38, "-58.5%"),
    ("Fabric Architect",       65,  111,  46, "+70.8%"),
    ("Fabric Data Engineer",  195,  271,  76, "+39.0%"),
    ("Power BI Specialist",   130,   75, -55, "-42.3%"),
    ("Data Modeller",          65,   25, -40, "-61.5%"),
    ("Tester",                 65,   87,  22, "+33.8%"),
]

# Sprints and weeks for Gantt (start_week, end_week)
SPRINT_BARS = [
    ("Sprint 1 — Planning & Foundation",        1,  2),
    ("Sprint 2 — Bronze Lakehouse Build",       3,  4),
    ("Sprint 3 — Bronze Warehouse + Refactor",  5,  6),
    ("Sprint 4 — Bronze Warehouse SIT (W7 ★)",7,  8),
    ("Sprint 5 — Prod Env + Lakehouse (W10 ★)",9, 10),
    ("Sprint 6 — UAT + PBI Repoint",            11, 12),
    ("Sprint 7 — Go-Live & Cutover (W13 ★)",13, 13),
    ("Hypercare",                               14, 15),
]
MILESTONES = [
    (2,  "Planning Sign-off"),
    (7,  "Bronze Warehouse SIT-Test"),
    (10, "Prod Lakehouse + Warehouse"),
    (13, "Phase 1 Go-Live"),
    (15, "Hypercare Close"),
]

# Top risks (from WBS Risk sheet, ordered Severity High then Medium)
TOP_RISKS = [
    ("R-01", "T-SQL parity gap: Synapse Serverless → Fabric Warehouse",
     "Med", "High", "High",
     "Pre-migration T-SQL audit (Sprint 1); PySpark notebook fallback for non-portable SPs",
     "Fabric Architect"),
    ("R-02", "Fabric Warehouse query performance vs Synapse baseline",
     "Med", "High", "High",
     "Performance baseline pre-cutover; parallel run; F128 capacity buffer; plan tuning Sprint 5",
     "Fabric Architect"),
    ("R-06", "Power BI report regression after Fabric repoint",
     "Med", "High", "High",
     "2 PBI Specialists in parallel; sample repoint Sprint 4 before bulk; DAX validation; parallel run SIT",
     "Power BI Specialist"),
    ("R-07", "13-week timeline aggressive vs 456 tables / 312 views / 64 SPs",
     "Med", "High", "High",
     "Buffer week absorbed in Sprint 6 UAT; CI/CD reuse to compress Prod build; weekly EVM tracking",
     "Project Manager"),
    ("R-08", "100% record-count match at every layer is hard acceptance gate",
     "Low", "High", "Med",
     "Reconciliation harness in Sprint 2; automated row-count validators at Bronze/WH SIT",
     "Tester"),
]

# Top 5 assumptions (from WBS Assumptions sheet)
TOP_ASSUMPTIONS = [
    "Lids provisions timely access to Fabric, OneLake, Synapse (R/O), D365 Dataverse, ADF, SQL DBs, AAS, Power BI workspaces, Azure DevOps by Day 1. (SOW §9.2)",
    "F128 Prod + F64 Dev/Test + F128 Semantic capacity provisioned and billed monthly ($25,033 + $819 OneLake).",
    "Lids SMEs and Integration Team SPOCs available for discovery, validation, UAT sessions on agreed cadence. (SOW §9.1 / 9.3)",
    "Inventory accuracy: 456 tables, 312 views, 64 stored procedures, 15 schemas. (SOW §3.1)",
    "Hypercare 2 weeks post Go-Live; cost reconciliation TBD (not separately priced in Phase 1 SOW).",
]

# Top 5 dependencies (from WBS Dependencies sheet)
TOP_DEPENDENCIES = [
    ("D-01", "Lids designates SPOC for access, credentials, network", "Lids", "Day 1 (2026-01-15)"),
    ("D-02", "Fabric workspaces (Dev/QA/Prod) F128/F64 provisioned",  "Lids IT", "Sprint 1 (2026-01-22)"),
    ("D-03", "D365 Dataverse access (Test & Prod F&O) for Dataverse Link", "Lids", "Sprint 1 (2026-01-22)"),
    ("D-05", "Integration Team SPOCs (ScalziDB, EDW) for ADF repoint SIT", "Lids", "Sprint 4 (2026-02-26)"),
    ("D-10", "Microsoft Partner Funding (Azure Accelerate PLF) claim filed pre-W13", "Santor + Lids", "Pre Go-Live"),
]

# Acceptance criteria — verbatim from SOW Section 12.1
ACCEPTANCE_CRITERIA = [
    "Bronze Lakehouse fully operational with all D365 tables ingested",
    "Bronze Warehouse contains tables & 86 views with correct data",
    "All Stored procedures refactored and functioning correctly",
    "Data validation: 100% record count match between legacy and Fabric",
    "Power BI reports connected to Bronze Lakehouse, Warehouse with accurate data",
    "ADF pipelines for EDW & ScalziDB repointed using Fabric as source",
    "UAT sign-off from Lids business stakeholders",
    "Complete documentation delivered and reviewed",
    "Azure Synapse Landing and Staging databases successfully decommissioned",
]

# Out of Scope — verbatim from SOW Section 12.3
OUT_OF_SCOPE = [
    "Gold layer (Enterprise Data Warehouse) migration",
    "Fabric Semantic Models development in EDW (replacement for AAS cubes)",
    "Power BI report redesign — new visuals, pages, KPIs, or new report development",
    "Source system modifications or enhancements (D365 or ScalziDB)",
]

# In Scope — pulled from SOW Sections 5.3.1 – 5.3.5
IN_SCOPE = [
    ("Bronze Lakehouse (Landing Layer)",
     "Fabric Dataverse Link to D365 (Test+Prod F&O); 227 tables ingested; 226 views; CDC handling; monitoring + alerting."),
    ("Bronze Warehouse (Staging Layer)",
     "Fabric Data Warehouses (Test, Prod Dev, Prod Test, Prod); 329 tables migrated; 86 views; 64 stored procs refactored to T-SQL / PySpark."),
    ("ADF Pipeline Repoint",
     "Analyze existing ADF; update pipelines to source from Bronze Lakehouse + Warehouse, feeding ScalziDB and EDW via Fabric endpoint."),
    ("Power BI Reports Migration",
     "Inventory all PBI reports on Synapse/Staging; bulk-update connection strings to Fabric Bronze Lakehouse + Warehouse; validate + deploy."),
    ("CI/CD Framework",
     "Git repository structure; Dev → Test → Prod deployment pipelines; automated testing; documented deployment procedures."),
]

# Payment schedule (SOW Section 13.5)
PAYMENT_SCHEDULE = [
    ("Project Kickoff",            "20%",  37_008),
    ("Bronze Lakehouse Sign-off",  "20%",  37_008),
    ("Bronze Warehouse Sign-off",  "20%",  37_008),
    ("UAT Sign-off",               "20%",  37_008),
    ("Phase 1 Go-Live + Closure",  "20%",  37_008),
]

# Open items (red / amber / green status from handover brief)
OPEN_ITEMS = [
    ("SOW signed by both parties",                   "AMBER", "Unsigned — Table 12 blank in SOW"),
    ("WBS finalized (8 sheets, 70 tasks, 596 PD)",   "GREEN", "Delivered with this handover"),
    ("Fabric capacity provisioned (F128+F64+F128)",  "AMBER", "Client action — required by Sprint 1"),
    ("Source credentials available (D365, SQL, AAS)","AMBER", "Client action — see Dependencies D-03/D-04"),
    ("Client SPOC named (single)",                   "AMBER", "Client action — required by Day 1 (D-01)"),
    ("Kickoff date scheduled",                       "AMBER", "Target 15-Jan-2026 — confirm with Lids"),
    ("Per-role allocation variance",                 "AMBER", "Fabric Arch +71%, PM −59%, PBI −42%, DM −62% — PM to rebalance or raise CR"),
    ("Hypercare cost reconciliation",                "AMBER", "Not separately priced in Phase 1 SOW — CR likely"),
    ("Microsoft PLF claim ($75K) filed pre-W13",     "AMBER", "Joint Santor + Lids action (D-10)"),
]

# Contacts
CONTACTS = [
    ("Account Manager",       "[TBD]", "[TBD]"),
    ("Solution Architect",    "[TBD]", "[TBD]"),
    ("Engagement Manager",    "[TBD]", "[TBD]"),
    ("Delivery PM (incoming)","[TBD]", "[TBD]"),
]

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def add_blank_slide(prs: Presentation):
    blank_layout = prs.slide_layouts[6]
    return prs.slides.add_slide(blank_layout)


def set_run(run, *, text=None, size=None, bold=None, color=None, italic=None, name=FONT):
    if text is not None:
        run.text = text
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    if name is not None:
        run.font.name = name


def add_textbox(slide, x, y, w, h, *, fill=None, line=None):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    if fill is not None:
        box.fill.solid()
        box.fill.fore_color.rgb = fill
    else:
        box.fill.background()
    if line is None:
        box.line.fill.background()
    else:
        box.line.color.rgb = line
    return box


def add_rect(slide, x, y, w, h, *, fill, line=None, line_width=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        if line_width is not None:
            shape.line.width = line_width
    shape.shadow.inherit = False
    return shape


def set_paragraph(p, text, *, size=14, bold=False, color=TEXT, align=PP_ALIGN.LEFT, italic=False):
    p.alignment = align
    if not p.runs:
        run = p.add_run()
    else:
        run = p.runs[0]
    set_run(run, text=text, size=size, bold=bold, color=color, italic=italic)


def add_slide_chrome(slide, slide_no: int, title: str, subtitle: str | None = None):
    """Header bar + footer + slide number."""
    # Header bar
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.7), fill=NAVY_DK)
    # Title text
    title_box = add_textbox(slide, Inches(0.4), Inches(0.08), Inches(12.5), Inches(0.55))
    tf = title_box.text_frame
    tf.margin_top = 0
    tf.margin_bottom = 0
    p = tf.paragraphs[0]
    set_paragraph(p, title, size=22, bold=True, color=WHITE)

    if subtitle:
        sub_box = add_textbox(slide, Inches(0.4), Inches(0.75), Inches(12.5), Inches(0.35))
        sp = sub_box.text_frame.paragraphs[0]
        set_paragraph(sp, subtitle, size=12, italic=True, color=MUTED)

    # Footer
    add_rect(slide, Inches(0), Inches(7.25), SLIDE_W, Inches(0.25), fill=LIGHT_BG)
    fb = add_textbox(slide, Inches(0.4), Inches(7.27), Inches(11.5), Inches(0.22))
    fp = fb.text_frame.paragraphs[0]
    set_paragraph(fp, FOOTER_TEXT, size=8, color=MUTED)
    pn = add_textbox(slide, Inches(12.4), Inches(7.27), Inches(0.85), Inches(0.22))
    pp = pn.text_frame.paragraphs[0]
    set_paragraph(pp, f"Slide {slide_no}", size=8, color=MUTED, align=PP_ALIGN.RIGHT)


def add_bullets(slide, x, y, w, h, items: list[str], *, size=14, color=TEXT, bullet_char="• "):
    box = add_textbox(slide, x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(4)
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        set_run(run, text=f"{bullet_char}{item}", size=size, color=color)
    return box


# -----------------------------------------------------------------------------
# Slide 1: Title
# -----------------------------------------------------------------------------
def slide_title(prs):
    s = add_blank_slide(prs)
    # Background
    add_rect(s, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill=WHITE)
    # Left accent band
    add_rect(s, Inches(0), Inches(0), Inches(0.4), SLIDE_H, fill=NAVY)
    # Top wedge
    add_rect(s, Inches(0.4), Inches(0), SLIDE_W - Inches(0.4), Inches(1.3), fill=NAVY_DK)

    # Logo placeholder
    logo = add_rect(s, Inches(11.2), Inches(0.35), Inches(1.7), Inches(0.6), fill=WHITE, line=GREY_BORDER)
    lp = logo.text_frame.paragraphs[0]
    set_paragraph(lp, "[Santor Logo]", size=10, color=MUTED, align=PP_ALIGN.CENTER, italic=True)

    # Eyebrow
    eb = add_textbox(s, Inches(0.7), Inches(0.35), Inches(8), Inches(0.45))
    set_paragraph(eb.text_frame.paragraphs[0],
                  "PRESALES → DELIVERY HANDOVER",
                  size=14, bold=True, color=ACCENT)

    # Title
    tb = add_textbox(s, Inches(0.7), Inches(1.9), Inches(11.5), Inches(1.4))
    p = tb.text_frame.paragraphs[0]
    set_paragraph(p, "Lids Phase 1 — Microsoft Fabric Migration",
                  size=40, bold=True, color=NAVY)

    sb = add_textbox(s, Inches(0.7), Inches(3.2), Inches(11.5), Inches(0.7))
    set_paragraph(sb.text_frame.paragraphs[0],
                  "Foundation & Core Analytics — Bronze + Staging Lift & Shift",
                  size=20, color=TEXT)

    # Client / date / presenter block
    info_box = add_rect(s, Inches(0.7), Inches(4.4), Inches(11.9), Inches(2.0),
                       fill=LIGHT_BG)
    tf = info_box.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.2)

    def line(text, *, size=14, bold=False, color=TEXT, first=False):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        p.space_after = Pt(4)
        run = p.add_run()
        set_run(run, text=text, size=size, bold=bold, color=color)

    line(f"Client:       {CLIENT}", size=16, bold=True, color=NAVY, first=True)
    line(f"Engagement:   {ENGAGEMENT}", size=14)
    line(f"Archetype:    {ARCHETYPE}", size=14)
    line(f"Duration:     {DURATION}  |  Start: {START_DATE}", size=14)
    line(f"Net to Lids:  ${NET_FEE:,.0f}  (Gross ${GROSS_FEE:,.0f}  −  Microsoft PLF ${PLF_FUNDING:,.0f})", size=14)
    line("Presented by: Account Manager  /  Solution Architect", size=12, color=MUTED)

    # Date footer
    df = add_textbox(s, Inches(0.7), Inches(6.7), Inches(11), Inches(0.4))
    set_paragraph(df.text_frame.paragraphs[0],
                  "Handover Meeting  ·  11-Jun-2026  ·  Santor Technologies",
                  size=11, color=MUTED, italic=True)


# -----------------------------------------------------------------------------
# Slide 2: Agenda
# -----------------------------------------------------------------------------
AGENDA = [
    "Executive Summary",
    "Client Context — Drivers, Current State, Target State",
    "Engagement Archetype & Phasing",
    "Target Fabric Architecture",
    "End-to-End Data Flow",
    "CI/CD Promotion (Dev → Test → Prod)",
    "Scope — In Scope",
    "Scope — Out of Scope",
    "Fabric Capacity & Cost",
    "Resource Roster",
    "Resource Loading Heatmap (WBS)",
    "Timeline, Sprints & Milestones",
    "Top Risks",
    "Top Assumptions & Dependencies",
    "Acceptance Criteria (verbatim from SOW)",
    "Commercial Summary",
    "Open Items & Handover Actions",
    "Q&A and Contacts",
]


def slide_agenda(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Agenda", "Order of this handover briefing")
    # Two-column agenda
    half = (len(AGENDA) + 1) // 2
    col1 = AGENDA[:half]
    col2 = AGENDA[half:]

    def column(x, items, start_no):
        box = add_textbox(s, x, Inches(1.4), Inches(6.2), Inches(5.5))
        tf = box.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(8)
            num_run = p.add_run()
            set_run(num_run, text=f"{start_no + i:>2}.  ", size=14, bold=True, color=NAVY)
            txt_run = p.add_run()
            set_run(txt_run, text=item, size=14, color=TEXT)

    column(Inches(0.6), col1, 1)
    column(Inches(7.0), col2, half + 1)


# -----------------------------------------------------------------------------
# Slide 3: Executive Summary (4-quadrant)
# -----------------------------------------------------------------------------
def slide_exec_summary(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Executive Summary", "One-line view of client, scope, commercial, timeline")

    q_w = Inches(6.2)
    q_h = Inches(2.7)
    x1, x2 = Inches(0.5), Inches(6.8)
    y1, y2 = Inches(1.3), Inches(4.1)

    def quadrant(x, y, label, lines):
        bg = add_rect(s, x, y, q_w, q_h, fill=LIGHT_BG, line=GREY_BORDER)
        # Label band
        band = add_rect(s, x, y, q_w, Inches(0.5), fill=NAVY)
        bp = band.text_frame.paragraphs[0]
        set_paragraph(bp, label, size=14, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
        # Indent
        band.text_frame.margin_left = Inches(0.2)
        # Content
        cb = add_textbox(s, x + Inches(0.2), y + Inches(0.55), q_w - Inches(0.4), q_h - Inches(0.6))
        tf = cb.text_frame
        tf.word_wrap = True
        for i, (k, v) in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(6)
            kr = p.add_run()
            set_run(kr, text=f"{k}: ", size=12, bold=True, color=NAVY)
            vr = p.add_run()
            set_run(vr, text=v, size=12, color=TEXT)

    quadrant(x1, y1, "CLIENT", [
        ("Client",    CLIENT),
        ("Industry",  "Specialty retail (headwear/licensed sports)"),
        ("Sponsor",   "Lids IT / Data Platform"),
        ("Driver",    "Consolidate Synapse + SQL onto unified Fabric platform"),
    ])
    quadrant(x2, y1, "SCOPE", [
        ("Archetype", ARCHETYPE),
        ("Inventory", "456 tables · 312 views · 64 stored procs · 15 schemas"),
        ("Pattern",   "Bronze Lakehouse + Bronze Warehouse (staging convention)"),
        ("Excluded",  "Gold layer, Semantic Models, PBI redesign (Phase 2)"),
    ])
    quadrant(x1, y2, "COMMERCIAL", [
        ("Gross fee",     f"${GROSS_FEE:,} (Impl ${IMPL_FEE:,} + Training ${TRAINING_FEE:,})"),
        ("MSFT funding",  f"${PLF_FUNDING:,} Azure Accelerate PLF"),
        ("Net to Lids",   f"${NET_FEE:,}"),
        ("Terms",         f"{PAYMENT_TERMS}  ·  Expense cap ${EXPENSE_CAP:,}"),
    ])
    quadrant(x2, y2, "TIMELINE", [
        ("Start",     START_DATE),
        ("Duration",  DURATION),
        ("Sprints",   "7 two-week sprints"),
        ("Milestones","W2 Planning · W7 WH SIT · W10 Prod · W13 Go-Live · W15 HC Close"),
    ])


# -----------------------------------------------------------------------------
# Slide 4: Client Context
# -----------------------------------------------------------------------------
def slide_client_context(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Client Context", "Business drivers, current pain points, target state (verbatim from SOW §2)")

    col_w = Inches(4.1)
    col_h = Inches(5.5)
    y = Inches(1.4)
    gap = Inches(0.15)
    x1 = Inches(0.5)
    x2 = x1 + col_w + gap
    x3 = x2 + col_w + gap

    def column(x, header, items, header_color):
        # header
        h = add_rect(s, x, y, col_w, Inches(0.5), fill=header_color)
        hp = h.text_frame.paragraphs[0]
        set_paragraph(hp, header, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        # body
        body = add_rect(s, x, y + Inches(0.5), col_w, col_h - Inches(0.5),
                        fill=LIGHT_BG, line=GREY_BORDER)
        tf = body.text_frame
        tf.margin_left = Inches(0.18); tf.margin_top = Inches(0.18)
        tf.margin_right = Inches(0.15); tf.margin_bottom = Inches(0.15)
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(8)
            run = p.add_run()
            set_run(run, text=f"•  {item}", size=12, color=TEXT)

    column(x1, "BUSINESS DRIVERS", [
        "Simplify architecture: consolidate fragmented Synapse + SQL onto unified Fabric platform",
        "Improve performance via Fabric's optimized analytics engine",
        "Enable near real-time analytics through Fabric Dataverse Link",
        "Accelerate self-service BI — foundation for centralized governance",
        "Reduce TCO via SaaS-based consumption model",
    ], NAVY)

    column(x2, "CURRENT STATE PAIN", [
        "Redundant data layers — multiple copies across Landing and Staging databases",
        "Operational complexity managing separate Synapse and SQL infrastructure",
        "Scalability limits in SQL Server Landing/Staging tiers",
        "456 tables · 312 views · 64 stored procs across 15 schemas to migrate",
    ], RED)

    column(x3, "TARGET STATE", [
        "Unified data platform foundation on OneLake as common storage layer",
        "Managed infrastructure — reduced operational overhead for Landing + Staging",
        "Governance foundation prepared for centralized security and lineage (Phase 2)",
        "Synapse Serverless, Landing SQL DB, Staging SQL DB decommissioned at Phase 1 close",
    ], GREEN)


# -----------------------------------------------------------------------------
# Slide 5: Engagement Archetype & Phasing
# -----------------------------------------------------------------------------
def slide_phasing(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Engagement Archetype & Phasing",
                     "Phase 1 — Lift & Shift (Bronze + Staging only). Gold layer and Semantic Models follow in Phase 2.")

    # Ribbon
    y = Inches(2.5)
    ribbon_h = Inches(0.9)
    x0 = Inches(0.7)
    full_w = Inches(11.9)

    # Phase widths: Assessment (small), Phase 1 (large, highlighted), Phase 2 (medium)
    w_assess = Inches(2.0)
    w_p1 = Inches(5.5)
    w_p2 = Inches(4.4)

    # Assessment
    a = add_rect(s, x0, y, w_assess, ribbon_h, fill=RGBColor(0xB5, 0xC5, 0xD9))
    ap = a.text_frame.paragraphs[0]
    set_paragraph(ap, "Assessment (complete)", size=13, bold=True, color=NAVY_DK, align=PP_ALIGN.CENTER)

    # Phase 1 (THIS HANDOVER)
    p1 = add_rect(s, x0 + w_assess, y - Inches(0.15), w_p1, ribbon_h + Inches(0.3),
                  fill=NAVY, line=ACCENT, line_width=Emu(38100))
    p1p = p1.text_frame.paragraphs[0]
    set_paragraph(p1p, "Phase 1 — Bronze + Staging Lift & Shift  ★  THIS HANDOVER",
                  size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # Phase 2
    p2 = add_rect(s, x0 + w_assess + w_p1, y, w_p2, ribbon_h,
                  fill=RGBColor(0xD9, 0xE2, 0xEC))
    p2p = p2.text_frame.paragraphs[0]
    set_paragraph(p2p, "Phase 2 — Gold + Semantic Models (future)",
                  size=13, bold=True, color=NAVY_DK, align=PP_ALIGN.CENTER)

    # Phase 1 details box
    details = add_rect(s, x0 + w_assess, y + Inches(1.4), w_p1, Inches(2.4),
                      fill=LIGHT_BG, line=GREY_BORDER)
    tf = details.text_frame
    tf.margin_left = Inches(0.2); tf.margin_top = Inches(0.15)
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_paragraph(p, "Phase 1 Includes", size=13, bold=True, color=NAVY)
    for item in [
        "Bronze Lakehouse (Landing) build + 227-table D365 ingest",
        "Bronze Warehouse (Staging) build + 64 SP refactor",
        "ADF pipeline repoint (EDW + ScalziDB downstream)",
        "Power BI bulk connection-string repoint",
        "CI/CD framework (Dev → Test → Prod) + Hypercare",
    ]:
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        run = p.add_run()
        set_run(run, text=f"•  {item}", size=11, color=TEXT)

    # Phase 2 placeholder details
    f = add_rect(s, x0 + w_assess + w_p1, y + Inches(1.4), w_p2, Inches(2.4),
                fill=LIGHT_BG, line=GREY_BORDER)
    tf = f.text_frame
    tf.margin_left = Inches(0.2); tf.margin_top = Inches(0.15)
    p = tf.paragraphs[0]
    set_paragraph(p, "Phase 2 Excluded from this engagement", size=13, bold=True, color=MUTED)
    for item in [
        "Gold layer / EDW migration",
        "Fabric Semantic Models (AAS cube replacement)",
        "Power BI redesign — new visuals, KPIs, reports",
    ]:
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        run = p.add_run()
        set_run(run, text=f"•  {item}", size=11, color=MUTED, italic=True)


# -----------------------------------------------------------------------------
# Slide 6: Target Fabric Architecture (PNG)
# -----------------------------------------------------------------------------
def slide_architecture(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Target Fabric Architecture",
                     "Source (D365, Synapse, Landing/Staging SQL) → Fabric (OneLake → Bronze Lakehouse → Bronze Warehouse) → Repointed Power BI / ADF.  Gold + Semantic Models OUT OF SCOPE.")
    if ARCH_PNG.exists():
        s.shapes.add_picture(str(ARCH_PNG), Inches(0.5), Inches(1.25),
                             width=Inches(12.3), height=Inches(5.85))
    else:
        ph = add_rect(s, Inches(0.5), Inches(1.25), Inches(12.3), Inches(5.85),
                      fill=LIGHT_BG, line=RED)
        set_paragraph(ph.text_frame.paragraphs[0],
                      "[MISSING: lids-phase1-target-architecture.png]",
                      size=18, color=RED, align=PP_ALIGN.CENTER, bold=True)


# -----------------------------------------------------------------------------
# Slide 7: Data Flow (PNG)
# -----------------------------------------------------------------------------
def slide_data_flow(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "End-to-End Data Flow",
                     "Ingestion → CDC + incremental → SP refactor (T-SQL/PySpark) → ADF repoint → Power BI repoint.  Critical-path tasks annotated.")
    # Diagram is portrait-shaped; place left, with annotations on right
    if FLOW_PNG.exists():
        s.shapes.add_picture(str(FLOW_PNG), Inches(0.4), Inches(1.2),
                             height=Inches(5.9))
    # Annotations panel on right
    panel = add_rect(s, Inches(7.8), Inches(1.3), Inches(5.2), Inches(5.7),
                    fill=LIGHT_BG, line=GREY_BORDER)
    tf = panel.text_frame
    tf.margin_left = Inches(0.2); tf.margin_top = Inches(0.18)
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_paragraph(p, "Flow Annotations", size=14, bold=True, color=NAVY)
    notes = [
        ("Ingest", "Fabric Dataverse Link (CDC) ingests 227 D365 tables to Bronze Lakehouse."),
        ("Legacy retire", "Synapse Serverless, Landing SQL DB, Staging SQL DB to be decommissioned."),
        ("Refactor", "64 stored procs refactored to Fabric T-SQL / PySpark — critical path 32 PD."),
        ("Bronze Warehouse", "329 tables / 86 views / 64 SPs (Lids 'Bronze Warehouse' = staging)."),
        ("Reconciliation", "100% record-count match harness validates each layer (SOW §12.1)."),
        ("Repoint downstream", "ADF pipelines repoint to Fabric SQL endpoint feeding EDW + ScalziDB."),
        ("PBI repoint", "Bulk connection-string update for existing PBI reports — critical path 24 PD."),
    ]
    for label, body in notes:
        p = tf.add_paragraph()
        p.space_after = Pt(6)
        lr = p.add_run()
        set_run(lr, text=f"{label}: ", size=11, bold=True, color=NAVY)
        br = p.add_run()
        set_run(br, text=body, size=11, color=TEXT)


# -----------------------------------------------------------------------------
# Slide 8: CI/CD (PNG)
# -----------------------------------------------------------------------------
def slide_cicd(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "CI/CD Promotion (Dev → Test → Prod)",
                     "Azure DevOps Git integration with Fabric workspaces; deployment pipelines gated by SIT + UAT.")
    if CICD_PNG.exists():
        s.shapes.add_picture(str(CICD_PNG), Inches(0.5), Inches(1.35),
                             width=Inches(12.3))
    # caption / bullets below
    cap = add_textbox(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(1.5))
    tf = cap.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_paragraph(p, "Promotion gates", size=12, bold=True, color=NAVY)
    for line in [
        "Dev (F64) → PR + approval → Test (F64): SIT + UAT reconciliation harness must pass.",
        "Test → Prod (F128 + F128 Semantic): UAT sign-off from Lids business stakeholders is the gate (SOW §12.1).",
        "Git repository + YAML pipelines deliverable at end of Sprint 1 (Fabric Architect owns).",
    ]:
        p = tf.add_paragraph()
        p.space_after = Pt(2)
        run = p.add_run()
        set_run(run, text=f"•  {line}", size=11, color=TEXT)


# -----------------------------------------------------------------------------
# Slide 9: In Scope
# -----------------------------------------------------------------------------
def slide_in_scope(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Scope — In Scope",
                     "Five workstreams per SOW §5.3 (verbatim).  Every commitment below maps to acceptance criteria on slide 15.")

    rows = IN_SCOPE
    n_rows = len(rows)
    # Table: WS label | description
    top = Inches(1.35)
    row_h = Inches(0.95)
    x = Inches(0.5)
    w_label = Inches(3.2)
    w_desc = Inches(9.4)

    # Header
    add_rect(s, x, top, w_label, Inches(0.4), fill=NAVY)
    add_rect(s, x + w_label, top, w_desc, Inches(0.4), fill=NAVY)
    hb1 = add_textbox(s, x, top + Inches(0.05), w_label, Inches(0.3))
    set_paragraph(hb1.text_frame.paragraphs[0], "  Workstream", size=12, bold=True, color=WHITE)
    hb2 = add_textbox(s, x + w_label, top + Inches(0.05), w_desc, Inches(0.3))
    set_paragraph(hb2.text_frame.paragraphs[0], "  Commitment", size=12, bold=True, color=WHITE)

    y = top + Inches(0.4)
    for i, (label, desc) in enumerate(rows):
        fill = LIGHT_BG if i % 2 == 0 else WHITE
        add_rect(s, x, y, w_label, row_h, fill=fill, line=GREY_BORDER)
        add_rect(s, x + w_label, y, w_desc, row_h, fill=fill, line=GREY_BORDER)
        lb = add_textbox(s, x + Inches(0.1), y + Inches(0.1), w_label - Inches(0.2), row_h - Inches(0.2))
        set_paragraph(lb.text_frame.paragraphs[0], label, size=12, bold=True, color=NAVY)
        db = add_textbox(s, x + w_label + Inches(0.1), y + Inches(0.1), w_desc - Inches(0.2), row_h - Inches(0.2))
        set_paragraph(db.text_frame.paragraphs[0], desc, size=12, color=TEXT)
        y += row_h


# -----------------------------------------------------------------------------
# Slide 10: Out of Scope
# -----------------------------------------------------------------------------
def slide_out_of_scope(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Scope — Out of Scope",
                     "MANDATORY: delivery must not absorb these without a Change Order. Verbatim from SOW §12.3.")

    # Red warning banner
    banner = add_rect(s, Inches(0.5), Inches(1.35), Inches(12.3), Inches(0.6),
                     fill=RGBColor(0xF8, 0xE3, 0xDF), line=RED)
    set_paragraph(banner.text_frame.paragraphs[0],
                  "Not in Phase 1 — raise as Change Order if requested.",
                  size=14, bold=True, color=RED, align=PP_ALIGN.CENTER)

    y = Inches(2.2)
    item_h = Inches(0.85)
    for i, item in enumerate(OUT_OF_SCOPE):
        bg = add_rect(s, Inches(0.5), y, Inches(12.3), item_h,
                     fill=LIGHT_BG, line=GREY_BORDER)
        # red prohibition box
        add_rect(s, Inches(0.7), y + Inches(0.15), Inches(0.55), Inches(0.55),
                fill=RED)
        x_box = add_textbox(s, Inches(0.7), y + Inches(0.15), Inches(0.55), Inches(0.55))
        set_paragraph(x_box.text_frame.paragraphs[0], "✕",
                      size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        # text
        tb = add_textbox(s, Inches(1.5), y + Inches(0.2), Inches(11), Inches(0.55))
        set_paragraph(tb.text_frame.paragraphs[0], item, size=14, color=TEXT, bold=True)
        y += item_h + Inches(0.1)


# -----------------------------------------------------------------------------
# Slide 11: Fabric Capacity & Cost
# -----------------------------------------------------------------------------
def slide_capacity(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Fabric Capacity & Cost",
                     "SOW §7.2 recommendation — capacity provisioned by Lids; billed monthly by Microsoft.")

    # Big numbers strip
    strip_y = Inches(1.4)
    strip_h = Inches(1.2)
    cards = [
        ("F128", "Prod Capacity"),
        ("F64",  "Dev/Test Capacity"),
        ("F128", "Semantic Capacity (Phase 2 ready)"),
        (f"${CAPACITY_MONTHLY:,}",  "Total Compute / month"),
        (f"${ONELAKE_MONTHLY:,}",   "OneLake Storage / month"),
    ]
    n_cards = len(cards)
    card_gap = Inches(0.15)
    total_w = Inches(12.3)
    card_w = Emu(int((total_w.emu - card_gap.emu * (n_cards - 1)) / n_cards))
    x = Inches(0.5)
    for big, lbl in cards:
        add_rect(s, x, strip_y, card_w, strip_h, fill=NAVY)
        bb = add_textbox(s, x, strip_y + Inches(0.15), card_w, Inches(0.6))
        set_paragraph(bb.text_frame.paragraphs[0], big, size=22, bold=True, color=WHITE,
                      align=PP_ALIGN.CENTER)
        lb = add_textbox(s, x, strip_y + Inches(0.75), card_w, Inches(0.4))
        set_paragraph(lb.text_frame.paragraphs[0], lbl, size=11, color=WHITE,
                      align=PP_ALIGN.CENTER)
        x = Emu(x.emu + card_w.emu + card_gap.emu)

    # Details table
    y = Inches(3.0)
    rows = [
        ("Item", "Detail"),
        ("Prod Capacity",          "F128 — Power BI + Warehouse + Lakehouse Prod workloads"),
        ("Dev / Test Capacity",    "F64 — shared by Dev + Test workspaces; CI/CD promotion target"),
        ("Semantic Capacity",      "F128 — Phase 2 ready (AAS cube replacement)"),
        ("Monthly compute total",  f"${CAPACITY_MONTHLY:,}/month  (Azure list)"),
        ("OneLake storage",        f"${ONELAKE_MONTHLY:,}/month estimate (Delta/Parquet)"),
        ("Annualized run-rate",    f"~${(CAPACITY_MONTHLY + ONELAKE_MONTHLY) * 12:,}/year"),
        ("Headroom",               "10% peak concurrency buffer; R-05 covers right-sizing post-UAT"),
        ("Funding",                f"Microsoft Azure Accelerate PLF — ${PLF_FUNDING:,} applied against impl fee"),
    ]
    col_w1 = Inches(3.7); col_w2 = Inches(8.6); row_h = Inches(0.38)
    for i, (a, b) in enumerate(rows):
        fill = NAVY if i == 0 else (LIGHT_BG if i % 2 == 1 else WHITE)
        color = WHITE if i == 0 else TEXT
        bold = (i == 0)
        add_rect(s, Inches(0.5), y, col_w1, row_h, fill=fill, line=GREY_BORDER)
        add_rect(s, Inches(0.5) + col_w1, y, col_w2, row_h, fill=fill, line=GREY_BORDER)
        tb1 = add_textbox(s, Inches(0.6), y + Inches(0.05), col_w1 - Inches(0.2), row_h - Inches(0.1))
        set_paragraph(tb1.text_frame.paragraphs[0], a, size=11, bold=bold or i > 0, color=color if i > 0 else WHITE)
        if i == 0:
            set_paragraph(tb1.text_frame.paragraphs[0], a, size=11, bold=True, color=WHITE)
        else:
            set_paragraph(tb1.text_frame.paragraphs[0], a, size=11, bold=True, color=NAVY)
        tb2 = add_textbox(s, Inches(0.5) + col_w1 + Inches(0.1), y + Inches(0.05),
                         col_w2 - Inches(0.2), row_h - Inches(0.1))
        set_paragraph(tb2.text_frame.paragraphs[0], b, size=11,
                      bold=(i==0), color=(WHITE if i == 0 else TEXT))
        y += row_h


# -----------------------------------------------------------------------------
# Slide 12: Resource Roster
# -----------------------------------------------------------------------------
def slide_roster(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Resource Roster",
                     "9 FTE-equivalents · Total 596 person-days · Aggregated from WBS Resource Loading sheet.")

    rows = [
        ("Role", "HC", "Total PD", "FTE-eq", "Active Weeks", "Onshore / Offshore"),
        ("Project Manager",       "1", "27",  "0.36", "W1–W2, W11–W15",            "100% Onshore"),
        ("Fabric Architect",      "1", "111", "1.48", "W1–W13",                          "100% Onshore"),
        ("Fabric Data Engineer",  "3", "271", "3.61", "W1–W15 (peak W5–W10)",       "1 Onshore / 2 Offshore"),
        ("Power BI Specialist",   "2", "75",  "1.00", "W7–W10, W14–W15",            "1 Onshore / 1 Offshore"),
        ("Data Modeller",         "1", "25",  "0.33", "W11–W12",                         "Offshore"),
        ("Tester",                "1", "87",  "1.16", "W5–W12",                          "Offshore"),
        ("TOTAL",                 "9", str(TOTAL_PD), "7.95", "15 weeks (W1–W15)",       "5 Onshore / 4 Offshore"),
    ]

    y = Inches(1.4)
    col_widths = [Inches(2.6), Inches(0.7), Inches(1.1), Inches(1.0), Inches(3.7), Inches(3.2)]
    row_h = Inches(0.55)
    for i, row in enumerate(rows):
        x = Inches(0.5)
        is_header = (i == 0)
        is_total = (i == len(rows) - 1)
        fill = NAVY if is_header else (ACCENT if is_total else (LIGHT_BG if i % 2 == 1 else WHITE))
        for ci, cell in enumerate(row):
            add_rect(s, x, y, col_widths[ci], row_h, fill=fill, line=GREY_BORDER)
            tb = add_textbox(s, x + Inches(0.1), y + Inches(0.12), col_widths[ci] - Inches(0.2), row_h - Inches(0.2))
            color = WHITE if is_header else (NAVY_DK if is_total else TEXT)
            bold = is_header or is_total
            align = PP_ALIGN.CENTER if ci in (1, 2, 3) else PP_ALIGN.LEFT
            set_paragraph(tb.text_frame.paragraphs[0], cell, size=12, bold=bold,
                          color=color, align=align)
            x = Emu(x.emu + col_widths[ci].emu)
        y += row_h

    # Variance note
    note = add_textbox(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(1.0))
    tf = note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_paragraph(p, "Variance vs SOW commitment (Phase 1 only):", size=11, bold=True, color=NAVY)
    p = tf.add_paragraph()
    set_paragraph(p,
                  "Fabric Architect +70.8% · Fabric DE +39.0% · Tester +33.8%  ||  Power BI Specialist −42.3% · PM −58.5% · Data Modeller −61.5%.",
                  size=11, color=TEXT)
    p = tf.add_paragraph()
    set_paragraph(p,
                  "Mix-shift expected for Lift & Shift archetype; delivery PM to rebalance or raise Change Request. See Open Items slide.",
                  size=11, italic=True, color=MUTED)


# -----------------------------------------------------------------------------
# Slide 13: Resource Loading Heatmap
# -----------------------------------------------------------------------------
def heat_color(v: float) -> RGBColor:
    if v <= 0:
        return HEAT_0
    if v < 5:
        return HEAT_1
    if v < 15:
        return HEAT_2
    if v < 30:
        return HEAT_3
    return HEAT_4


def slide_heatmap(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Resource Loading Heatmap",
                     "Person-days per role per week — mirrors WBS 'Resource Loading' sheet exactly. No smoothing.")

    # Geometry
    top = Inches(1.35)
    left = Inches(0.3)
    role_col_w = Inches(1.7)
    week_col_w = Inches(0.6)
    total_col_w = Inches(0.75)
    fte_col_w = Inches(0.65)
    row_h = Inches(0.42)
    n_weeks = 15

    # Header row
    # Role
    add_rect(s, left, top, role_col_w, row_h, fill=NAVY)
    tb = add_textbox(s, left + Inches(0.1), top + Inches(0.08), role_col_w - Inches(0.2), row_h - Inches(0.16))
    set_paragraph(tb.text_frame.paragraphs[0], "Role", size=11, bold=True, color=WHITE)
    x = _emu(left.emu + role_col_w.emu)
    for w in range(1, n_weeks + 1):
        add_rect(s, x, top, week_col_w, row_h, fill=NAVY)
        wb = add_textbox(s, x, top + Inches(0.08), week_col_w, row_h - Inches(0.16))
        set_paragraph(wb.text_frame.paragraphs[0], f"W{w}", size=10, bold=True, color=WHITE,
                      align=PP_ALIGN.CENTER)
        x = Emu(x.emu + week_col_w.emu)
    add_rect(s, x, top, total_col_w, row_h, fill=NAVY)
    tb2 = add_textbox(s, x, top + Inches(0.08), total_col_w, row_h - Inches(0.16))
    set_paragraph(tb2.text_frame.paragraphs[0], "Total", size=10, bold=True, color=WHITE,
                  align=PP_ALIGN.CENTER)
    x = Emu(x.emu + total_col_w.emu)
    add_rect(s, x, top, fte_col_w, row_h, fill=NAVY)
    tb3 = add_textbox(s, x, top + Inches(0.08), fte_col_w, row_h - Inches(0.16))
    set_paragraph(tb3.text_frame.paragraphs[0], "FTE", size=10, bold=True, color=WHITE,
                  align=PP_ALIGN.CENTER)

    # Body rows
    y = Emu(top.emu + row_h.emu)
    week_totals = [0.0] * n_weeks
    for role, total_pd, fte_eq, weeks in RESOURCE_LOADING_ROWS:
        add_rect(s, left, y, role_col_w, row_h, fill=LIGHT_BG, line=GREY_BORDER)
        rb = add_textbox(s, left + Inches(0.1), y + Inches(0.08), role_col_w - Inches(0.2), row_h - Inches(0.16))
        set_paragraph(rb.text_frame.paragraphs[0], role, size=11, bold=True, color=NAVY)
        cx = _emu(left.emu + role_col_w.emu)
        for wi, v in enumerate(weeks):
            v = float(v) if v else 0.0
            week_totals[wi] += v
            col = heat_color(v)
            add_rect(s, cx, y, week_col_w, row_h, fill=col, line=GREY_BORDER)
            if v > 0:
                vb = add_textbox(s, cx, y + Inches(0.08), week_col_w, row_h - Inches(0.16))
                txt_color = WHITE if v >= 15 else TEXT
                disp = f"{v:.1f}" if v != int(v) else f"{int(v)}"
                set_paragraph(vb.text_frame.paragraphs[0], disp, size=9, bold=True,
                              color=txt_color, align=PP_ALIGN.CENTER)
            cx = Emu(cx.emu + week_col_w.emu)
        # totals
        add_rect(s, cx, y, total_col_w, row_h, fill=LIGHT_BG, line=GREY_BORDER)
        tt = add_textbox(s, cx, y + Inches(0.08), total_col_w, row_h - Inches(0.16))
        set_paragraph(tt.text_frame.paragraphs[0], str(total_pd), size=10, bold=True,
                      color=NAVY, align=PP_ALIGN.CENTER)
        cx = Emu(cx.emu + total_col_w.emu)
        add_rect(s, cx, y, fte_col_w, row_h, fill=LIGHT_BG, line=GREY_BORDER)
        ft = add_textbox(s, cx, y + Inches(0.08), fte_col_w, row_h - Inches(0.16))
        set_paragraph(ft.text_frame.paragraphs[0], f"{fte_eq:.2f}", size=10, bold=True,
                      color=NAVY, align=PP_ALIGN.CENTER)
        y = Emu(y.emu + row_h.emu)

    # Footer total row
    add_rect(s, left, y, role_col_w, row_h, fill=NAVY_DK)
    tb = add_textbox(s, left + Inches(0.1), y + Inches(0.08), role_col_w - Inches(0.2), row_h - Inches(0.16))
    set_paragraph(tb.text_frame.paragraphs[0], "Weekly Total", size=11, bold=True, color=WHITE)
    cx = _emu(left.emu + role_col_w.emu)
    for v in week_totals:
        add_rect(s, cx, y, week_col_w, row_h, fill=NAVY_DK)
        vb = add_textbox(s, cx, y + Inches(0.08), week_col_w, row_h - Inches(0.16))
        disp = f"{v:.0f}" if v == int(v) else f"{v:.1f}"
        set_paragraph(vb.text_frame.paragraphs[0], disp, size=10, bold=True, color=WHITE,
                      align=PP_ALIGN.CENTER)
        cx = Emu(cx.emu + week_col_w.emu)
    add_rect(s, cx, y, total_col_w, row_h, fill=NAVY_DK)
    tt = add_textbox(s, cx, y + Inches(0.08), total_col_w, row_h - Inches(0.16))
    set_paragraph(tt.text_frame.paragraphs[0], str(TOTAL_PD), size=10, bold=True, color=WHITE,
                  align=PP_ALIGN.CENTER)
    cx = Emu(cx.emu + total_col_w.emu)
    add_rect(s, cx, y, fte_col_w, row_h, fill=NAVY_DK)
    ft = add_textbox(s, cx, y + Inches(0.08), fte_col_w, row_h - Inches(0.16))
    set_paragraph(ft.text_frame.paragraphs[0], "7.95", size=10, bold=True, color=WHITE,
                  align=PP_ALIGN.CENTER)

    # Legend
    legy = Inches(6.4)
    add_textbox(s, Inches(0.5), legy, Inches(2), Inches(0.3)).text_frame.paragraphs[0].text = ""
    leg_lbl = add_textbox(s, Inches(0.5), legy, Inches(2), Inches(0.3))
    set_paragraph(leg_lbl.text_frame.paragraphs[0], "Heat intensity (PD/wk):",
                  size=11, bold=True, color=NAVY)
    legend_items = [(HEAT_0, "0"), (HEAT_1, "<5"), (HEAT_2, "5–15"),
                    (HEAT_3, "15–30"), (HEAT_4, "30+")]
    lx = Inches(2.7)
    for col, lbl in legend_items:
        add_rect(s, lx, legy + Inches(0.02), Inches(0.4), Inches(0.25), fill=col, line=GREY_BORDER)
        tb = add_textbox(s, lx + Inches(0.45), legy, Inches(0.9), Inches(0.3))
        set_paragraph(tb.text_frame.paragraphs[0], lbl, size=11, color=TEXT)
        lx = Emu(lx.emu + Inches(1.3).emu)

    # Caveat
    cv = add_textbox(s, Inches(0.5), Inches(6.85), Inches(12.3), Inches(0.3))
    set_paragraph(cv.text_frame.paragraphs[0],
                  "Source: WBS ‘Resource Loading’ sheet — reproduced without rounding or smoothing.",
                  size=10, italic=True, color=MUTED)


# -----------------------------------------------------------------------------
# Slide 14: Timeline & Milestones (Gantt)
# -----------------------------------------------------------------------------
def slide_timeline(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Timeline, Sprints & Milestones",
                     "7 Sprints over 13 weeks + 2-week Hypercare. Start: 15-Jan-2026. Milestones marked ★.")

    # Geometry
    top = Inches(1.4)
    left = Inches(3.4)
    n_weeks = 15
    chart_w = Inches(9.4)
    week_w = Emu(int(chart_w.emu / n_weeks))
    row_h = Inches(0.45)
    label_x = Inches(0.5)
    label_w = Inches(2.85)

    # Week header
    head_h = Inches(0.42)
    add_rect(s, label_x, top, label_w, head_h, fill=NAVY)
    tb = add_textbox(s, label_x + Inches(0.1), top + Inches(0.08), label_w - Inches(0.2), head_h - Inches(0.16))
    set_paragraph(tb.text_frame.paragraphs[0], "Sprint / Phase", size=11, bold=True, color=WHITE)
    for w in range(1, n_weeks + 1):
        x = Emu(left.emu + (w - 1) * week_w.emu)
        add_rect(s, x, top, week_w, head_h, fill=NAVY)
        wb = add_textbox(s, x, top + Inches(0.08), week_w, head_h - Inches(0.16))
        set_paragraph(wb.text_frame.paragraphs[0], f"W{w}", size=9, bold=True, color=WHITE,
                      align=PP_ALIGN.CENTER)

    # Bars
    y = Emu(top.emu + head_h.emu + Inches(0.05).emu)
    for label, sw, ew in SPRINT_BARS:
        # Label
        add_rect(s, label_x, y, label_w, row_h, fill=LIGHT_BG, line=GREY_BORDER)
        lb = add_textbox(s, label_x + Inches(0.1), y + Inches(0.1), label_w - Inches(0.2), row_h - Inches(0.2))
        set_paragraph(lb.text_frame.paragraphs[0], label, size=10, bold=True, color=NAVY)
        # Background grid (weeks)
        for w in range(1, n_weeks + 1):
            gx = Emu(left.emu + (w - 1) * week_w.emu)
            add_rect(s, gx, y, week_w, row_h, fill=WHITE, line=GREY_BORDER)
        # Bar
        bar_x = Emu(left.emu + (sw - 1) * week_w.emu + Inches(0.05).emu)
        bar_w = Emu((ew - sw + 1) * week_w.emu - Inches(0.1).emu)
        is_hypercare = "Hypercare" in label
        fill_color = ACCENT if is_hypercare else NAVY
        add_rect(s, bar_x, y + Inches(0.07), bar_w, row_h - Inches(0.14), fill=fill_color)
        # Bar text (week range)
        bt = add_textbox(s, bar_x, y + Inches(0.07), bar_w, row_h - Inches(0.14))
        set_paragraph(bt.text_frame.paragraphs[0], f"W{sw}–W{ew}",
                      size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        y = Emu(y.emu + row_h.emu + Inches(0.05).emu)

    # Milestone strip below
    ms_y = Emu(y.emu + Inches(0.15).emu)
    add_rect(s, label_x, ms_y, label_w, Inches(0.45), fill=ACCENT)
    mb = add_textbox(s, label_x + Inches(0.1), ms_y + Inches(0.08), label_w - Inches(0.2), Inches(0.35))
    set_paragraph(mb.text_frame.paragraphs[0], "★ Milestones", size=11, bold=True, color=NAVY_DK)
    for w in range(1, n_weeks + 1):
        gx = Emu(left.emu + (w - 1) * week_w.emu)
        ms = [m for m in MILESTONES if m[0] == w]
        bgfill = RGBColor(0xFD, 0xF5, 0xE3) if ms else WHITE
        add_rect(s, gx, ms_y, week_w, Inches(0.45), fill=bgfill, line=GREY_BORDER)
        if ms:
            sb = add_textbox(s, gx, ms_y + Inches(0.08), week_w, Inches(0.32))
            set_paragraph(sb.text_frame.paragraphs[0], "★", size=14, bold=True,
                          color=ACCENT, align=PP_ALIGN.CENTER)

    # Milestone legend at bottom
    leg = add_textbox(s, Inches(0.5), Inches(6.4), Inches(12.3), Inches(0.9))
    tf = leg.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_paragraph(p, "Milestone detail:", size=11, bold=True, color=NAVY)
    txt = "  ·  ".join([f"W{w} ★ {label}" for w, label in MILESTONES])
    p = tf.add_paragraph()
    set_paragraph(p, txt, size=11, color=TEXT)
    p = tf.add_paragraph()
    set_paragraph(p,
                  "Critical path: SP refactor (32 PD) → 227-table D365 ingest to Test (25 PD) → bulk PBI repoint (24 PD).",
                  size=11, italic=True, color=MUTED)


# -----------------------------------------------------------------------------
# Slide 15: Top Risks
# -----------------------------------------------------------------------------
def slide_risks(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Top 5 Risks",
                     "Pulled from WBS ‘Risk’ sheet, ordered by Severity. 3 Open High-severity items.")

    # Header
    top = Inches(1.35)
    col_widths = [Inches(0.6), Inches(3.6), Inches(0.7), Inches(0.7), Inches(0.7), Inches(4.7), Inches(1.3)]
    headers = ["ID", "Risk", "Lik.", "Imp.", "Sev.", "Mitigation", "Owner"]
    row_h_head = Inches(0.4)
    x = Inches(0.5)
    for ci, h in enumerate(headers):
        add_rect(s, x, top, col_widths[ci], row_h_head, fill=NAVY)
        tb = add_textbox(s, x + Inches(0.05), top + Inches(0.08), col_widths[ci] - Inches(0.1), row_h_head - Inches(0.16))
        align = PP_ALIGN.CENTER if ci in (0, 2, 3, 4) else PP_ALIGN.LEFT
        set_paragraph(tb.text_frame.paragraphs[0], h, size=11, bold=True, color=WHITE, align=align)
        x = Emu(x.emu + col_widths[ci].emu)

    y = Emu(top.emu + row_h_head.emu)
    row_h = Inches(1.0)
    sev_color = {"High": RED, "Med": AMBER, "Medium": AMBER, "Low": GREEN}
    for rid, desc, lik, imp, sev, mit, owner in TOP_RISKS:
        cells = [rid, desc, lik, imp, sev, mit, owner]
        x = Inches(0.5)
        for ci, val in enumerate(cells):
            add_rect(s, x, y, col_widths[ci], row_h, fill=LIGHT_BG, line=GREY_BORDER)
            tb = add_textbox(s, x + Inches(0.08), y + Inches(0.08), col_widths[ci] - Inches(0.16), row_h - Inches(0.16))
            align = PP_ALIGN.CENTER if ci in (0, 2, 3, 4) else PP_ALIGN.LEFT
            color = TEXT
            bold = False
            if ci == 0:
                color = NAVY; bold = True
            if ci == 4:
                # Sev pill
                color = sev_color.get(val, TEXT)
                bold = True
            set_paragraph(tb.text_frame.paragraphs[0], val, size=10, bold=bold,
                          color=color, align=align)
            x = Emu(x.emu + col_widths[ci].emu)
        y = Emu(y.emu + row_h.emu)


# -----------------------------------------------------------------------------
# Slide 16: Top Assumptions & Dependencies
# -----------------------------------------------------------------------------
def slide_assumptions(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Top Assumptions & Dependencies",
                     "Client-dependent items most critical for Day 1. Source: WBS ‘Assumptions’ + ‘Dependencies’ sheets.")

    # Left: assumptions
    col_w = Inches(6.1)
    a_x = Inches(0.5)
    d_x = Inches(6.7)
    y = Inches(1.35)
    h = Inches(5.5)

    # Headers
    add_rect(s, a_x, y, col_w, Inches(0.5), fill=NAVY)
    ah = add_textbox(s, a_x + Inches(0.15), y + Inches(0.08), col_w - Inches(0.3), Inches(0.4))
    set_paragraph(ah.text_frame.paragraphs[0], "Top 5 Assumptions",
                  size=14, bold=True, color=WHITE)
    add_rect(s, d_x, y, col_w, Inches(0.5), fill=NAVY)
    dh = add_textbox(s, d_x + Inches(0.15), y + Inches(0.08), col_w - Inches(0.3), Inches(0.4))
    set_paragraph(dh.text_frame.paragraphs[0], "Top 5 Dependencies (client-dependent for Day 1)",
                  size=14, bold=True, color=WHITE)

    # Bodies
    body_y = Emu(y.emu + Inches(0.5).emu)
    body_h = Emu(h.emu - Inches(0.5).emu)
    a_body = add_rect(s, a_x, body_y, col_w, body_h, fill=LIGHT_BG, line=GREY_BORDER)
    tf = a_body.text_frame
    tf.margin_left = Inches(0.15); tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.15); tf.margin_bottom = Inches(0.15)
    tf.word_wrap = True
    for i, item in enumerate(TOP_ASSUMPTIONS):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        ir = p.add_run()
        set_run(ir, text=f"A{i+1}.  ", size=11, bold=True, color=NAVY)
        tr = p.add_run()
        set_run(tr, text=item, size=11, color=TEXT)

    # Dependencies table-style
    d_body = add_rect(s, d_x, body_y, col_w, body_h, fill=LIGHT_BG, line=GREY_BORDER)
    tf = d_body.text_frame
    tf.margin_left = Inches(0.15); tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.15); tf.margin_bottom = Inches(0.15)
    tf.word_wrap = True
    for i, (did, desc, owner, due) in enumerate(TOP_DEPENDENCIES):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        ir = p.add_run()
        set_run(ir, text=f"{did}  ", size=11, bold=True, color=NAVY)
        tr = p.add_run()
        set_run(tr, text=f"{desc}  ", size=11, color=TEXT)
        meta = p.add_run()
        set_run(meta, text=f"— Owner: {owner}  ·  Due: {due}",
                size=10, italic=True, color=MUTED)


# -----------------------------------------------------------------------------
# Slide 17: Acceptance Criteria
# -----------------------------------------------------------------------------
def slide_acceptance(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Acceptance Criteria",
                     "Verbatim from SOW §12.1. Contractual definition of ‘done’ — delivery PM owns.")

    # Headline call-out
    co = add_rect(s, Inches(0.5), Inches(1.35), Inches(12.3), Inches(0.8),
                 fill=ACCENT)
    set_paragraph(co.text_frame.paragraphs[0],
                  "Hard acceptance gate:  100% record-count match between legacy and Fabric at every layer.",
                  size=16, bold=True, color=NAVY_DK, align=PP_ALIGN.CENTER)

    # Numbered acceptance list
    y = Inches(2.3)
    item_h = Inches(0.5)
    for i, item in enumerate(ACCEPTANCE_CRITERIA):
        bg = add_rect(s, Inches(0.5), y, Inches(12.3), item_h,
                     fill=(LIGHT_BG if i % 2 == 0 else WHITE), line=GREY_BORDER)
        # Number circle
        add_rect(s, Inches(0.65), y + Inches(0.1), Inches(0.32), Inches(0.32), fill=NAVY)
        nb = add_textbox(s, Inches(0.65), y + Inches(0.1), Inches(0.32), Inches(0.32))
        set_paragraph(nb.text_frame.paragraphs[0], str(i + 1),
                      size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        # Text
        tb = add_textbox(s, Inches(1.1), y + Inches(0.1), Inches(11.0), Inches(0.32))
        set_paragraph(tb.text_frame.paragraphs[0], item, size=12, color=TEXT)
        y = Emu(y.emu + item_h.emu + Inches(0.02).emu)


# -----------------------------------------------------------------------------
# Slide 18: Commercial Summary
# -----------------------------------------------------------------------------
def slide_commercial(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Commercial Summary",
                     "Fixed-fee + Microsoft PLF + payment schedule. SOW §13.")

    # Left: totals stack
    x = Inches(0.5)
    y = Inches(1.35)
    card_w = Inches(5.5)
    card_h = Inches(0.55)

    def card(text_l, text_r, *, fill=NAVY, color=WHITE, bold=True, sub=None):
        nonlocal y
        c = add_rect(s, x, y, card_w, card_h, fill=fill, line=GREY_BORDER)
        lb = add_textbox(s, x + Inches(0.2), y + Inches(0.08), Inches(3.2), card_h - Inches(0.16))
        set_paragraph(lb.text_frame.paragraphs[0], text_l, size=12, bold=bold, color=color)
        rb = add_textbox(s, x + Inches(3.4), y + Inches(0.08), card_w - Inches(3.6), card_h - Inches(0.16))
        set_paragraph(rb.text_frame.paragraphs[0], text_r,
                      size=14, bold=True, color=color, align=PP_ALIGN.RIGHT)
        y = Emu(y.emu + card_h.emu + Inches(0.07).emu)

    card("Implementation fee",   f"${IMPL_FEE:,.0f}", fill=NAVY, color=WHITE)
    card("Training fee",          f"${TRAINING_FEE:,.0f}", fill=NAVY, color=WHITE)
    card("Gross fee",             f"${GROSS_FEE:,.0f}",  fill=NAVY_DK, color=WHITE)
    card("− Microsoft Azure Accelerate PLF", f"− ${PLF_FUNDING:,.0f}",
         fill=RGBColor(0xE0, 0xE9, 0xF2), color=NAVY_DK)
    card("Net to Lids",           f"${NET_FEE:,.0f}",   fill=ACCENT, color=NAVY_DK)
    card("Expense cap (T&E)",     f"${EXPENSE_CAP:,.0f}", fill=LIGHT_BG, color=NAVY_DK)
    card("Payment terms",         PAYMENT_TERMS,         fill=LIGHT_BG, color=NAVY_DK)
    card("Hypercare cost",        "TBD (CR likely)",     fill=LIGHT_BG, color=AMBER)

    # Right: Payment schedule table
    px = Inches(6.3)
    py = Inches(1.35)
    pw = Inches(6.5)
    # header
    h = add_rect(s, px, py, pw, Inches(0.5), fill=NAVY)
    hb = add_textbox(s, px + Inches(0.15), py + Inches(0.08), pw - Inches(0.3), Inches(0.4))
    set_paragraph(hb.text_frame.paragraphs[0], "Payment Schedule (5 milestones × 20%)",
                  size=13, bold=True, color=WHITE)

    # Sub-header
    sub_y = Emu(py.emu + Inches(0.5).emu)
    cols = [Inches(3.8), Inches(1.2), Inches(1.5)]
    headers = ["Milestone", "%", "Amount"]
    cx = px
    for ci, txt in enumerate(headers):
        add_rect(s, cx, sub_y, cols[ci], Inches(0.4), fill=NAVY_DK)
        tb = add_textbox(s, cx + Inches(0.1), sub_y + Inches(0.08), cols[ci] - Inches(0.2), Inches(0.3))
        align = PP_ALIGN.CENTER if ci > 0 else PP_ALIGN.LEFT
        set_paragraph(tb.text_frame.paragraphs[0], txt, size=11, bold=True, color=WHITE, align=align)
        cx = Emu(cx.emu + cols[ci].emu)
    ry = Emu(sub_y.emu + Inches(0.4).emu)
    row_h = Inches(0.45)
    running = 0
    for i, (ms, pct, amt) in enumerate(PAYMENT_SCHEDULE):
        running += amt
        fill = LIGHT_BG if i % 2 == 0 else WHITE
        cx = px
        cells = [ms, pct, f"${amt:,.0f}"]
        for ci, val in enumerate(cells):
            add_rect(s, cx, ry, cols[ci], row_h, fill=fill, line=GREY_BORDER)
            tb = add_textbox(s, cx + Inches(0.1), ry + Inches(0.1), cols[ci] - Inches(0.2), row_h - Inches(0.2))
            align = PP_ALIGN.CENTER if ci == 1 else (PP_ALIGN.RIGHT if ci == 2 else PP_ALIGN.LEFT)
            set_paragraph(tb.text_frame.paragraphs[0], val, size=11, color=TEXT, align=align)
            cx = Emu(cx.emu + cols[ci].emu)
        ry = Emu(ry.emu + row_h.emu)

    # Total
    cx = px
    totals = ["Total Implementation", "100%", f"${IMPL_FEE:,.0f}"]
    for ci, val in enumerate(totals):
        add_rect(s, cx, ry, cols[ci], row_h, fill=ACCENT)
        tb = add_textbox(s, cx + Inches(0.1), ry + Inches(0.1), cols[ci] - Inches(0.2), row_h - Inches(0.2))
        align = PP_ALIGN.CENTER if ci == 1 else (PP_ALIGN.RIGHT if ci == 2 else PP_ALIGN.LEFT)
        set_paragraph(tb.text_frame.paragraphs[0], val, size=12, bold=True, color=NAVY_DK, align=align)
        cx = Emu(cx.emu + cols[ci].emu)

    # Note
    note_y = Emu(ry.emu + Inches(0.55).emu)
    nb = add_textbox(s, px, note_y, pw, Inches(0.6))
    nt = nb.text_frame
    nt.word_wrap = True
    set_paragraph(nt.paragraphs[0],
                  "Training ($9,000) invoiced separately on completion of training delivery.",
                  size=10, italic=True, color=MUTED)
    p = nt.add_paragraph()
    set_paragraph(p,
                  "PLF claim must be filed pre-W13 (D-10) to net against final-milestone invoice.",
                  size=10, italic=True, color=MUTED)


# -----------------------------------------------------------------------------
# Slide 19: Open Items & Handover Actions
# -----------------------------------------------------------------------------
def slide_open_items(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Open Items & Handover Actions",
                     "MOST IMPORTANT SLIDE OF THIS MEETING. Red/Amber/Green status per item.")

    # Status legend top-right
    leg = add_textbox(s, Inches(8.5), Inches(0.78), Inches(4.5), Inches(0.3))
    p = leg.text_frame.paragraphs[0]
    set_paragraph(p, "RAG:", size=10, bold=True, color=MUTED)

    # Three colour boxes inline (rough)
    items = OPEN_ITEMS
    top = Inches(1.35)
    row_h = Inches(0.55)
    rag_w = Inches(1.0)
    item_w = Inches(5.0)
    note_w = Inches(6.3)
    x = Inches(0.5)

    # Header
    headers = [("Status", rag_w), ("Item", item_w), ("Notes / Action", note_w)]
    cx = x
    for h, w in headers:
        add_rect(s, cx, top, w, Inches(0.4), fill=NAVY)
        tb = add_textbox(s, cx + Inches(0.1), top + Inches(0.08), w - Inches(0.2), Inches(0.3))
        align = PP_ALIGN.CENTER if h == "Status" else PP_ALIGN.LEFT
        set_paragraph(tb.text_frame.paragraphs[0], h, size=11, bold=True, color=WHITE, align=align)
        cx = Emu(cx.emu + w.emu)

    rag_fill = {
        "RED": RED, "AMBER": AMBER, "GREEN": GREEN,
    }
    rag_label = {"RED": "RED", "AMBER": "AMBER", "GREEN": "GREEN"}

    y = Emu(top.emu + Inches(0.4).emu)
    for i, (item, rag, note) in enumerate(items):
        cx = x
        # status pill cell
        cell_fill = LIGHT_BG if i % 2 == 0 else WHITE
        add_rect(s, cx, y, rag_w, row_h, fill=cell_fill, line=GREY_BORDER)
        # Pill
        pad = Inches(0.08)
        pill = add_rect(s, cx + pad, y + Inches(0.12), rag_w - Inches(0.16), Inches(0.3),
                       fill=rag_fill[rag])
        pb = add_textbox(s, cx + pad, y + Inches(0.13), rag_w - Inches(0.16), Inches(0.3))
        set_paragraph(pb.text_frame.paragraphs[0], rag_label[rag], size=9, bold=True,
                      color=WHITE, align=PP_ALIGN.CENTER)
        cx = Emu(cx.emu + rag_w.emu)
        # item
        add_rect(s, cx, y, item_w, row_h, fill=cell_fill, line=GREY_BORDER)
        ib = add_textbox(s, cx + Inches(0.1), y + Inches(0.12), item_w - Inches(0.2), row_h - Inches(0.2))
        set_paragraph(ib.text_frame.paragraphs[0], item, size=11, bold=True, color=NAVY)
        cx = Emu(cx.emu + item_w.emu)
        # note
        add_rect(s, cx, y, note_w, row_h, fill=cell_fill, line=GREY_BORDER)
        nb = add_textbox(s, cx + Inches(0.1), y + Inches(0.12), note_w - Inches(0.2), row_h - Inches(0.2))
        set_paragraph(nb.text_frame.paragraphs[0], note, size=11, color=TEXT)
        y = Emu(y.emu + row_h.emu)

    # Footer call-out
    cb = add_rect(s, Inches(0.5), Inches(6.85), Inches(12.3), Inches(0.32),
                 fill=NAVY)
    set_paragraph(cb.text_frame.paragraphs[0],
                  "Action: Delivery PM to drive every AMBER to GREEN before kickoff (Day 1 = 15-Jan-2026).",
                  size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# -----------------------------------------------------------------------------
# Slide 20: Contacts / Q&A
# -----------------------------------------------------------------------------
def slide_contacts(prs, n):
    s = add_blank_slide(prs)
    add_slide_chrome(s, n, "Q&A and Contacts",
                     "Escalation contacts for the Lids Phase 1 delivery team.")

    # Big "Q&A"
    qa = add_textbox(s, Inches(0.5), Inches(1.5), Inches(6), Inches(2))
    set_paragraph(qa.text_frame.paragraphs[0], "Q & A", size=80, bold=True, color=NAVY)

    sub = add_textbox(s, Inches(0.5), Inches(3.6), Inches(6), Inches(0.6))
    set_paragraph(sub.text_frame.paragraphs[0],
                  "Questions, escalations, and handover actions.",
                  size=14, color=TEXT)
    sub2 = add_textbox(s, Inches(0.5), Inches(4.1), Inches(6), Inches(0.6))
    set_paragraph(sub2.text_frame.paragraphs[0],
                  "Suggested next step: circulate this deck 24h before the handover meeting.",
                  size=12, italic=True, color=MUTED)

    # Right: contacts table
    x = Inches(7.0)
    y = Inches(1.4)
    w = Inches(5.8)
    h = Inches(0.5)
    # header
    add_rect(s, x, y, w, h, fill=NAVY)
    tb = add_textbox(s, x + Inches(0.2), y + Inches(0.1), w - Inches(0.4), h - Inches(0.2))
    set_paragraph(tb.text_frame.paragraphs[0], "Contacts", size=14, bold=True, color=WHITE)

    body_y = Emu(y.emu + h.emu)
    row_h = Inches(0.7)
    for i, (role, name, email) in enumerate(CONTACTS):
        fill = LIGHT_BG if i % 2 == 0 else WHITE
        add_rect(s, x, body_y, w, row_h, fill=fill, line=GREY_BORDER)
        rb = add_textbox(s, x + Inches(0.2), body_y + Inches(0.1), w - Inches(0.4), row_h - Inches(0.2))
        tf = rb.text_frame
        p = tf.paragraphs[0]
        set_paragraph(p, role, size=12, bold=True, color=NAVY)
        p2 = tf.add_paragraph()
        set_paragraph(p2, f"{name}  ·  {email}", size=11, color=TEXT)
        body_y = Emu(body_y.emu + row_h.emu)

    # Footer pointer to artifacts
    af = add_textbox(s, Inches(0.5), Inches(6.7), Inches(12.3), Inches(0.5))
    set_paragraph(af.text_frame.paragraphs[0],
                  "Source artifacts: outputs/lids-phase-1-sow.docx  ·  outputs/lids-phase-1-wbs.xlsx  ·  outputs/diagrams/lids-phase1-*.png",
                  size=10, italic=True, color=MUTED, align=PP_ALIGN.CENTER)


# -----------------------------------------------------------------------------
# Build
# -----------------------------------------------------------------------------
def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_title(prs)                  # 1
    slide_agenda(prs, 2)              # 2
    slide_exec_summary(prs, 3)        # 3
    slide_client_context(prs, 4)      # 4
    slide_phasing(prs, 5)             # 5
    slide_architecture(prs, 6)        # 6
    slide_data_flow(prs, 7)           # 7
    slide_cicd(prs, 8)                # 8
    slide_in_scope(prs, 9)            # 9
    slide_out_of_scope(prs, 10)       # 10
    # Modular Release Plan slide intentionally omitted (Phase 2 / Emory only)
    slide_capacity(prs, 11)           # 11
    slide_roster(prs, 12)             # 12
    slide_heatmap(prs, 13)            # 13
    slide_timeline(prs, 14)           # 14
    slide_risks(prs, 15)              # 15
    slide_assumptions(prs, 16)        # 16
    slide_acceptance(prs, 17)         # 17
    slide_commercial(prs, 18)         # 18
    slide_open_items(prs, 19)         # 19
    slide_contacts(prs, 20)           # 20

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    return OUT, len(prs.slides)


if __name__ == "__main__":
    path, n_slides = build()
    print(f"Built: {path}  ({n_slides} slides)")
