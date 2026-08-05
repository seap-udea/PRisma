#!/usr/bin/env python3
"""generate_figures_sorting.py — Generate a Markdown report from scoring.json.

Reads the scoring JSON and outputs a Markdown file with embedded figures 
grouped by category and sorted by PPC (Z1).
"""

import sys
import json
from pathlib import Path
import glob
from collections import defaultdict

def find_figure(results_dir: Path, tag: str, kind: str):
    """Finds the figure in the figures/ directory ending with {tag}_{kind}.png"""
    figures_dir = results_dir / "figures"
    pattern = str(figures_dir / f"*{tag}_{kind}.png")
    matches = glob.glob(pattern)
    if matches:
        return f"figures/{Path(matches[0]).name}"
    # Fallback to the expected filename if not found
    return f"figures/{tag}_{kind}.png"

def format_val(val, fmt="{:.2f}"):
    if val is None:
        return "N/A"
    return fmt.format(val)

def generate_markdown(results_dir: Path):
    scoring_files = list(results_dir.glob("scoring_*.json"))
    if not scoring_files:
        print(f"Error: No scoring_*.json files found in {results_dir}. Run score_retrievals.py first.")
        return

    # Define strict category order for the report
    CATEGORY_ORDER = [
        "[Excellent] Golden Sample",
        "[Acceptable] Multimodal Angles",
        "[Degenerate] Ringless",
        "[Rejected] Unphysical Nuisance",
        "[Rejected] Poor Individual Fit",
        "[Rejected] Poor Fit",
        "[Rejected] Missing PPC"
    ]

    for scoring_file in scoring_files:
        with open(scoring_file) as f:
            results = json.load(f)

        md_path = scoring_file.with_suffix('.md')
        case = results[0].get('case', 'Unknown Case') if results else 'Unknown Case'
        planet = results[0].get('planet', 'Unknown Planet') if results else 'Unknown Planet'
        
        lines = [
            f"# {case.capitalize()} {planet.upper()} Retrievals Classification Report",
            "",
            "This report groups retrievals into strict physical categories based on a Decision Tree logic. Within each category, retrievals are ranked by their PPC ($z_1$) score.",
            ""
        ]
        
        # Group results by category
        by_category = defaultdict(list)
        for r in results:
            cat = r.get('category', 'Unknown')
            by_category[cat].append(r)
            
        # Write summary table of contents/counts
        lines.append("## Category Summary")
        for cat in CATEGORY_ORDER:
            if cat in by_category:
                lines.append(f"- **{cat}**: {len(by_category[cat])} retrievals")
        lines.append("")
        
        # Details by category
        lines.append("## Detailed Results")
        lines.append("")
        
        rank = 1
        for cat in CATEGORY_ORDER:
            if cat not in by_category:
                continue
                
            group = by_category[cat]
            lines.append(f"### Category: {cat}")
            lines.append("")
            
            lines.append("| Rank | Tag | PPC (z1) | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |")
            lines.append("|---|---|---|---|---|---|---|")
            
            for r in group:
                z1_str = format_val(r.get('raw_z1'), "{:.2f}")
                z1_min_str = format_val(r.get('z1_min'), "{:.2f}")
                fe_str = format_val(r.get('fe_p16'), "{:.2f}")
                rho_err_str = format_val(r.get('err_rho_true'), "{:.4f}")
                ang_str = format_val(r.get('angle_peaks'), "{:.1f}")
                
                lines.append(f"| {rank} | `{r['tag']}` | **{z1_str}** | {z1_min_str} | {fe_str} | {rho_err_str} | {ang_str} |")
                rank += 1
            lines.append("")
            
            for r in group:
                lines.append(f"#### {r['tag']}")
                lines.append(f"- **PPC (z1)**: {format_val(r.get('raw_z1'))}")
                lines.append(f"- **PPC (z1 min)**: {format_val(r.get('z1_min'))}")
                lines.append(f"- **Ring fe (16th)**: {format_val(r.get('fe_p16'))}")
                lines.append(f"- **err(rho_true)**: {format_val(r.get('err_rho_true'), '{:.4f}')}")
                lines.append(f"- **Angle Peaks**: {format_val(r.get('angle_peaks'), '{:.1f}')}")
                lines.append(f"- **Category**: {r.get('category', cat)}")
                lines.append("")
                
                corner_img = find_figure(results_dir, r['tag'], "corner")
                ppc_img = find_figure(results_dir, r['tag'], "ppc")
                
                lines.append(f"![Corner Plot]({corner_img})")
                lines.append("")
                lines.append(f"![PPC]({ppc_img})")
                lines.append("")
                lines.append("---")
                lines.append("")

        with open(md_path, "w") as f:
            f.write("\n".join(lines))
            
        print(f"Successfully generated markdown report at {md_path}")

def main():
    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])
    else:
        results_dir = Path(__file__).resolve().parent / "kepler_51" / "results" / "exorings"
        
    generate_markdown(results_dir)

if __name__ == "__main__":
    main()
