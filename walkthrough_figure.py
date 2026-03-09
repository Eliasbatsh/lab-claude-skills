"""
walkthrough_figure.py — Walkthrough demo figure.

Settings chosen by user:
  Palette : Okabe-Ito (project default)
  Font    : Standard (labels 8 pt, ticks 7 pt)
  Journal : Nature / Nature Communications
              - panel labels lowercase (a, b, c)
              - single column = 3.5 in, double = 7.0 in
              - save as PDF (vector) + PNG (review)

NOTE: for final Nature submission, switch to ms.apply(font_size_offset=-2)
      to comply with their 5-7 pt text requirement.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ms_style as ms

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd

rng = np.random.default_rng(42)

# ── Apply: standard sizes, Okabe-Ito (default) ───────────────────────────────
ms.apply()
# For final Nature submission use:  ms.apply(font_size_offset=-2)

OUT_DIR = os.path.join(os.path.dirname(__file__), 'demo_output')

# ── Demo data ─────────────────────────────────────────────────────────────────
means_net = {'Ctrl': 8, 'LPS': 22, 'Aux': 38, 'PMA': 72}
records = []
for t in ms.TREATMENT_ORDER:
    v = rng.normal(means_net[t], means_net[t] * 0.25, 18).clip(0, 100)
    records.extend([{'treatment': t, 'NETosis (%)': x} for x in v])
df = pd.DataFrame(records)

time_min = np.arange(0, 241, 10)
normal   = np.clip(90  * np.exp(-time_min / 90)  + rng.normal(0, 1.5, len(time_min)), 0, 100)
dcnd_i   = np.clip(8   * np.exp(-((time_min - 60)**2)  / 1800) + rng.normal(0, 0.8, len(time_min)), 0, 20)
dcnd_r   = np.clip(15  * np.exp(-((time_min - 120)**2) / 2500) + rng.normal(0, 1.2, len(time_min)), 0, 30)
netosis  = np.clip(100 - normal - dcnd_i - dcnd_r + rng.normal(0, 1.5, len(time_min)), 0, 100)
state_ts = {
    'Normal':                    normal,
    'Decondensed-(NM_Intact)':   dcnd_i,
    'Decondensed-(NM_Ruptured)': dcnd_r,
    'NETosis':                   netosis,
}

# ── Figure: double-column, two panels ────────────────────────────────────────
# Nature double column = 7.0 in wide
fig = plt.figure(figsize=ms.DOUBLE_TALL)   # 7.0 × 4.5 in
gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.42)
ax_a = fig.add_subplot(gs[0])
ax_b = fig.add_subplot(gs[1])

# ── Panel a: Bar + strip + stat bracket (treatment comparison) ────────────────
sns.barplot(data=df, x='treatment', y='NETosis (%)',
            order=ms.TREATMENT_ORDER, hue='treatment', palette=ms.TREATMENT_COLORS,
            errorbar='sd', capsize=0.12, ax=ax_a, legend=False,
            err_kws={'linewidth': 0.8}, width=0.55)
sns.stripplot(data=df, x='treatment', y='NETosis (%)',
              order=ms.TREATMENT_ORDER, color='#333333',
              alpha=0.55, size=3, jitter=True, ax=ax_a)
ms.style_ax(ax_a)
ax_a.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_a.set_ylabel('NETosis (%)', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_a.set_title('NETosis rate by treatment', fontsize=ms.TITLE_SIZE)

y_top = df['NETosis (%)'].max()
ms.stat_annot(ax_a, x1=0, x2=3, y=y_top * 1.07, h=y_top * 0.04, p_val=0.0001)
ms.stat_annot(ax_a, x1=1, x2=3, y=y_top * 1.18, h=y_top * 0.04, p_val=0.003)

# Nature-style: lowercase panel label
ms.panel_label(ax_a, 'a')

# ── Panel b: Time series (state occupancy) ────────────────────────────────────
for state in ms.STATE_ORDER:
    ax_b.plot(time_min, state_ts[state],
              color=ms.STATE_COLORS[state],
              label=ms.STATE_SHORT[state],
              linewidth=1.2)
ms.style_ax(ax_b)
ax_b.set_xlabel('Time (min)', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_b.set_ylabel('% cells in state', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_b.set_title('State occupancy — PMA stimulation', fontsize=ms.TITLE_SIZE)
ax_b.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc',
            loc='center right', handlelength=1.5)

# Nature-style: lowercase panel label
ms.panel_label(ax_b, 'b')

# ── Save ──────────────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)
fig.savefig(os.path.join(OUT_DIR, 'walkthrough_figure.pdf'),
            dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUT_DIR, 'walkthrough_figure.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"Saved to {OUT_DIR}/walkthrough_figure.{{pdf,png}}")
print()
print("Nature submission checklist:")
print("  [x] Okabe-Ito colorblind-safe palette")
print("  [x] Arial font, pdf.fonttype=42 (TrueType embedded)")
print("  [x] L-frame spines, y-grid only")
print("  [x] Lowercase panel labels (a, b) — Nature convention")
print("  [x] Double-column width (7.0 in = 177 mm)")
print("  [x] PDF saved (vector, for submission)")
print("  [ ] For final submission: re-run with ms.apply(font_size_offset=-2)")
print("       to reduce labels to 6 pt / ticks to 5 pt (Nature max = 7 pt)")
