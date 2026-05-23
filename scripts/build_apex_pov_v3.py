"""Build APEX_RU_POV_Options_v3.pptx by:

1. Starting from the original v2.1 deck
2. Duplicating slide 6 (Approach B) and rewriting it as Option 3
   (Agent Orchestration POV — assumes data + semantic model already built)
3. Rebuilding the comparison slide (slide 9) as a 3-way comparison
4. Saving as APEX_RU_POV_Options_v3.pptx

Output: outputs/APEX_RU_POV_Options_v3.pptx
"""
from __future__ import annotations

import copy
import shutil
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

SOURCE = Path("/tmp/apex_pov_options.pptx")
OUT_DIR = Path("/home/user/Fabric-Ontology-Contest/outputs")
OUT = OUT_DIR / "APEX_RU_POV_Options_v3.pptx"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------
# Step 1: Map old → new text for Option 3 (built on slide 6 layout).
# Keys are the existing text strings on slide 6; values are what
# Option 3 should say. Anything not in the map is left alone (so the
# visual chrome stays identical to Approach B).
# ------------------------------------------------------------------

OPTION3_TEXT_MAP = {
    "Approach B - Reasoning agent": "Option 3 — Agent Orchestration POV",
    "Single Foundry agent with specialist tools. Recommends reallocations.":
        "Data and semantic model already built. Build the agent orchestration layer that combines analytics Q&A and reasoning recommendations.",

    "SOURCE": "PRE-EXISTING",
    "INGEST & MODEL": "PRE-EXISTING",
    "DATA AGENT": "ORCHESTRATOR",
    "AGENT + TOOLS": "AGENTS (NEW)",
    "EXPERIENCE": "EXPERIENCE",

    "Deltek Vantagepoint": "Deltek Vantagepoint",
    "SOURCE OF TRUTH": "SOURCE — DONE",
    "SQL Server backend\nalready in APEX": "SQL Server backend\nalready in APEX",

    "~13 core tables\nTimesheets (LD)\nProjects (PR)\nEmployees (EM)\nResource Plans (RP)":
        "~13 core tables\nTimesheets (LD)\nProjects (PR)\nEmployees (EM)\nResource Plans (RP)",

    "Microsoft Fabric": "Microsoft Fabric — DONE",
    "Bronze Layer": "Bronze Layer",
    "pre-populated · raw Deltek\nAll ~13 tables present":
        "ingestion live · raw Deltek\nAll ~13 tables loaded",
    "Silver Layer": "Silver Layer",
    "cleansed, conformed\nBillability rules applied":
        "cleansed · conformed\nbillability rules applied",
    "Gold Layer": "Gold + Semantic — DONE",
    "Kimball + skills bridge\n3 facts + conformed dims\nDimSkill + BridgeEmployeeSkill":
        "Kimball model + Semantic Model\nfacts, conformed dims, ontology\nMeasures: UT %, Available Hrs",

    "Fabric Data Agent": "Orchestrator Agent",
    "GROUNDING LAYER": "ROUTES THE QUESTION",
    "Natural-language query\ninterface over Gold model":
        "Classifies user intent and\nroutes to the right agent",
    "Serves the tool calls:": "Routing rules:",
    "Utilization · Backlog · Skills":
        "Q&A → Data Agent\nRecommend → Reasoning Agent",
    "Same Gold model.\nSame numbers.\nEvery answer is grounded.":
        "Single Teams entry point.\nUser doesn't choose the agent.\nOrchestrator decides.",

    "Microsoft Foundry\n(Foundry IQ)": "Fabric Data Agent + Foundry Agent",
    "SINGLE AGENT · MULTIPLE TOOLS": "TWO AGENTS · ONE ORCHESTRATOR",
    "Resource Allocation Agent\ndecomposes · reasons · synthesizes":
        "Data Agent answers Q&A.\nReasoning Agent recommends.\nBoth share the Gold model.",

    "CALLS THESE TOOLS": "AGENT CAPABILITIES",
    "Utilization": "Q&A",
    "UT lookup": "UT, backlog, skills lookups",
    "Backlog": "Recommendations",
    "backlog lookup": "ranked reallocation options",
    "Match skills": "Multi-step",
    "skills ranking": "decomposes & synthesizes",
    "Score options": "Audit",
    "APEX scoring": "every call logged via Agent 365",

    "One agent, four tools — fewer moving parts.":
        "Two agents, one orchestrator — every question routes to the right intelligence.",

    "Microsoft Teams": "Microsoft Teams",
    "+ COPILOT STUDIO": "+ COPILOT STUDIO",
    "Conversational interface\nfor practice leads":
        "Conversational interface\nfor practice leads",
    "Where people work": "Where people work",
    "No new tool to learn\nNo new login": "No new tool to learn\nNo new login",
    "Output style:": "Output style:",
    "\"Top 3 reallocation\noptions, ranked, with\ncited rationale.\"":
        "Q&A: \"Here's the data.\"\nRecommend: \"Top 3 options\nranked, with rationale.\"",

    "GOVERNANCE LAYER": "GOVERNANCE LAYER",
    "Microsoft Entra ID — role-based access  ·  Agent 365 — audit every query  ·  Purview optional (separate scope)":
        "Microsoft Entra ID — role-based access  ·  Agent 365 — audit every query  ·  Purview optional (separate scope)",

    "WHAT THIS APPROACH IS": "WHAT THIS APPROACH IS",
    "Allocation reasoning": "Agent orchestration",
    "One Foundry agent decomposes questions, calls the right tools, and synthesizes ranked recommendations.":
        "An orchestrator inspects each user question, routes Q&A to the Data Agent and reasoning tasks to the Foundry Agent. Users see one Teams chat.",
    "Agent-driven recommendations": "Both capabilities, day one",
    "The agent proposes who to move to which project, scored against APEX rules. Leads accept or override.":
        "Practice leads can ask factual questions AND get ranked reallocation recommendations — without picking which agent to use.",
    "Simpler than it looks": "Fastest path to value",
    "Single agent + four tools is fewer moving parts than multi-agent. Cheaper to run, easier to maintain.":
        "Data work and semantic model are already done. This POV only builds the agent layer — shortest timeline of the three options.",

    "3 / 4": "3 / 5",
}


# ------------------------------------------------------------------
# Slide-duplication helper. python-pptx doesn't have copy_slide
# built-in; this clones the source slide's spTree XML and re-uses the
# same slide layout. Picture parts are referenced; embedded images are
# kept in the source rels.
# ------------------------------------------------------------------

def duplicate_slide(prs: Presentation, src_idx: int) -> int:
    """Duplicate slide at src_idx, return new slide index."""
    source = prs.slides[src_idx]
    blank_layout = source.slide_layout
    new_slide = prs.slides.add_slide(blank_layout)

    # Remove anything the layout drops onto the new slide (placeholders, etc.)
    for shape in list(new_slide.shapes):
        sp = shape._element
        sp.getparent().remove(sp)

    # Deep-copy every shape element from the source spTree
    src_spTree = source.shapes._spTree
    new_spTree = new_slide.shapes._spTree
    for child in src_spTree.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag in {"nvGrpSpPr", "grpSpPr"}:
            continue
        new_spTree.append(copy.deepcopy(child))

    # Copy rels (so picture references resolve)
    src_rels = source.part.rels
    new_rels = new_slide.part.rels
    for rel in src_rels.values():
        if "image" in rel.reltype or "media" in rel.reltype or "chart" in rel.reltype:
            new_slide.part.relate_to(rel.target_part, rel.reltype)

    return len(prs.slides) - 1


def remap_text(slide, text_map: dict[str, str]) -> None:
    """Walk every text frame, replace match-after-strip text contents using text_map."""
    # Normalize the map keys once (strip whitespace)
    norm_map = {k.strip(): v for k, v in text_map.items()}
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        full_text = shape.text_frame.text.strip()
        if full_text in norm_map:
            _replace_text_preserve_formatting(shape.text_frame, norm_map[full_text])


def _replace_text_preserve_formatting(tf, new_text: str) -> None:
    """Replace all text in a text_frame with new_text, preserving the
    formatting of the first run of the first paragraph."""
    paragraphs = list(tf.paragraphs)
    if not paragraphs:
        return
    first_para = paragraphs[0]
    template_run = None
    if first_para.runs:
        template_run = first_para.runs[0]

    # Capture template formatting
    tmpl_font = None
    if template_run:
        tmpl_font = template_run.font

    # Drop all paragraphs except the first
    p_elem = first_para._p
    for extra in paragraphs[1:]:
        extra._p.getparent().remove(extra._p)

    # Clear runs in the first paragraph
    for run in list(first_para.runs):
        run._r.getparent().remove(run._r)

    # Re-add the new content, preserving line breaks as separate paragraphs
    lines = new_text.split("\n")

    # First line into the existing paragraph
    new_run = first_para.add_run()
    new_run.text = lines[0]
    if tmpl_font:
        _copy_font(tmpl_font, new_run.font)

    # Remaining lines as new paragraphs
    for line in lines[1:]:
        new_para = tf.add_paragraph()
        if first_para.alignment is not None:
            new_para.alignment = first_para.alignment
        nr = new_para.add_run()
        nr.text = line
        if tmpl_font:
            _copy_font(tmpl_font, nr.font)


def _copy_font(src_font, dst_font) -> None:
    """Copy size/bold/italic/color/name from one Font to another."""
    if src_font.size is not None:
        dst_font.size = src_font.size
    if src_font.name is not None:
        dst_font.name = src_font.name
    if src_font.bold is not None:
        dst_font.bold = src_font.bold
    if src_font.italic is not None:
        dst_font.italic = src_font.italic
    try:
        if src_font.color.type is not None:
            if src_font.color.type == 1:  # MSO_THEME_COLOR.RGB
                dst_font.color.rgb = src_font.color.rgb
            elif src_font.color.type == 2:  # MSO_THEME_COLOR.SCHEME
                dst_font.color.theme_color = src_font.color.theme_color
    except Exception:
        pass


# ------------------------------------------------------------------
# Step 2: Rewrite the comparison slide as a 3-way comparison.
# Original is slide 9 (index 8) — same content as slide 7 but with
# real numbers. We replace it entirely with a clean 3-column version.
# ------------------------------------------------------------------

NAVY = RGBColor(0x1F, 0x2D, 0x5C)
DARK_BLUE = RGBColor(0x00, 0x4B, 0x8D)
LIGHT_GREY = RGBColor(0xF2, 0xF2, 0xF2)
ACCENT_ORANGE = RGBColor(0xE8, 0x7A, 0x2E)
TEXT_GREY = RGBColor(0x40, 0x40, 0x40)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

COMPARISON_ROWS = [
    ("Duration",         "8 weeks",                        "11 weeks",                          "[TBD] weeks"),
    ("Effort",           "~784 hours",                     "~1,030 hours",                      "[TBD] hours"),
    ("Proposed cost",    "$48k–$62k (TBF)",                "$65k–$80k (TBF)",                   "$[TBD] (TBF)"),
    ("Calculated est.",  "$50,496 (TBF)",                  "$67,916 (TBF)",                     "$[TBD] (TBF)"),
    ("What it does",     "Answers UT & backlog Q&A",       "Recommends reallocations",          "BOTH — orchestrator routes per question"),
    ("Data work",        "Build Bronze→Gold + Semantic",   "Build Bronze→Gold + Semantic",      "✓ ALREADY DONE — skipped"),
    ("AI components",    "Fabric Data Agent only",         "1 Foundry agent + 4 tools + Data Agent", "Data Agent + Foundry Agent + Orchestrator"),
    ("Recommendations",  "✗ Manager decides manually",     "✓ Agent ranks options",             "✓ Agent ranks options (when asked)"),
    ("Change mgmt",      "Light",                          "Heavier",                           "Light – Moderate"),
    ("Risk profile",     "Low",                            "Low–moderate",                      "Low — only agent layer is new"),
]


def rebuild_comparison_slide(prs: Presentation, idx: int) -> None:
    """Wipe slide `idx` and rebuild as a 3-way comparison."""
    slide = prs.slides[idx]
    # The original deck may have flagged this slide as hidden (show=0).
    # Make sure it's visible in the rebuilt version.
    sld = slide._element
    if sld.get("show") is not None:
        del sld.attrib["show"]
    # Remove every existing shape
    for shape in list(slide.shapes):
        sp = shape._element
        sp.getparent().remove(sp)

    sw = prs.slide_width
    sh = prs.slide_height

    # Title
    title = slide.shapes.add_textbox(Inches(0.4), Inches(0.25), Inches(12.5), Inches(0.55))
    tf = title.text_frame
    tf.text = "Three options compared"
    tf.paragraphs[0].runs[0].font.size = Pt(28)
    tf.paragraphs[0].runs[0].font.bold = True
    tf.paragraphs[0].runs[0].font.color.rgb = NAVY
    tf.paragraphs[0].runs[0].font.name = "Calibri"

    # Subtitle
    sub = slide.shapes.add_textbox(Inches(0.4), Inches(0.8), Inches(12.5), Inches(0.4))
    sf = sub.text_frame
    sf.text = "Same data foundation. Different intelligence layer. Different outcome."
    sf.paragraphs[0].runs[0].font.size = Pt(14)
    sf.paragraphs[0].runs[0].font.color.rgb = TEXT_GREY
    sf.paragraphs[0].runs[0].font.italic = True
    sf.paragraphs[0].runs[0].font.name = "Calibri"

    # Table region
    table_top = Inches(1.45)
    table_left = Inches(0.35)
    table_width = Inches(12.6)
    table_height = Inches(5.0)

    # Column layout: Dimension | A | B | C (Option 3)
    col_widths = [Inches(2.4), Inches(3.4), Inches(3.4), Inches(3.4)]
    col_lefts = [table_left]
    for w in col_widths[:-1]:
        col_lefts.append(col_lefts[-1] + w)

    n_rows = len(COMPARISON_ROWS) + 1  # +1 header
    row_height = Inches(5.0 / n_rows)

    # Header row
    header_labels = ["DIMENSION",
                     "APPROACH A — Analytics",
                     "APPROACH B — Reasoning",
                     "OPTION 3 — Orchestration"]
    header_fills = [NAVY, DARK_BLUE, DARK_BLUE, ACCENT_ORANGE]
    for ci, (label, fill) in enumerate(zip(header_labels, header_fills)):
        cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_lefts[ci], table_top, col_widths[ci], row_height)
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
        cell.line.color.rgb = WHITE
        cell.line.width = Pt(0.75)
        tf = cell.text_frame
        tf.margin_left = Inches(0.1)
        tf.margin_right = Inches(0.1)
        tf.text = label
        para = tf.paragraphs[0]
        para.alignment = PP_ALIGN.LEFT
        run = para.runs[0]
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = WHITE
        run.font.name = "Calibri"

    # Data rows
    for ri, row in enumerate(COMPARISON_ROWS, start=1):
        y = table_top + row_height * ri
        for ci, val in enumerate(row):
            cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_lefts[ci], y, col_widths[ci], row_height)
            fill = LIGHT_GREY if ri % 2 == 1 else WHITE
            if ci == 3:
                # Option 3 column with a soft tint to highlight it
                fill = RGBColor(0xFD, 0xEE, 0xDC) if ri % 2 == 1 else RGBColor(0xFE, 0xF6, 0xEE)
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
            cell.line.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
            cell.line.width = Pt(0.5)
            tf = cell.text_frame
            tf.margin_left = Inches(0.1)
            tf.margin_right = Inches(0.1)
            tf.word_wrap = True
            tf.text = val
            para = tf.paragraphs[0]
            para.alignment = PP_ALIGN.LEFT
            run = para.runs[0]
            run.font.size = Pt(10.5)
            run.font.color.rgb = TEXT_GREY
            run.font.name = "Calibri"
            if ci == 0:
                run.font.bold = True
                run.font.color.rgb = NAVY

    # Footnote
    footer = slide.shapes.add_textbox(Inches(0.4), Inches(6.55), Inches(12.5), Inches(0.7))
    tf = footer.text_frame
    tf.word_wrap = True
    tf.text = ("Option 3 assumes Fabric data foundation (Bronze/Silver/Gold) and Semantic Model are already in production. "
               "This is the lowest-effort path: only the agent orchestration layer is built. "
               "Pick A for faster data access, B to automate the reasoning, C to add both agent capabilities on top of work already done.")
    para = tf.paragraphs[0]
    run = para.runs[0]
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = TEXT_GREY
    run.font.name = "Calibri"

    # Footer label bottom-right
    foot_r = slide.shapes.add_textbox(Inches(10.5), Inches(7.15), Inches(2.6), Inches(0.3))
    tf = foot_r.text_frame
    tf.text = "5 / 5"
    tf.paragraphs[0].alignment = PP_ALIGN.RIGHT
    run = tf.paragraphs[0].runs[0]
    run.font.size = Pt(10)
    run.font.color.rgb = TEXT_GREY
    run.font.name = "Calibri"

    foot_l = slide.shapes.add_textbox(Inches(0.4), Inches(7.15), Inches(8.0), Inches(0.3))
    tf = foot_l.text_frame
    tf.text = "APEX Resource Intelligence  ·  Prepared by Santor  ·  Confidential"
    run = tf.paragraphs[0].runs[0]
    run.font.size = Pt(10)
    run.font.color.rgb = TEXT_GREY
    run.font.name = "Calibri"


# ------------------------------------------------------------------
# Reorder slides helper. python-pptx doesn't expose this directly; we
# manipulate the underlying sldIdLst XML to put the new Option 3 slide
# between slide 6 (Approach B) and the comparison slide.
# ------------------------------------------------------------------

def move_slide(prs: Presentation, old_idx: int, new_idx: int) -> None:
    """Move slide from old_idx to new_idx (in-place)."""
    sldIdLst = prs.slides._sldIdLst
    slides = list(sldIdLst)
    moving = slides[old_idx]
    sldIdLst.remove(moving)
    # Re-fetch after removal
    slides = list(sldIdLst)
    if new_idx >= len(slides):
        sldIdLst.append(moving)
    else:
        sldIdLst.insert(list(sldIdLst).index(slides[new_idx]), moving)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main() -> None:
    shutil.copy(SOURCE, OUT)
    prs = Presentation(str(OUT))

    print(f"Original slide count: {len(prs.slides)}")

    # 1. Duplicate slide 6 (Approach B) → becomes new last slide
    new_idx = duplicate_slide(prs, src_idx=5)
    print(f"Duplicated slide 6 → new slide at index {new_idx}")

    # 2. Rewrite the duplicate as Option 3
    new_slide = prs.slides[new_idx]
    remap_text(new_slide, OPTION3_TEXT_MAP)
    print(f"Rewrote duplicate as Option 3 — Agent Orchestration POV")

    # 3. The source deck has TWO comparison slides:
    #    - one with TBF placeholders ("-" in cost cells)
    #    - one with real numbers ($50,496, ~784 hours)
    #    We keep the real-numbers one and rebuild it as a 3-way comparison;
    #    we delete the placeholder one entirely.
    cmp_real_idx = None  # the one with $50,496
    cmp_placeholder_idx = None  # the one with "-" / TBF
    for i, s in enumerate(prs.slides):
        if i == new_idx:
            continue
        all_text = "\n".join(shp.text_frame.text for shp in s.shapes if shp.has_text_frame)
        if "Side by side" in all_text or "side by side" in all_text:
            if "$50,496" in all_text or "$67,916" in all_text or "784 hours" in all_text:
                cmp_real_idx = i
            else:
                cmp_placeholder_idx = i

    print(f"Real-numbers comparison slide at index {cmp_real_idx}")
    print(f"Placeholder comparison slide at index {cmp_placeholder_idx}")

    # Delete the placeholder comparison slide first (before rebuilding, so
    # indexes are stable for the rebuild step)
    if cmp_placeholder_idx is not None:
        xml_slides = prs.slides._sldIdLst
        slides_list = list(xml_slides)
        xml_slides.remove(slides_list[cmp_placeholder_idx])
        print(f"Removed placeholder comparison slide at index {cmp_placeholder_idx}")
        # Adjust cmp_real_idx and new_idx if they shifted
        if cmp_real_idx is not None and cmp_real_idx > cmp_placeholder_idx:
            cmp_real_idx -= 1
        if new_idx > cmp_placeholder_idx:
            new_idx -= 1

    if cmp_real_idx is not None:
        rebuild_comparison_slide(prs, cmp_real_idx)
        print(f"Rebuilt comparison slide (now at index {cmp_real_idx}) as 3-way comparison")

    # 5. Reorder: move new Option 3 slide to sit RIGHT AFTER Approach B
    #    (which was originally at index 5). After all manipulations
    #    re-find both indices, then move.
    # find Option 3 slide and Approach B slide
    opt3_idx = None
    approach_b_idx = None
    for i, s in enumerate(prs.slides):
        for shp in s.shapes:
            if shp.has_text_frame:
                t = shp.text_frame.text
                if "Option 3" in t and "Agent Orchestration" in t:
                    opt3_idx = i
                if "Approach B - Reasoning agent" in t:
                    approach_b_idx = i
        if opt3_idx is not None and approach_b_idx is not None:
            break

    if opt3_idx is not None and approach_b_idx is not None and opt3_idx != approach_b_idx + 1:
        print(f"Moving Option 3 slide from index {opt3_idx} to index {approach_b_idx + 1}")
        move_slide(prs, opt3_idx, approach_b_idx + 1)

    # 6. Move the rebuilt comparison slide ("Three options compared") so it
    #    sits BEFORE the contact slide (the original deck had the comparison
    #    at the very end after the contact). Re-find by title text.
    cmp_idx = None
    contact_idx = None
    for i, s in enumerate(prs.slides):
        for shp in s.shapes:
            if shp.has_text_frame:
                t = shp.text_frame.text
                if "Three options compared" in t:
                    cmp_idx = i
                if "sgoradia@santortech.com" in t or "Sanjay Goradia" in t:
                    contact_idx = i
        if cmp_idx is not None and contact_idx is not None:
            break

    if cmp_idx is not None and contact_idx is not None and cmp_idx > contact_idx:
        print(f"Moving comparison slide from index {cmp_idx} to index {contact_idx} (before contact)")
        move_slide(prs, cmp_idx, contact_idx)

    prs.save(str(OUT))
    print(f"\n✓ Saved: {OUT}")
    print(f"  Final slide count: {len(Presentation(str(OUT)).slides)}")


if __name__ == "__main__":
    main()
