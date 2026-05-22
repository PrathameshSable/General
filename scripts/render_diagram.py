#!/usr/bin/env python3
"""Render Mermaid diagram source (.mmd) files to PNG/SVG via mmdc.

Usage:
    python3 render_diagram.py <input.mmd> [output.png|output.svg]

If output is omitted, writes alongside input with same basename and .png extension.

Used by all SOW/PPT-building agents to embed architecture diagrams and process flows
into DOCX/PPTX deliverables.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


MMDC_PUPPETEER_CONFIG = {
    "args": ["--no-sandbox", "--disable-setuid-sandbox"],
}


def render(input_path: Path, output_path: Path, theme: str = "default", background: str = "white") -> Path:
    if not input_path.exists():
        raise FileNotFoundError(f"Mermaid source not found: {input_path}")
    if shutil.which("mmdc") is None:
        raise RuntimeError("mmdc not installed. Run: npm install -g @mermaid-js/mermaid-cli")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write a puppeteer config so mmdc can run in containerized environments without sandbox.
    pp_config = output_path.parent / ".puppeteer.json"
    pp_config.write_text('{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}')

    cmd = [
        "mmdc",
        "-i", str(input_path),
        "-o", str(output_path),
        "-t", theme,
        "-b", background,
        "-p", str(pp_config),
        "--scale", "2",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"mmdc failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Mermaid diagram to PNG/SVG.")
    parser.add_argument("input", type=Path, help="Path to .mmd source file")
    parser.add_argument("output", type=Path, nargs="?", default=None, help="Output path (.png or .svg)")
    parser.add_argument("--theme", default="default", choices=["default", "dark", "forest", "neutral"])
    parser.add_argument("--background", default="white")
    args = parser.parse_args()

    output = args.output or args.input.with_suffix(".png")
    rendered = render(args.input, output, theme=args.theme, background=args.background)
    print(f"Rendered: {rendered}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
