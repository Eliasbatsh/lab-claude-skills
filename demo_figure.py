"""
demo_figure.py — Demonstrates the ms_style skill with fake NETosis data.

Produces a 4-panel figure (A–D) covering the most common plot types:
  A. Bar + strip plot (treatment comparison, NETosis %)
  B. Time series (state occupancy over 4 h)
  C. Confusion matrix heatmap
  D. Two-model accuracy comparison

Run:
    python demo_figure.py
Output:
    demo_output/demo_figure.pdf
    demo_output/demo_figure.png
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
ms.apply()

# ── Fake data ─────────────────────────────────────────────────────────────────

# A: NETosis % per treatment (15 cells each)
treatments = []
values = []
means = {'Ctrl': 8, 'LPS': 22, 'Aux': 38, 'PMA': 72}
for t in ms.TREATMENT_ORDER:
    n = 15
    v = rng.normal(means[t], means[t] * 0.25, n).clip(0, 100)
    treatments.extend([t] * n)
    values.extend(v)
df_bar = pd.DataFrame({'treatment': treatments, 'NETosis (%)': values})

# B: State occupancy time series (0–240 min, 10 min bins)
time_min = np.arange(0, 241, 10)
normal    = 90  * np.exp(-time_min / 90)
decond_i  = 8   * np.exp(-((time_min - 60)**2) / 1800)
decond_r  = 15  * np.exp(-((time_min - 120)**2) / 2500)
netosis   = 100 - normal - decond_i - decond_r
netosis   = np.clip(netosis, 0, 100)
# add noise
normal   += rng.normal(0, 1.5, len(time_min))
decond_i += rng.normal(0, 0.8, len(time_min))
decond_r += rng.normal(0, 1.2, len(time_min))
netosis  += rng.normal(0, 1.5, len(time_min))

# C: Confusion matrix (4x4 normalised)
cm_raw = np.array([
    [92,  4,  2,  2],
    [ 5, 84,  8,  3],
    [ 1,  6, 87,  6],
    [ 2,  3,  5, 90],
], dtype=float)
cm_norm = cm_raw / cm_raw.sum(axis=1, keepdims=True)

# D: YOLO vs Viterbi accuracy per treatment
acc_yolo    = np.array([0.82, 0.78, 0.80, 0.85])
acc_viterbi = np.array([0.91, 0.89, 0.92, 0.94])

# ── Layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(7.0, 6.5))
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.52, wspace=0.40)
ax_A = fig.add_subplot(gs[0, 0])
ax_B = fig.add_subplot(gs[0, 1])
ax_C = fig.add_subplot(gs[1, 0])
ax_D = fig.add_subplot(gs[1, 1])

# ── Panel A — Bar + strip ─────────────────────────────────────────────────────
sns.barplot(data=df_bar, x='treatment', y='NETosis (%)',
            order=ms.TREATMENT_ORDER, hue='treatment', palette=ms.TREATMENT_COLORS,
            errorbar='sd', capsize=0.12, ax=ax_A, legend=False,
            err_kws={'linewidth': 0.8}, width=0.55)
sns.stripplot(data=df_bar, x='treatment', y='NETosis (%)',
              order=ms.TREATMENT_ORDER, color='#333333',
              alpha=0.55, size=2.5, jitter=True, ax=ax_A)
ms.style_ax(ax_A)
ax_A.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_A.set_ylabel('NETosis (%)', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_A.set_title('NETosis rate by treatment', fontsize=ms.TITLE_SIZE)

# stat bracket: Ctrl vs PMA
y_top = df_bar['NETosis (%)'].max()
ms.stat_annot(ax_A, x1=0, x2=3, y=y_top * 1.08, h=y_top * 0.04, p_val=0.0001)
ms.panel_label(ax_A, 'A')

# ── Panel B — Time series ─────────────────────────────────────────────────────
state_data = {
    'Normal':                    normal,
    'Decondensed-(NM_Intact)':   decond_i,
    'Decondensed-(NM_Ruptured)': decond_r,
    'NETosis':                   netosis,
}
for state in ms.STATE_ORDER:
    ax_B.plot(time_min, state_data[state],
              color=ms.STATE_COLORS[state],
              label=ms.STATE_SHORT[state],
              linewidth=1.2)
ms.style_ax(ax_B)
ax_B.set_xlabel('Time (min)', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_B.set_ylabel('% cells in state', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_B.set_title('State occupancy — PMA stimulation', fontsize=ms.TITLE_SIZE)
ax_B.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc',
            loc='center right', handlelength=1.5)
ms.panel_label(ax_B, 'B')

# ── Panel C — Confusion matrix ────────────────────────────────────────────────
state_labels = ['Normal', 'Decond.\n(Intact)', 'Decond.\n(Rupt.)', 'NETosis']
im = ax_C.imshow(cm_norm, cmap=ms.SEQ_CMAP, vmin=0, vmax=1, aspect='auto')
ax_C.set_xticks(range(4)); ax_C.set_xticklabels(state_labels, fontsize=ms.TICK_SIZE)
ax_C.set_yticks(range(4)); ax_C.set_yticklabels(state_labels, fontsize=ms.TICK_SIZE)
ax_C.set_xlabel('Predicted', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_C.set_ylabel('True', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_C.set_title('Viterbi confusion matrix', fontsize=ms.TITLE_SIZE)
for i in range(4):
    for j in range(4):
        ax_C.text(j, i, f'{cm_norm[i,j]:.2f}',
                  ha='center', va='center', fontsize=ms.ANNOT_SIZE,
                  color='white' if cm_norm[i,j] > 0.6 else '#333333')
cbar = fig.colorbar(im, ax=ax_C, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=ms.TICK_SIZE)
ms.style_ax_heatmap(ax_C)
ms.panel_label(ax_C, 'C')

# ── Panel D — Model accuracy comparison ───────────────────────────────────────
x    = np.arange(len(ms.TREATMENT_ORDER))
w    = 0.35
bars_y = ax_D.bar(x - w/2, acc_yolo,    width=w, color=ms.YOLO_COLOR,
                  label='YOLO', zorder=3)
bars_v = ax_D.bar(x + w/2, acc_viterbi, width=w, color=ms.VITERBI_COLOR,
                  label='Viterbi', zorder=3)
ax_D.set_xticks(x)
ax_D.set_xticklabels(ms.TREATMENT_ORDER, fontsize=ms.TICK_SIZE)
ax_D.set_ylim(0, 1.12)
ax_D.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_D.set_ylabel('Accuracy', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_D.set_title('YOLO vs Viterbi accuracy', fontsize=ms.TITLE_SIZE)
ax_D.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc')
ms.bar_labels(ax_D, bars_y,    fmt="{:.2f}", color='white')
ms.bar_labels(ax_D, bars_v,    fmt="{:.2f}", color='white')
ms.style_ax(ax_D)
ms.panel_label(ax_D, 'D')

# ── Save ──────────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), 'demo_output')
ms.save(fig, os.path.join(out_dir, 'demo_figure.pdf'))

# Re-create fig for PNG (save() closes it)
fig2 = plt.figure(figsize=(7.0, 6.5))
gs2  = gridspec.GridSpec(2, 2, figure=fig2, hspace=0.52, wspace=0.40)
ax_A2 = fig2.add_subplot(gs2[0, 0])
ax_B2 = fig2.add_subplot(gs2[0, 1])
ax_C2 = fig2.add_subplot(gs2[1, 0])
ax_D2 = fig2.add_subplot(gs2[1, 1])

# Panel A
sns.barplot(data=df_bar, x='treatment', y='NETosis (%)',
            order=ms.TREATMENT_ORDER, hue='treatment', palette=ms.TREATMENT_COLORS,
            errorbar='sd', capsize=0.12, ax=ax_A2, legend=False,
            err_kws={'linewidth': 0.8}, width=0.55)
sns.stripplot(data=df_bar, x='treatment', y='NETosis (%)',
              order=ms.TREATMENT_ORDER, color='#333333',
              alpha=0.55, size=2.5, jitter=True, ax=ax_A2)
ms.style_ax(ax_A2)
ax_A2.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_A2.set_ylabel('NETosis (%)', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_A2.set_title('NETosis rate by treatment', fontsize=ms.TITLE_SIZE)
y_top2 = df_bar['NETosis (%)'].max()
ms.stat_annot(ax_A2, 0, 3, y_top2*1.08, y_top2*0.04, 0.0001)
ms.panel_label(ax_A2, 'A')

# Panel B
for state in ms.STATE_ORDER:
    ax_B2.plot(time_min, state_data[state],
               color=ms.STATE_COLORS[state], label=ms.STATE_SHORT[state], linewidth=1.2)
ms.style_ax(ax_B2)
ax_B2.set_xlabel('Time (min)', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_B2.set_ylabel('% cells in state', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_B2.set_title('State occupancy — PMA stimulation', fontsize=ms.TITLE_SIZE)
ax_B2.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc',
             loc='center right', handlelength=1.5)
ms.panel_label(ax_B2, 'B')

# Panel C
im2 = ax_C2.imshow(cm_norm, cmap=ms.SEQ_CMAP, vmin=0, vmax=1, aspect='auto')
ax_C2.set_xticks(range(4)); ax_C2.set_xticklabels(state_labels, fontsize=ms.TICK_SIZE)
ax_C2.set_yticks(range(4)); ax_C2.set_yticklabels(state_labels, fontsize=ms.TICK_SIZE)
ax_C2.set_xlabel('Predicted', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_C2.set_ylabel('True', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_C2.set_title('Viterbi confusion matrix', fontsize=ms.TITLE_SIZE)
for i in range(4):
    for j in range(4):
        ax_C2.text(j, i, f'{cm_norm[i,j]:.2f}',
                   ha='center', va='center', fontsize=ms.ANNOT_SIZE,
                   color='white' if cm_norm[i,j] > 0.6 else '#333333')
cbar2 = fig2.colorbar(im2, ax=ax_C2, fraction=0.046, pad=0.04)
cbar2.ax.tick_params(labelsize=ms.TICK_SIZE)
ms.style_ax_heatmap(ax_C2)
ms.panel_label(ax_C2, 'C')

# Panel D
bars_y2 = ax_D2.bar(x - w/2, acc_yolo,    width=w, color=ms.YOLO_COLOR,    label='YOLO',    zorder=3)
bars_v2 = ax_D2.bar(x + w/2, acc_viterbi, width=w, color=ms.VITERBI_COLOR, label='Viterbi', zorder=3)
ax_D2.set_xticks(x); ax_D2.set_xticklabels(ms.TREATMENT_ORDER, fontsize=ms.TICK_SIZE)
ax_D2.set_ylim(0, 1.12)
ax_D2.set_xlabel('Treatment', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_D2.set_ylabel('Accuracy', fontsize=ms.LABEL_SIZE, labelpad=3)
ax_D2.set_title('YOLO vs Viterbi accuracy', fontsize=ms.TITLE_SIZE)
ax_D2.legend(fontsize=ms.LEGEND_SIZE, framealpha=0.9, edgecolor='#cccccc')
ms.bar_labels(ax_D2, bars_y2, fmt="{:.2f}", color='white')
ms.bar_labels(ax_D2, bars_v2, fmt="{:.2f}", color='white')
ms.style_ax(ax_D2)
ms.panel_label(ax_D2, 'D')

ms.save(fig2, os.path.join(out_dir, 'demo_figure.png'))
print("Done. Check demo_output/")
