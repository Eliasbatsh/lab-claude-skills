"""
walkthrough_box.py — Box + strip walkthrough figure.

User choices:
  Graph type : Box + strip
  Data       : Demo / fake data
  Palette    : Okabe-Ito
  Text size  : Presentation (labels 10 pt, ticks 9 pt)
  Journal    : Cell Press (Cell, Immunity, etc.)
                 - uppercase panel labels (A, B, C)
                 - single col = 85 mm ≈ 3.35 in
                 - PDF preferred (also save PNG for review)
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ms_style as ms

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

rng = np.random.default_rng(42)

# ── Apply: presentation sizing, Okabe-Ito default ────────────────────────────
ms.apply(font_size_offset=+2)   # labels → 10 pt, ticks → 9 pt

OUT_DIR = os.path.join(os.path.dirname(__file__), 'demo_output')

# ── Demo data — NETosis % per treatment ──────────────────────────────────────
means_net = {'Ctrl': 8, 'LPS': 22, 'Aux': 38, 'PMA': 72}
records = []
for t in ms.TREATMENT_ORDER:
    v = rng.normal(means_net[t], means_net[t] * 0.25, 20).clip(0, 100)
    records.extend([{'Treatment': t, 'NETosis (%)': x} for x in v])
df = pd.DataFrame(records)

# ── Figure: single column (Cell Press 85 mm ≈ 3.35 in) ──────────────────────
fig, ax = plt.subplots(figsize=(3.35, 4.0))

# Box + strip — Okabe-Ito colors, no outlier markers (fliersize=0),
# individual points shown via strip instead
sns.boxplot(data=df, x='Treatment', y='NETosis (%)',
            order=ms.TREATMENT_ORDER, hue='Treatment',
            palette=ms.TREATMENT_COLORS,
            width=0.5, linewidth=0.8, fliersize=0,
            ax=ax, legend=False)

sns.stripplot(data=df, x='Treatment', y='NETosis (%)',
              order=ms.TREATMENT_ORDER, color='#333333',
              alpha=0.55, size=3.5, jitter=True, ax=ax)

ms.style_ax(ax)

ax.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE + 2, labelpad=3)
ax.set_ylabel('NETosis (%)', fontsize=ms.LABEL_SIZE + 2, labelpad=3)
ax.set_title('NETosis rate by treatment', fontsize=ms.TITLE_SIZE + 2)

# Stat brackets
y_top = df['NETosis (%)'].max()
ms.stat_annot(ax, x1=0, x2=3, y=y_top * 1.07, h=y_top * 0.04, p_val=0.0001)
ms.stat_annot(ax, x1=1, x2=3, y=y_top * 1.18, h=y_top * 0.04, p_val=0.003)

# Cell Press: uppercase panel label
ms.panel_label(ax, 'A')

# ── Save ──────────────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)
fig.savefig(os.path.join(OUT_DIR, 'walkthrough_box.pdf'),
            dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUT_DIR, 'walkthrough_box.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

print(f"Saved to {OUT_DIR}/walkthrough_box.{{pdf,png}}")
print()
print("Cell Press submission checklist:")
print("  [x] Okabe-Ito colorblind-safe palette")
print("  [x] Arial font, pdf.fonttype=42 (TrueType embedded)")
print("  [x] L-frame spines, y-grid only, spine width 1.2 pt")
print("  [x] Uppercase panel label (A) — Cell Press convention")
print("  [x] Single-column width (3.35 in = 85 mm)")
print("  [x] Individual data points shown (strip) — no bar-only plot")
print("  [x] PDF saved (Cell Press preferred format)")
print("  [ ] For final submission: switch to ms.apply(font_size_offset=0)")
print("       Cell Press max text size ~7-8 pt; presentation sizing is for review only")
