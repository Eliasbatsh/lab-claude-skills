---
description: Create publication-quality (manuscript-ready) matplotlib figures for the NETosis project
---

# Manuscript Graph Skill

Use this skill whenever the user asks for a plot that needs to be "publication-ready", "manuscript-ready", or "submission quality".

---

## BEFORE GENERATING — Ask these questions first (two calls)

**Before writing any plotting code**, fire two `AskUserQuestion` calls in sequence. Do not skip this step.

### Call 1 — What and where

```python
# NOTE: AskUserQuestion max 4 options per question.
# Graph types are grouped; follow up if user picks "Something else".
AskUserQuestion(questions=[
  {
    "question": "What type of graph do you want to make?",
    "header": "Graph type",
    "multiSelect": False,
    "options": [
      {"label": "Bar + strip",    "description": "Bar chart (mean ± SD) with individual data points. Best for treatment comparisons."},
      {"label": "Box + strip",    "description": "Box-and-whisker with individual points. Best for N ≥ 10, shows median and IQR."},
      {"label": "Violin + strip", "description": "Full distribution shape plus individual data points."},
      {"label": "Something else", "description": "Time series, Scatter/PHATE, Confusion matrix, Grouped bar, Stacked bar, or Diverging bar — specify below."},
    ]
  },
  {
    "question": "Where is the data?",
    "header": "Data location",
    "multiSelect": False,
    "options": [
      {"label": "Use demo / fake data",     "description": "Generate synthetic data matching the plot type — good for testing."},
      {"label": "feature_analysis/ directory", "description": "Parquet or CSV files in the feature_analysis/ folder."},
      {"label": "Results_HMM/ directory",   "description": "HMM output files (state sequences, probabilities, confusion matrices)."},
      {"label": "I'll type the path",       "description": "Type the exact file path or variable name in the text box."},
    ]
  }
])
```

If user picks "Something else", immediately ask a follow-up:
```python
AskUserQuestion(questions=[
  {
    "question": "Which plot type?",
    "header": "Graph type",
    "multiSelect": False,
    "options": [
      {"label": "Time series",      "description": "Multi-line plot over time. State occupancy, fluorescence traces, etc."},
      {"label": "Scatter / PHATE",  "description": "2D scatter coloured by category. Dimensionality reduction outputs."},
      {"label": "Confusion matrix", "description": "Heatmap of classification performance. Uses SEQ_CMAP (Blues)."},
      {"label": "Grouped / Stacked / Diverging bar", "description": "Side-by-side grouped bars, stacked composition, or fold-change — specify which below."},
    ]
  }
])
```

### Call 2 — Style settings

```python
AskUserQuestion(questions=[
  {
    "question": "Which color palette do you want to use?",
    "header": "Color palette",
    "multiSelect": False,
    "options": [
      {"label": "Okabe-Ito (Recommended)", "description": "Gold-standard colorblind-safe palette (Wong 2011, Nature Methods). Project default."},
      {"label": "Paul Tol Bright",         "description": "Crisper, more saturated. Also colorblind-safe. Good for slides."},
      {"label": "Paul Tol Muted",          "description": "9 soft colors. Best when you have many categories."},
      {"label": "Custom / Other",          "description": "Specify hex codes or palette name in the text box."},
    ]
  },
  {
    "question": "Which text size profile do you want?",
    "header": "Text size",
    "multiSelect": False,
    "options": [
      {"label": "Standard (labels 8 pt, ticks 7 pt)", "description": "Project default — good for in-lab review. Slightly above journal minimum."},
      {"label": "Strict journal (labels 6 pt, ticks 5 pt)", "description": "Nature/Cell strict maximum. Use for final submission."},
      {"label": "Presentation (labels 10 pt, ticks 9 pt)", "description": "Larger text for talks, posters, or small reproductions."},
    ]
  },
  {
    "question": "Which journal are you targeting?",
    "header": "Target journal",
    "multiSelect": False,
    "options": [
      {"label": "Nature / Nature Communications",    "description": "Arial 5-7 pt, lowercase panel labels (a, b, c), 88/180 mm cols, vector PDF/EPS."},
      {"label": "Cell Press (Cell, Immunity, etc.)", "description": "Avenir/Arial 7 pt, uppercase panel labels, 85/170 mm cols, 1000 DPI or PDF."},
      {"label": "JCI",                              "description": "Arial, uppercase panel labels (Roman), 600 ppi TIFF. BAR-ONLY PLOTS PROHIBITED."},
      {"label": "No specific journal / in-lab use", "description": "Use project defaults — no journal-specific constraints."},
      {"label": "Other — I'll specify",             "description": "Type the journal name and I will look up its requirements."},
    ]
  }
])
```

### How to use the answers

| Answer | What to do |
|--------|-----------|
| Graph type | Choose the matching recipe from **Common graph recipes** below |
| Demo data | Generate synthetic data from the matching recipe |
| Real data path | Load with `pd.read_parquet(path)` / `pd.read_csv(path)` as appropriate |
| Okabe-Ito | Use `ms.TREATMENT_COLORS` / `ms.STATE_COLORS` as-is |
| Tol Bright / Muted | `pal = ms.get_palette('tol_bright')` or `'tol_muted'` |
| Custom | Apply user-provided hex codes directly |
| Standard text | `ms.apply()` — no offset |
| Strict journal | `ms.apply(font_size_offset=-2)` |
| Presentation | `ms.apply(font_size_offset=+2)` |
| Named journal preset | `preset = ms.apply_journal('nature')` — prints all requirements |
| "Other" journal | Web-search `[journal name] figure guidelines author instructions`, extract requirements, apply manually |

---

## Step 1 — Import and apply

```python
import sys
sys.path.insert(0, '/Users/eliasbatshon/Documents/GitHub/NETosisProject/.agents/skills/manuscript_graphs/')
import ms_style as ms

ms.apply()                     # default (8/7 pt, Okabe-Ito)
# or
preset = ms.apply_journal('nature')   # journal-specific sizing + prints requirements
```

---

## Step 2 — Figure sizes

| Constant | Size (in) | Use for |
|----------|-----------|---------|
| `ms.SINGLE` | 3.5 × 3.0 | Single-column small panel |
| `ms.SINGLE_TALL` | 3.5 × 4.0 | Single-column portrait |
| `ms.DOUBLE` | 7.0 × 3.0 | Wide single row of panels |
| `ms.DOUBLE_TALL` | 7.0 × 4.5 | Multi-row panels |
| `ms.DOUBLE_SQ` | 7.0 × 7.0 | Confusion matrices, heatmaps |

---

## Step 3 — Color palettes

### Option A — Okabe-Ito (DEFAULT)
```python
ms.TREATMENT_COLORS   # already Okabe-Ito
ms.STATE_COLORS       # already Okabe-Ito
pal = ms.get_palette('okabe_ito')
```
| Role | Hex |
|------|-----|
| Ctrl / resting | `#0072B2` |
| LPS / priming  | `#CC79A7` |
| Aux            | `#E69F00` |
| PMA / strong   | `#D55E00` |

### Option B — Paul Tol Bright
```python
pal = ms.get_palette('tol_bright')
# blue #4477AA, cyan #66CCEE, green #228833, yellow #CCBB44, red #EE6677, purple #AA3377
```

### Option C — Paul Tol Muted
```python
pal = ms.get_palette('tol_muted')
# rose #CC6677, indigo #332288, sand #DDCC77, green #117733, cyan #88CCEE ...
```

---

## Step 4 — Apply style to axes

```python
ms.style_ax(ax)            # standard plots (L-frame, grid, ticks)
ms.style_ax_heatmap(ax)    # heatmaps / confusion matrices
```

---

## Step 5 — Labels and font sizes

| Constant | Default | Use |
|----------|---------|-----|
| `ms.TITLE_SIZE` | 9 | Panel title |
| `ms.LABEL_SIZE` | 8 | Axis labels |
| `ms.TICK_SIZE` | 7 | Tick labels |
| `ms.LEGEND_SIZE` | 7 | Legend entries |
| `ms.ANNOT_SIZE` | 7 | Stat brackets, in-figure text |

```python
ax.set_title('Title', fontsize=ms.TITLE_SIZE, pad=5)
ax.set_xlabel('X', fontsize=ms.LABEL_SIZE, labelpad=3)
ax.set_ylabel('Y', fontsize=ms.LABEL_SIZE, labelpad=3)
ax.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc')
```

---

## Step 6 — Error bars and data display

Always show individual data points when N < 30. JCI explicitly prohibits bar-only graphs.

```python
# Preferred: bar + strip
sns.barplot(data=df, x='treatment', y='value',
            order=ms.TREATMENT_ORDER, hue='treatment', palette=ms.TREATMENT_COLORS,
            errorbar='sd', capsize=0.12, ax=ax, legend=False)
sns.stripplot(data=df, x='treatment', y='value',
              order=ms.TREATMENT_ORDER, color='#333333',
              alpha=0.5, size=3, jitter=True, ax=ax)
```

Always define error bars in the legend: *"mean ± SD"*, *"mean ± SEM"*, or *"95% CI"*.

---

## Step 7 — Statistical annotations

```python
ms.stat_annot(ax, x1=0, x2=3, y=max_y*1.05, h=max_y*0.03, p_val=0.001)
```

Auto-converts: `ns` (>0.05) / `*` (≤0.05) / `**` (≤0.01) / `***` (≤0.001) / `****` (≤0.0001)

Always define symbols in the legend.

---

## Step 8 — Panel labels

```python
ms.panel_label(ax, 'A')    # Cell/JCI/PNAS — uppercase
ms.panel_label(ax, 'a')    # Nature family — lowercase
```

---

## Step 9 — Saving

```python
# Save both for every figure:
fig.savefig('figure.pdf', dpi=300, bbox_inches='tight', facecolor='white')  # submission
fig.savefig('figure.png', dpi=300, bbox_inches='tight', facecolor='white')  # review
# or use:
ms.save(fig, 'figure.pdf')   # also closes the figure
```

---

## Journal requirements table

| Journal | Font | Text pt | Panel labels | Single col | Double col | Line art | Halftone | Format | Color | Special |
|---------|------|---------|--------------|-----------|-----------|----------|----------|--------|-------|---------|
| **Nature / Nat. Comms** | Arial/Helvetica | 5–7 pt | lowercase **a, b** (8 pt bold) | 88 mm | 180 mm | vector / 1200 DPI | 300 DPI | PDF/EPS/AI | RGB | Min line 1 pt |
| **Cell Press** | Avenir/Arial | 6–8 pt | UPPERCASE A, B (7 pt) | 85 mm | 170 mm | 1000 DPI / PDF | 300 DPI | PDF/EPS/TIFF | RGB | — |
| **JCI** | Arial | 6–12 pt | UPPERCASE A, B (Roman) | 85 mm | 170 mm | 600 ppi TIFF | 600 ppi | TIFF | RGB | **Bar-only plots banned** |
| **Blood** | Arial | 9–12 pt | uppercase | 88 mm | 180 mm | 1000 DPI | 300 DPI | TIFF only | RGB | — |
| **PNAS** | Arial | 6–8 pt | UPPERCASE A, B | 88 mm | 180 mm | 1200 DPI / vector | 300 DPI | TIFF/EPS/PDF | RGB | LZW compression |
| **eLife** | Arial | 7–12 pt | uppercase | 88 mm | 180 mm | 300 DPI | 300 DPI | JPG/PPT | RGB | Discourages bar-only |
| **JCB** | Arial | 5–8 pt | UPPERCASE A, B (bold) | 85 mm | 176 mm | 1200 DPI / vector | 300 DPI | PDF/EPS/TIFF | RGB | Min font 5 pt |
| **J. Microscopy (Wiley)** | Arial | 8–12 pt | uppercase | 88 mm | 178 mm | 1200 DPI / EPS | 300 DPI | EPS/TIFF | CMYK | CMYK; embed fonts; scale bars required |
| **Frontiers** | Arial | 8–12 pt | uppercase | 90 mm | 180 mm | 300 DPI | 300 DPI | TIFF/EPS/PDF | RGB | — |
| **PLOS ONE/Biology** | Arial | 8–12 pt | UPPERCASE A, B (bold) | 90 mm | 180 mm | 300 DPI | 300 DPI | TIFF/EPS/PDF | RGB | — |

Use `ms.apply_journal('nature')` etc. to auto-configure rcParams and print a requirements reminder.

---

## Common graph recipes

### Bar + strip (treatment comparison)
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.SINGLE_TALL)
sns.barplot(data=df, x='treatment', y='value',
            order=ms.TREATMENT_ORDER, hue='treatment', palette=ms.TREATMENT_COLORS,
            errorbar='sd', capsize=0.12, ax=ax, legend=False)
sns.stripplot(data=df, x='treatment', y='value',
              order=ms.TREATMENT_ORDER, color='#333333',
              alpha=0.5, size=3, jitter=True, ax=ax)
ms.style_ax(ax)
ax.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
ax.set_ylabel('Metric', fontsize=ms.LABEL_SIZE, labelpad=3)
ax.set_title('Title', fontsize=ms.TITLE_SIZE)
ms.save(fig, 'output.pdf')
```

### Box + strip (distribution, preferred for N ≥ 10)
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.SINGLE_TALL)
sns.boxplot(data=df, x='treatment', y='value',
            order=ms.TREATMENT_ORDER, hue='treatment', palette=ms.TREATMENT_COLORS,
            width=0.5, linewidth=0.8, fliersize=0, ax=ax, legend=False)
sns.stripplot(data=df, x='treatment', y='value',
              order=ms.TREATMENT_ORDER, color='#333333',
              alpha=0.55, size=3, jitter=True, ax=ax)
ms.style_ax(ax)
ax.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
ax.set_ylabel('Metric', fontsize=ms.LABEL_SIZE, labelpad=3)
ax.set_title('Title', fontsize=ms.TITLE_SIZE)
ms.save(fig, 'output.pdf')
```

### Violin + strip (distribution shape visible)
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.SINGLE_TALL)
pal = {ms.STATE_SHORT[s]: ms.STATE_COLORS[s] for s in ms.STATE_ORDER}
sns.violinplot(data=df, x='State', y='value', order=state_short_order,
               hue='State', palette=pal, inner=None, linewidth=0.6,
               ax=ax, legend=False, alpha=0.55)
sns.stripplot(data=df, x='State', y='value', order=state_short_order,
              hue='State', palette=pal, size=2.5, alpha=0.7,
              jitter=True, ax=ax, legend=False)
ms.style_ax(ax)
ms.save(fig, 'output.pdf')
```

### Time series (state occupancy)
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.DOUBLE)
for state in ms.STATE_ORDER:
    ax.plot(time, data[state], color=ms.STATE_COLORS[state],
            label=ms.STATE_SHORT[state], linewidth=1.2)
ms.style_ax(ax)
ax.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc')
ms.save(fig, 'output.pdf')
```

### Confusion matrix heatmap
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.DOUBLE_SQ)
im = ax.imshow(cm_norm, cmap=ms.SEQ_CMAP, vmin=0, vmax=1, aspect='auto')
ms.style_ax_heatmap(ax)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=ms.TICK_SIZE)
ms.save(fig, 'output.pdf')
```

### Grouped bar + value labels (model comparison)
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.SINGLE)
x, w = np.arange(N), 0.35
bars_a = ax.bar(x - w/2, vals_a, width=w, color=ms.YOLO_COLOR,    label='YOLO',    zorder=3)
bars_b = ax.bar(x + w/2, vals_b, width=w, color=ms.VITERBI_COLOR, label='Viterbi', zorder=3)
ms.bar_labels(ax, bars_a, fmt="{:.2f}", color='white')
ms.bar_labels(ax, bars_b, fmt="{:.2f}", color='white')
ms.style_ax(ax)
ms.save(fig, 'output.pdf')
```

### Stacked bar (state composition)
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.SINGLE_TALL)
bottom = np.zeros(len(ms.TREATMENT_ORDER))
for state in ms.STATE_ORDER:
    vals = np.array([composition[t][state] for t in ms.TREATMENT_ORDER])
    ax.bar(x_pos, vals, bottom=bottom, color=ms.STATE_COLORS[state],
           label=ms.STATE_SHORT[state], width=0.55, zorder=3)
    bottom += vals
ms.style_ax(ax)
ms.save(fig, 'output.pdf')
```

### Scatter / PHATE space
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.SINGLE)
for state in ms.STATE_ORDER:
    mask = df['state'] == state
    ax.scatter(df.loc[mask, 'x'], df.loc[mask, 'y'],
               c=ms.STATE_COLORS[state], label=ms.STATE_SHORT[state],
               s=8, alpha=0.65, linewidths=0, zorder=3)
ms.style_ax(ax)
ax.grid(axis='both', color=ms.GRID_COLOR, linewidth=0.5, alpha=0.5)
ms.save(fig, 'output.pdf')
```

### Diverging bar (fold-change / delta)
```python
ms.apply()
fig, ax = plt.subplots(figsize=ms.SINGLE_TALL)
colors = [ms.POS_COLOR if v >= 0 else ms.NEG_COLOR for v in log2fc]
ax.barh(features, log2fc, color=colors, height=0.55, zorder=3)
ax.axvline(0, color='#888888', linewidth=0.7, zorder=2)
ms.style_ax(ax)
ms.save(fig, 'output.pdf')
```

---

## Checklist before saving

- [ ] Asked user the 3 pre-generation questions
- [ ] `ms.apply()` or `ms.apply_journal()` called at top
- [ ] Figure width ≤ single or double column for target journal
- [ ] Colorblind-safe palette used
- [ ] `ms.style_ax()` on every axis
- [ ] Axis labels at `ms.LABEL_SIZE`, ticks at `ms.TICK_SIZE`
- [ ] Error bars defined in legend
- [ ] Individual data points shown (strip/dot) where N < 30
- [ ] Stat brackets use `ms.stat_annot()`, symbols defined in legend
- [ ] Panel labels correct case for target journal
- [ ] Saved as PDF (submission) + PNG (review)
