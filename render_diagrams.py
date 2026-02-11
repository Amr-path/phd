#!/usr/bin/env python3
"""Extract TikZ diagrams from chap-design.tex and render them as PNG files."""

import os
import re
import subprocess
import tempfile
import shutil

FIGURES_DIR = "/home/user/phd/figures"
CHAPTER_FILE = "/home/user/phd/chap-design.tex"

# Standalone LaTeX preamble that mirrors the thesis packages
PREAMBLE = r"""
\documentclass[border=10pt,varwidth=\maxdimen]{standalone}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc, fit, backgrounds}
\usepackage{enumitem}
\begin{document}
"""

POSTAMBLE = r"""
\end{document}
"""


def extract_tikz_figures(tex_path):
    """Extract all TikZ figure environments from a .tex file."""
    with open(tex_path, "r") as f:
        content = f.read()

    # Find all figure environments that contain tikzpicture
    # Pattern: \begin{figure}...\begin{tikzpicture}...\end{tikzpicture}...\end{figure}
    figures = []
    fig_pattern = re.compile(
        r"\\begin\{figure\}.*?"
        r"(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})"
        r".*?"
        r"\\label\{(fig:\w+)\}"
        r".*?"
        r"\\end\{figure\}",
        re.DOTALL,
    )

    for match in fig_pattern.finditer(content):
        tikz_code = match.group(1)
        label = match.group(2)
        # Clean up the label to make a filename
        filename = label.replace("fig:", "").replace("_", "_")
        figures.append((filename, tikz_code))

    return figures


def render_tikz_to_png(name, tikz_code, output_dir, dpi=300):
    """Render a TikZ diagram to PNG via pdflatex + pdftoppm."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, f"{name}.tex")
        pdf_path = os.path.join(tmpdir, f"{name}.pdf")

        # Write standalone LaTeX file
        clean_code = tikz_code

        # Replace \eqref{...} cross-references with hardcoded text since
        # standalone compilation has no access to the thesis equation counters.
        # The formulas are already shown inline, so we just remove the Eq. refs.
        clean_code = clean_code.replace(
            r"via Eq.~\eqref{eq:radius_standard}", ""
        )
        clean_code = clean_code.replace(
            r"via Eq.~\eqref{eq:radius_gradient}", ""
        )
        # Catch any remaining \eqref and remove them
        clean_code = re.sub(r"\\eqref\{[^}]*\}", "", clean_code)

        latex_content = PREAMBLE + "\n" + clean_code + "\n" + POSTAMBLE
        with open(tex_path, "w") as f:
            f.write(latex_content)

        # Compile with pdflatex
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            print(f"  ERROR compiling {name}:")
            # Print last 30 lines of log for debugging
            log_lines = result.stdout.split("\n")
            for line in log_lines[-30:]:
                if line.strip():
                    print(f"    {line}")
            return False

        if not os.path.exists(pdf_path):
            print(f"  ERROR: PDF not created for {name}")
            return False

        # Convert PDF to PNG using pdftoppm
        png_prefix = os.path.join(tmpdir, name)
        result = subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), "-singlefile", pdf_path, png_prefix],
            capture_output=True,
            text=True,
            timeout=30,
        )

        png_path = png_prefix + ".png"
        if not os.path.exists(png_path):
            print(f"  ERROR: PNG not created for {name}")
            return False

        # Copy to output directory
        output_path = os.path.join(output_dir, f"{name}.png")
        shutil.copy2(png_path, output_path)
        file_size = os.path.getsize(output_path) / 1024
        print(f"  OK: {output_path} ({file_size:.0f} KB)")
        return True


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)

    print("Extracting TikZ diagrams from thesis...")
    figures = extract_tikz_figures(CHAPTER_FILE)
    print(f"Found {len(figures)} TikZ diagrams.\n")

    success = 0
    for name, tikz_code in figures:
        print(f"Rendering: {name}")
        if render_tikz_to_png(name, tikz_code, FIGURES_DIR):
            success += 1

    print(f"\nDone: {success}/{len(figures)} diagrams rendered to {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
