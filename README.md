# lab-claude-skills

Claude Code skills for the lab. Currently contains the **manuscript_graphs** skill for generating publication-quality matplotlib figures.

---

## manuscript_graphs skill

Generates publication-ready figures using `ms_style.py` — a styling module built on matplotlib/seaborn with colorblind-safe palettes, journal presets, and consistent typography.

### What it does

- Guides you through graph type, color palette, text size, and target journal via interactive questions before writing any code
- Applies the correct rcParams for the chosen journal automatically
- Provides copy-paste recipes for 9 common graph types
- Enforces best practices: L-frame axes, colorblind-safe palettes, data points shown when N < 30, stat brackets, and proper save settings (300 dpi, tight bbox, white background)

### Supported graph types

| Type | Best for |
|------|----------|
| Bar + strip | Treatment comparisons (mean ± SD + individual points) |
| Box + strip | Distributions, N ≥ 10 (median + IQR + points) |
| Violin + strip | Full distribution shape visible |
| Time series | State occupancy, fluorescence traces |
| Scatter / PHATE | 2D embeddings coloured by category |
| Confusion matrix | Classification performance (heatmap) |
| Grouped bar | Side-by-side model/condition comparison |
| Stacked bar | State composition / proportion data |
| Diverging bar | Fold-change / log2FC feature ranking |

### Journal presets

`ms.apply_journal('nature')` configures rcParams and prints all requirements for:

`nature` · `cell` · `jci` · `blood` · `pnas` · `elife` · `jcb` · `j_microscopy` · `frontiers` · `plos`

---

## Installation

### 1. Clone this repo

```bash
git clone https://github.com/eliasbatshon/lab-claude-skills.git
cd lab-claude-skills
```

### 2. Copy the skill files

**Option A — project-local (recommended):**
Installs the skill only for a specific project. Run this from inside the cloned repo:
```bash
cp SKILL.md ms_style.py /path/to/your/project/.agents/skills/manuscript_graphs/
```
Replace `/path/to/your/project/` with your actual project directory (e.g. `~/Documents/GitHub/NETosisProject`).

**Option B — user-global (available in all Claude Code sessions):**
```bash
mkdir -p ~/.claude/skills/manuscript_graphs/
cp SKILL.md ms_style.py ~/.claude/skills/manuscript_graphs/
```

### Python dependencies

```bash
pip install -r requirements.txt
```

Or with conda:
```bash
conda install matplotlib seaborn pandas numpy scikit-learn
```

---

## How to invoke

In any Claude Code session, type:

```
/manuscript_graphs
```

Claude will ask three questions (graph type, data location, style settings) before writing any plotting code.

---

## Running the demo

The demo script renders all 9 plot types using synthetic data and saves them to `demo_output/`.

```bash
# with conda env
conda run -n <your-env> python all_plots_demo.py

# or with pip env active
python all_plots_demo.py
```

Output files:
- `demo_output/all_plots.png` — raster preview (300 dpi)
- `demo_output/all_plots.pdf` — vector submission copy

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition — loaded by Claude Code |
| `ms_style.py` | Styling module (import this in your scripts) |
| `all_plots_demo.py` | 9-panel showcase of every plot type and style setting |
| `demo_figure.py` | Minimal single-figure example |
| `walkthrough_figure.py` | Annotated walkthrough for new users |
| `walkthrough_box.py` | Box + strip walkthrough |
| `requirements.txt` | Python package dependencies |
