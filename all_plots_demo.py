"""
all_plots_demo.py — Full showcase of every ms_style setting.

9-panel, 3×3 figure (14 × 10.5 in):
  A. Bar + strip + stat bracket   (TREATMENT_COLORS)
  B. Time series                  (STATE_COLORS)
  C. Confusion matrix heatmap     (SEQ_CMAP)
  D. Grouped bar + bar_labels     (YOLO_COLOR / VITERBI_COLOR)
  E. Box + strip                  (STATE_COLORS) ← NEW
  F. Violin + strip               (STATE_COLORS)
  G. Stacked bar composition      (STATE_COLORS)
  H. Scatter / feature space      (STATE_COLORS)
  I. Fold-change diverging bar    (POS_COLOR / NEG_COLOR)

Run:
    conda run -n netsproject python all_plots_demo.py
Output:
    demo_output/all_plots.pdf
    demo_output/all_plots.png
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ms_style as ms

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd

rng = np.random.default_rng(42)
ms.apply()

OUT_DIR = os.path.join(os.path.dirname(__file__), 'demo_output')

# ─────────────────────────────────────────────────────────────────────────────
# Shared fake data
# ─────────────────────────────────────────────────────────────────────────────

# Treatment bar data (A, D, F)
means_net = {'Ctrl': 8, 'LPS': 22, 'Aux': 38, 'PMA': 72}
records = []
for t in ms.TREATMENT_ORDER:
    v = rng.normal(means_net[t], means_net[t] * 0.25, 18).clip(0, 100)
    records.extend([{'treatment': t, 'NETosis (%)': x} for x in v])
df_bar = pd.DataFrame(records)

# Time series data (B)
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

# Confusion matrix (C)
cm_raw  = np.array([[92,4,2,2],[5,84,8,3],[1,6,87,6],[2,3,5,90]], dtype=float)
cm_norm = cm_raw / cm_raw.sum(axis=1, keepdims=True)
state_labels_short = ['Normal', 'Decond.\n(Intact)', 'Decond.\n(Rupt.)', 'NETosis']

# Model accuracy (D)
acc_yolo    = np.array([0.82, 0.78, 0.80, 0.85])
acc_viterbi = np.array([0.91, 0.89, 0.92, 0.94])
x_model = np.arange(4)
w = 0.35

# Violin / strip data (E) — DNA intensity per state
intensity_records = []
state_intensity_means = {
    'Normal': 200, 'Decondensed-(NM_Intact)': 145,
    'Decondensed-(NM_Ruptured)': 95, 'NETosis': 60,
}
for st in ms.STATE_ORDER:
    vals = rng.normal(state_intensity_means[st], 25, 40).clip(10, 300)
    intensity_records.extend([{'State': ms.STATE_SHORT[st], 'DNA intensity (AU)': v,
                                '_state': st} for v in vals])
df_violin = pd.DataFrame(intensity_records)
state_short_order = [ms.STATE_SHORT[s] for s in ms.STATE_ORDER]

# Stacked bar composition (F) — state % at t=120 min per treatment
composition = {
    'Ctrl': [72, 12, 8, 8],
    'LPS':  [50, 18, 18, 14],
    'Aux':  [32, 15, 25, 28],
    'PMA':  [10, 8, 18, 64],
}

# Scatter feature space (G) — fake 2D embedding coloured by state
scatter_records = []
state_centers = {
    'Normal':                    (1.5, 1.2),
    'Decondensed-(NM_Intact)':   (-0.5, 2.0),
    'Decondensed-(NM_Ruptured)': (-1.8, 0.2),
    'NETosis':                   (-0.8, -1.8),
}
for st in ms.STATE_ORDER:
    cx, cy = state_centers[st]
    n = 60
    xs = rng.normal(cx, 0.55, n)
    ys = rng.normal(cy, 0.55, n)
    scatter_records.extend([{'x': xi, 'y': yi, 'State': ms.STATE_SHORT[st],
                              '_state': st} for xi, yi in zip(xs, ys)])
df_scatter = pd.DataFrame(scatter_records)

# Fold-change diverging bars (H) — fake feature log2FC (PMA vs Ctrl)
features = ['Feat 1', 'Feat 2', 'Feat 3', 'Feat 4',
            'Feat 5', 'Feat 6', 'Feat 7', 'Feat 8']
log2fc   = np.array([2.1, 1.4, -0.8, -1.9, 0.6, 3.2, -2.4, 0.3])
p_vals   = np.array([0.0001, 0.003, 0.04, 0.0001, 0.12, 0.0001, 0.001, 0.31])


# ─────────────────────────────────────────────────────────────────────────────
# Draw function — builds all panels into the provided axes list
# ─────────────────────────────────────────────────────────────────────────────
def draw_all(fig, axes):
    ax_A, ax_B, ax_C, ax_D, ax_E, ax_F, ax_G, ax_H, ax_I = axes

    # ── A: Bar + strip + stat bracket ─────────────────────────────────────────
    sns.barplot(data=df_bar, x='treatment', y='NETosis (%)',
                order=ms.TREATMENT_ORDER, hue='treatment', palette=ms.TREATMENT_COLORS,
                errorbar='sd', capsize=0.12, ax=ax_A, legend=False,
                err_kws={'linewidth': 0.8}, width=0.55)
    sns.stripplot(data=df_bar, x='treatment', y='NETosis (%)',
                  order=ms.TREATMENT_ORDER, color='#333333',
                  alpha=0.5, size=2.5, jitter=True, ax=ax_A)
    ms.style_ax(ax_A)
    ax_A.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_A.set_ylabel('NETosis (%)', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_A.set_title('NETosis rate by treatment', fontsize=ms.TITLE_SIZE)
    y_top = df_bar['NETosis (%)'].max()
    ms.stat_annot(ax_A, 0, 3, y_top * 1.08, y_top * 0.04, 0.0001)
    ms.stat_annot(ax_A, 1, 3, y_top * 1.20, y_top * 0.04, 0.002)
    ms.panel_label(ax_A, 'A')

    # ── B: Time series ─────────────────────────────────────────────────────────
    for state in ms.STATE_ORDER:
        ax_B.plot(time_min, state_ts[state],
                  color=ms.STATE_COLORS[state], label=ms.STATE_SHORT[state],
                  linewidth=1.2)
    ms.style_ax(ax_B)
    ax_B.set_xlabel('Time (min)', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_B.set_ylabel('% cells in state', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_B.set_title('State occupancy — PMA stimulation', fontsize=ms.TITLE_SIZE)
    ax_B.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc',
                loc='center right', handlelength=1.5)
    ms.panel_label(ax_B, 'B')

    # ── C: Confusion matrix ────────────────────────────────────────────────────
    im = ax_C.imshow(cm_norm, cmap=ms.SEQ_CMAP, vmin=0, vmax=1, aspect='auto')
    ax_C.set_xticks(range(4)); ax_C.set_xticklabels(state_labels_short, fontsize=ms.TICK_SIZE)
    ax_C.set_yticks(range(4)); ax_C.set_yticklabels(state_labels_short, fontsize=ms.TICK_SIZE)
    ax_C.set_xlabel('Predicted', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_C.set_ylabel('True', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_C.set_title('Viterbi confusion matrix', fontsize=ms.TITLE_SIZE)
    for i in range(4):
        for j in range(4):
            ax_C.text(j, i, f'{cm_norm[i,j]:.2f}', ha='center', va='center',
                      fontsize=ms.ANNOT_SIZE,
                      color='white' if cm_norm[i,j] > 0.6 else '#333333')
    cbar = fig.colorbar(im, ax=ax_C, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=ms.TICK_SIZE)
    ms.style_ax_heatmap(ax_C)
    ms.panel_label(ax_C, 'C')

    # ── D: Grouped bar + bar_labels ────────────────────────────────────────────
    bars_y = ax_D.bar(x_model - w/2, acc_yolo,    width=w, color=ms.YOLO_COLOR,
                      label='YOLO', zorder=3)
    bars_v = ax_D.bar(x_model + w/2, acc_viterbi, width=w, color=ms.VITERBI_COLOR,
                      label='Viterbi', zorder=3)
    ax_D.set_xticks(x_model); ax_D.set_xticklabels(ms.TREATMENT_ORDER, fontsize=ms.TICK_SIZE)
    ax_D.set_ylim(0, 1.12)
    ax_D.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_D.set_ylabel('Accuracy', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_D.set_title('YOLO vs Viterbi accuracy', fontsize=ms.TITLE_SIZE)
    ax_D.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc')
    ms.bar_labels(ax_D, bars_y, fmt="{:.2f}", color='white')
    ms.bar_labels(ax_D, bars_v, fmt="{:.2f}", color='white')
    ms.style_ax(ax_D)
    ms.panel_label(ax_D, 'D')

    # ── E: Box + strip ─────────────────────────────────────────────────────────
    pal_state = {ms.STATE_SHORT[s]: ms.STATE_COLORS[s] for s in ms.STATE_ORDER}
    sns.boxplot(data=df_violin, x='State', y='DNA intensity (AU)',
                order=state_short_order, hue='State', palette=pal_state,
                width=0.5, linewidth=0.8, fliersize=0, ax=ax_E, legend=False)
    sns.stripplot(data=df_violin, x='State', y='DNA intensity (AU)',
                  order=state_short_order, color='#333333',
                  alpha=0.55, size=2.5, jitter=True, ax=ax_E)
    ms.style_ax(ax_E)
    ax_E.set_xlabel('Cell state', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_E.set_ylabel('DNA intensity (AU)', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_E.set_title('Box plot — DNA intensity by state', fontsize=ms.TITLE_SIZE)
    ax_E.tick_params(axis='x', labelsize=ms.TICK_SIZE - 1)
    ms.panel_label(ax_E, 'E')

    # ── F: Violin + strip ──────────────────────────────────────────────────────
    sns.violinplot(data=df_violin, x='State', y='DNA intensity (AU)',
                   order=state_short_order, hue='State', palette=pal_state,
                   inner=None, linewidth=0.6, ax=ax_F, legend=False, alpha=0.55)
    sns.stripplot(data=df_violin, x='State', y='DNA intensity (AU)',
                  order=state_short_order, hue='State', palette=pal_state,
                  size=2, alpha=0.7, jitter=True, ax=ax_F, legend=False)
    ms.style_ax(ax_F)
    ax_F.set_xlabel('Cell state', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_F.set_ylabel('DNA intensity (AU)', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_F.set_title('Violin plot — DNA intensity by state', fontsize=ms.TITLE_SIZE)
    ax_F.tick_params(axis='x', labelsize=ms.TICK_SIZE - 1)
    ms.panel_label(ax_F, 'F')

    # ── G: Stacked bar composition ─────────────────────────────────────────────
    bottom = np.zeros(4)
    x_pos = np.arange(4)
    for k, state in enumerate(ms.STATE_ORDER):
        vals = np.array([composition[t][k] for t in ms.TREATMENT_ORDER])
        ax_G.bar(x_pos, vals, bottom=bottom, color=ms.STATE_COLORS[state],
                 label=ms.STATE_SHORT[state], width=0.55, zorder=3)
        bottom += vals
    ax_G.set_xticks(x_pos); ax_G.set_xticklabels(ms.TREATMENT_ORDER, fontsize=ms.TICK_SIZE)
    ax_G.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_G.set_ylabel('% cells', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_G.set_ylim(0, 110)
    ax_G.set_title('State composition at t = 120 min', fontsize=ms.TITLE_SIZE)
    ax_G.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc',
                loc='upper right', handlelength=1.2)
    ms.style_ax(ax_G)
    ms.panel_label(ax_G, 'G')

    # ── H: Scatter / feature space ─────────────────────────────────────────────
    for state in ms.STATE_ORDER:
        sub = df_scatter[df_scatter['_state'] == state]
        ax_H.scatter(sub['x'], sub['y'], c=ms.STATE_COLORS[state],
                     label=ms.STATE_SHORT[state], s=8, alpha=0.65,
                     linewidths=0, zorder=3)
    ms.style_ax(ax_H)
    ax_H.set_xlabel('PHATE 1', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_H.set_ylabel('PHATE 2', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_H.set_title('Feature space (PHATE), coloured by state', fontsize=ms.TITLE_SIZE)
    ax_H.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc',
                markerscale=1.8, handlelength=0.8)
    ax_H.grid(axis='both', color=ms.GRID_COLOR, linewidth=0.5, alpha=0.5)
    ms.panel_label(ax_H, 'H')

    # ── I: Fold-change diverging bar ───────────────────────────────────────────
    colors_fc = [ms.POS_COLOR if v >= 0 else ms.NEG_COLOR for v in log2fc]
    ax_I.barh(features, log2fc, color=colors_fc, height=0.55, zorder=3)
    ax_I.axvline(0, color='#888888', linewidth=0.7, zorder=2)
    for i, (v, p) in enumerate(zip(log2fc, p_vals)):
        if p <= 0.05:
            sym  = '****' if p <= 0.0001 else ('***' if p <= 0.001 else ('**' if p <= 0.01 else '*'))
            xpos = v + (0.15 if v >= 0 else -0.15)
            ha   = 'left' if v >= 0 else 'right'
            ax_I.text(xpos, i, sym, va='center', ha=ha,
                      fontsize=ms.ANNOT_SIZE, color='#333333')
    ax_I.set_xlabel(r'log$_2$ fold change (PMA vs Ctrl)', fontsize=ms.LABEL_SIZE, labelpad=3)
    ax_I.set_title('Differential features — PMA vs Ctrl', fontsize=ms.TITLE_SIZE)
    # manual spine style (horizontal bar needs both axes styled)
    ax_I.spines['top'].set_visible(False)
    ax_I.spines['right'].set_visible(False)
    for sp in ['left', 'bottom']:
        ax_I.spines[sp].set_color(ms.SPINE_COLOR)
        ax_I.spines[sp].set_linewidth(ms.SPINE_WIDTH)
    ax_I.tick_params(labelsize=ms.TICK_SIZE, colors='#333333',
                     length=3.5, width=ms.SPINE_WIDTH)
    ax_I.grid(axis='x', color=ms.GRID_COLOR, linewidth=0.5, alpha=0.5, zorder=0)
    pos_patch = mpatches.Patch(color=ms.POS_COLOR, label='Upregulated')
    neg_patch = mpatches.Patch(color=ms.NEG_COLOR, label='Downregulated')
    ax_I.legend(handles=[pos_patch, neg_patch], fontsize=ms.LEGEND_SIZE,
                framealpha=0.9, edgecolor='#cccccc', loc='lower right')
    ms.panel_label(ax_I, 'I')


# ─────────────────────────────────────────────────────────────────────────────
# Build figure — 3×3 layout, save both PDF and PNG
# ─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14.0, 10.5))
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.60, wspace=0.45)
axes = [
    fig.add_subplot(gs[0, 0]),  # A
    fig.add_subplot(gs[0, 1]),  # B
    fig.add_subplot(gs[0, 2]),  # C
    fig.add_subplot(gs[1, 0]),  # D
    fig.add_subplot(gs[1, 1]),  # E  (box + strip — NEW)
    fig.add_subplot(gs[1, 2]),  # F  (violin + strip)
    fig.add_subplot(gs[2, 0]),  # G
    fig.add_subplot(gs[2, 1]),  # H
    fig.add_subplot(gs[2, 2]),  # I
]

draw_all(fig, axes)

os.makedirs(OUT_DIR, exist_ok=True)
fig.savefig(os.path.join(OUT_DIR, 'all_plots.png'), dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUT_DIR, 'all_plots.pdf'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"Done. Outputs in {OUT_DIR}/")
