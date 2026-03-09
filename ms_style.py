"""
ms_style.py — Manuscript styling module for NETosis project figures.

Ground truth: Arial/Helvetica, Okabe-Ito colorblind-safe palette,
white background, L-frame (no top/right spines), 300 dpi vector-ready.

Research references:
  - Wong B (2011) Nature Methods 8:441  → Okabe-Ito palette
  - Nature Communications figure guidelines (nature.com)
  - Cell Press figure guidelines (cell.com)
  - JCI figure instructions (jci.org)
  - Paul Tol (2021) SRON Technical Note v3.2
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ── Figure sizes (width × height in inches) ──────────────────────────────────
# Nature/Cell: single column = 88–90 mm ≈ 3.46 in; double = 170–180 mm ≈ 7.09 in
SINGLE      = (3.5, 3.0)   # single-column small panel
SINGLE_TALL = (3.5, 4.0)   # single-column portrait
DOUBLE      = (7.0, 3.0)   # double-column wide
DOUBLE_TALL = (7.0, 4.5)   # double-column multi-row
DOUBLE_SQ   = (7.0, 7.0)   # confusion matrices / heatmaps

# ── Font sizes (defaults — override per journal via apply_journal()) ──────────
# Slightly above journal minimum (5-7 pt) for in-lab review; dial back at submission.
TITLE_SIZE  = 9    # panel title
LABEL_SIZE  = 8    # axis labels
TICK_SIZE   = 7    # tick labels
LEGEND_SIZE = 7    # legend text
ANNOT_SIZE  = 7    # in-figure annotations, stat brackets

# ── Spine / grid style ────────────────────────────────────────────────────────
SPINE_WIDTH = 1.2           # pt — thicker axes for visibility
SPINE_COLOR = '#888888'
GRID_COLOR  = '#e5e5e5'

# ─────────────────────────────────────────────────────────────────────────────
# COLOR PALETTES
# ─────────────────────────────────────────────────────────────────────────────

# ── Option 1: Okabe-Ito (Wong 2011, Nature Methods) ──────────────────────────
OKABE_ITO = {
    'orange':         '#E69F00',
    'sky_blue':       '#56B4E9',
    'bluish_green':   '#009E73',
    'yellow':         '#F0E442',
    'blue':           '#0072B2',
    'vermillion':     '#D55E00',
    'reddish_purple': '#CC79A7',
    'black':          '#000000',
}

# ── Option 2: Paul Tol Bright ─────────────────────────────────────────────────
TOL_BRIGHT = {
    'blue':   '#4477AA',
    'cyan':   '#66CCEE',
    'green':  '#228833',
    'yellow': '#CCBB44',
    'red':    '#EE6677',
    'purple': '#AA3377',
    'grey':   '#BBBBBB',
}

# ── Option 3: Paul Tol Muted ──────────────────────────────────────────────────
TOL_MUTED = {
    'rose':   '#CC6677',
    'indigo': '#332288',
    'sand':   '#DDCC77',
    'green':  '#117733',
    'cyan':   '#88CCEE',
    'wine':   '#882255',
    'teal':   '#44AA99',
    'olive':  '#999933',
    'purple': '#AA4499',
}

# ── Project palettes (Okabe-Ito defaults) ────────────────────────────────────
TREATMENT_ORDER  = ['Ctrl', 'LPS', 'Aux', 'PMA']
TREATMENT_COLORS = {
    'Ctrl': OKABE_ITO['blue'],
    'LPS':  OKABE_ITO['reddish_purple'],
    'Aux':  OKABE_ITO['orange'],
    'PMA':  OKABE_ITO['vermillion'],
}

STATE_ORDER = [
    'Normal',
    'Decondensed-(NM_Intact)',
    'Decondensed-(NM_Ruptured)',
    'NETosis',
]
STATE_COLORS = {
    'Normal':                    OKABE_ITO['blue'],
    'Decondensed-(NM_Intact)':   OKABE_ITO['sky_blue'],
    'Decondensed-(NM_Ruptured)': OKABE_ITO['orange'],
    'NETosis':                   OKABE_ITO['vermillion'],
}
STATE_SHORT = {
    'Normal':                    'Normal',
    'Decondensed-(NM_Intact)':   'Decond.\n(NM Intact)',
    'Decondensed-(NM_Ruptured)': 'Decond.\n(NM Rupt.)',
    'NETosis':                   'NETosis',
}

YOLO_COLOR    = OKABE_ITO['sky_blue']
VITERBI_COLOR = OKABE_ITO['blue']

SEQ_CMAP       = 'Blues'
DIVERGING_CMAP = 'RdBu_r'

POS_COLOR = '#2a7a2a'
NEG_COLOR = '#c0392b'

# ─────────────────────────────────────────────────────────────────────────────
# Journal presets
# Source: Nature Communications guidelines, Cell Press guidelines,
#         JCI figure instructions, Blood/ASH, PNAS, eLife, JCB, Wiley/JMicroscopy
# ─────────────────────────────────────────────────────────────────────────────
JOURNAL_PRESETS = {
    # ── Nature family ────────────────────────────────────────────────────────
    'nature': {
        'display_name':    'Nature / Nature Communications / Nature Immunology',
        'font':            'Arial',
        'min_pt':          5,
        'max_pt':          7,
        'panel_label_pt':  8,
        'panel_case':      'lower',   # a, b, c
        'panel_bold':      True,
        'col_single_mm':   88,
        'col_double_mm':   180,
        'col_single_in':   3.46,
        'col_double_in':   7.09,
        'dpi_line':        1200,      # bitmap fallback; prefer vector
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['PDF', 'EPS', 'AI', 'SVG', 'TIFF'],
        'min_linewidth_pt': 1.0,
        'notes':           'Panel labels 8 pt bold lowercase. All text 5-7 pt. Min line 1 pt. Prefer vector (PDF/EPS/AI/SVG).',
        'url':             'https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/',
    },
    # ── Cell Press ───────────────────────────────────────────────────────────
    'cell': {
        'display_name':    'Cell / Immunity / Cell Host & Microbe / Cell Reports',
        'font':            'Avenir',   # Arial acceptable fallback
        'min_pt':          6,
        'max_pt':          8,
        'panel_label_pt':  7,
        'panel_case':      'upper',   # A, B, C
        'panel_bold':      False,
        'col_single_mm':   85,
        'col_double_mm':   170,
        'col_single_in':   3.35,
        'col_double_in':   6.69,
        'dpi_line':        1000,
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['PDF', 'EPS', 'TIFF'],
        'min_linewidth_pt': 0.5,
        'notes':           'Panel labels uppercase, 6-8 pt. PDF preferred. Avenir font; use Arial if unavailable.',
        'url':             'https://www.cell.com/information-for-authors/figure-guidelines',
    },
    # ── JCI ──────────────────────────────────────────────────────────────────
    'jci': {
        'display_name':    'Journal of Clinical Investigation (JCI)',
        'font':            'Arial',
        'min_pt':          6,
        'max_pt':          12,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      False,     # Roman (non-bold) per JCI instructions
        'col_single_mm':   85,
        'col_double_mm':   170,
        'col_single_in':   3.35,
        'col_double_in':   6.69,
        'dpi_line':        600,
        'dpi_halftone':    600,
        'color_mode':      'RGB',
        'formats':         ['TIFF', 'PDF', 'EPS'],
        'min_linewidth_pt': 0.5,
        'notes':           'BAR-ONLY PLOTS PROHIBITED — must show individual data points (strip/dot/box). Panel labels uppercase Roman (non-bold). All figures 600 ppi TIFF.',
        'url':             'https://www.jci.org/kiosks/publish/figures',
    },
    # ── Blood ─────────────────────────────────────────────────────────────────
    'blood': {
        'display_name':    'Blood (ASH Publications)',
        'font':            'Arial',
        'min_pt':          9,
        'max_pt':          12,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      False,
        'col_single_mm':   88,
        'col_double_mm':   180,
        'col_single_in':   3.46,
        'col_double_in':   7.09,
        'dpi_line':        1000,
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['TIFF'],
        'min_linewidth_pt': 0.5,
        'notes':           'TIFF only. In-figure text 9-12 pt. RGB color mode.',
        'url':             'https://ashpublications.org/blood/pages/manuscript-prep',
    },
    # ── PNAS ─────────────────────────────────────────────────────────────────
    'pnas': {
        'display_name':    'PNAS (Proceedings of the National Academy of Sciences)',
        'font':            'Arial',
        'min_pt':          6,
        'max_pt':          8,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      False,
        'col_single_mm':   88,
        'col_double_mm':   180,
        'col_single_in':   3.46,
        'col_double_in':   7.09,
        'dpi_line':        1200,
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['TIFF', 'EPS', 'PDF'],
        'min_linewidth_pt': 0.5,
        'notes':           'Min font 6 pt. Panel labels uppercase. LZW compression for TIFF. Vector EPS/PDF preferred for line art.',
        'url':             'https://www.pnas.org/pb-assets/authors/digitalart-1675347574760.pdf',
    },
    # ── eLife ─────────────────────────────────────────────────────────────────
    'elife': {
        'display_name':    'eLife',
        'font':            'Arial',
        'min_pt':          7,
        'max_pt':          12,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      False,
        'col_single_mm':   88,
        'col_double_mm':   180,
        'col_single_in':   3.46,
        'col_double_in':   7.09,
        'dpi_line':        300,
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['JPG', 'PPT', 'PDF'],
        'min_linewidth_pt': 0.5,
        'notes':           'Strongly discourages bar-only graphs. Prefers showing all data points. JPG or PPT format.',
        'url':             'https://reviewer.elifesciences.org/author-guide/initial',
    },
    # ── Journal of Cell Biology ───────────────────────────────────────────────
    'jcb': {
        'display_name':    'Journal of Cell Biology (JCB)',
        'font':            'Arial',
        'min_pt':          5,
        'max_pt':          8,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      True,
        'col_single_mm':   85,
        'col_double_mm':   176,
        'col_single_in':   3.35,
        'col_double_in':   6.93,
        'dpi_line':        1200,
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['PDF', 'EPS', 'TIFF'],
        'min_linewidth_pt': 0.5,
        'notes':           'Min font 5 pt. Panel labels uppercase bold. Embed fonts in EPS.',
        'url':             'https://rupress.org/jcb/pages/general-information',
    },
    # ── Journal of Microscopy (Wiley) ─────────────────────────────────────────
    'j_microscopy': {
        'display_name':    'Journal of Microscopy (Wiley)',
        'font':            'Arial',
        'min_pt':          8,
        'max_pt':          12,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      False,
        'col_single_mm':   88,
        'col_double_mm':   178,
        'col_single_in':   3.46,
        'col_double_in':   7.01,
        'dpi_line':        1200,
        'dpi_halftone':    300,
        'color_mode':      'CMYK',   # CMYK preferred for print
        'formats':         ['EPS', 'TIFF'],
        'min_linewidth_pt': 0.5,
        'notes':           'CMYK preferred. Min font 8 pt in figures. EPS with embedded fonts. Min line 0.5 pt (0.2 mm). Must include scale bars on micrographs.',
        'url':             'https://onlinelibrary.wiley.com/page/journal/13652818/homepage/forauthors.html',
    },
    # ── Frontiers in Immunology ───────────────────────────────────────────────
    'frontiers': {
        'display_name':    'Frontiers in Immunology / Frontiers journals',
        'font':            'Arial',
        'min_pt':          8,
        'max_pt':          12,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      False,
        'col_single_mm':   90,
        'col_double_mm':   180,
        'col_single_in':   3.54,
        'col_double_in':   7.09,
        'dpi_line':        300,
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['TIFF', 'JPEG', 'PNG', 'EPS', 'PDF'],
        'min_linewidth_pt': 0.5,
        'notes':           'Min 300 DPI. Min font 8 pt. RGB. Does not restrict bar graphs.',
        'url':             'https://www.frontiersin.org/guidelines/author-guidelines',
    },
    # ── PLOS ONE / PLOS Biology ───────────────────────────────────────────────
    'plos': {
        'display_name':    'PLOS ONE / PLOS Biology',
        'font':            'Arial',
        'min_pt':          8,
        'max_pt':          12,
        'panel_label_pt':  8,
        'panel_case':      'upper',
        'panel_bold':      True,
        'col_single_mm':   90,
        'col_double_mm':   180,
        'col_single_in':   3.54,
        'col_double_in':   7.09,
        'dpi_line':        300,
        'dpi_halftone':    300,
        'color_mode':      'RGB',
        'formats':         ['TIFF', 'EPS', 'PDF'],
        'min_linewidth_pt': 0.5,
        'notes':           'Min 300 DPI. Panel labels uppercase bold. No minimum font restriction beyond legibility.',
        'url':             'https://journals.plos.org/plosone/s/figures',
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────────────────

def _find_font(preferred=None):
    """Find best available sans-serif. Searches: preferred → Arial → Helvetica → DejaVu Sans."""
    skip = {'signpainter', 'zapfino', 'brush script', 'comic', 'papyrus',
            'chalkboard', 'marker felt', 'snell', 'noteworthy', 'party let',
            'rounded', 'narrow', 'condensed', 'black', 'ultra'}
    candidates = ([preferred] if preferred else []) + ['Arial', 'Helvetica Neue', 'Helvetica', 'Inter', 'DejaVu Sans']
    for name in candidates:
        for fp in fm.findSystemFonts():
            try:
                prop = fm.FontProperties(fname=fp)
                font_name = prop.get_name()
                if any(s in font_name.lower() for s in skip):
                    continue
                if name.lower() in font_name.lower():
                    return font_name
            except Exception:
                continue
    return 'DejaVu Sans'


def apply(font_size_offset=0):
    """Set rcParams globally for manuscript-quality figures.

    Parameters
    ----------
    font_size_offset : int
        Shift all font sizes by this amount (e.g. -1 to match strict 5-7pt journals).
    """
    font_name = _find_font()
    o = font_size_offset
    plt.rcParams.update({
        'font.family':        'sans-serif',
        'font.sans-serif':    [font_name, 'Arial', 'Helvetica', 'DejaVu Sans'],
        'pdf.fonttype':       42,
        'ps.fonttype':        42,
        'font.size':          TICK_SIZE  + o,
        'axes.titlesize':     TITLE_SIZE + o,
        'axes.labelsize':     LABEL_SIZE + o,
        'xtick.labelsize':    TICK_SIZE  + o,
        'ytick.labelsize':    TICK_SIZE  + o,
        'legend.fontsize':    LEGEND_SIZE + o,
        'axes.linewidth':     SPINE_WIDTH,
        'axes.labelpad':      3,
        'axes.titlepad':      5,
        'axes.spines.top':    False,
        'axes.spines.right':  False,
        'xtick.major.size':   3.5,
        'ytick.major.size':   3.5,
        'xtick.major.width':  SPINE_WIDTH,
        'ytick.major.width':  SPINE_WIDTH,
        'xtick.major.pad':    2,
        'ytick.major.pad':    2,
        'xtick.direction':    'out',
        'ytick.direction':    'out',
        'figure.facecolor':   'white',
        'axes.facecolor':     'white',
        'axes.edgecolor':     SPINE_COLOR,
        'axes.grid':          True,
        'axes.grid.axis':     'y',
        'grid.alpha':         0.4,
        'grid.color':         GRID_COLOR,
        'grid.linewidth':     0.5,
        'figure.dpi':         150,
        'savefig.dpi':        300,
        'savefig.bbox':       'tight',
        'savefig.facecolor':  'white',
    })


def apply_journal(journal_key):
    """Configure rcParams and return preset dict for a specific journal.

    Parameters
    ----------
    journal_key : str
        One of: 'nature', 'cell', 'jci', 'blood', 'pnas', 'elife',
                'jcb', 'j_microscopy', 'frontiers', 'plos'

    Returns
    -------
    dict  — the full preset dict (font sizes, formats, notes, etc.)

    Example
    -------
    preset = ms.apply_journal('nature')
    # → also prints key requirements as a reminder
    """
    key = journal_key.lower().replace(' ', '_').replace('-', '_')
    if key not in JOURNAL_PRESETS:
        raise ValueError(f"Unknown journal '{journal_key}'. Available: {list(JOURNAL_PRESETS)}")
    p = JOURNAL_PRESETS[key]

    font_name = _find_font(p['font'])
    # Use the journal's max text size as the base; panel labels set separately
    body_pt = p['max_pt']
    tick_pt = max(p['min_pt'], body_pt - 1)

    plt.rcParams.update({
        'font.family':        'sans-serif',
        'font.sans-serif':    [font_name, 'Arial', 'Helvetica', 'DejaVu Sans'],
        'pdf.fonttype':       42,
        'ps.fonttype':        42,
        'font.size':          tick_pt,
        'axes.titlesize':     body_pt,
        'axes.labelsize':     body_pt,
        'xtick.labelsize':    tick_pt,
        'ytick.labelsize':    tick_pt,
        'legend.fontsize':    tick_pt,
        'axes.linewidth':     SPINE_WIDTH,
        'axes.labelpad':      3,
        'axes.titlepad':      5,
        'axes.spines.top':    False,
        'axes.spines.right':  False,
        'xtick.major.size':   3.5,
        'ytick.major.size':   3.5,
        'xtick.major.width':  SPINE_WIDTH,
        'ytick.major.width':  SPINE_WIDTH,
        'xtick.major.pad':    2,
        'ytick.major.pad':    2,
        'xtick.direction':    'out',
        'ytick.direction':    'out',
        'figure.facecolor':   'white',
        'axes.facecolor':     'white',
        'axes.edgecolor':     SPINE_COLOR,
        'axes.grid':          True,
        'axes.grid.axis':     'y',
        'grid.alpha':         0.4,
        'grid.color':         GRID_COLOR,
        'grid.linewidth':     0.5,
        'figure.dpi':         150,
        'savefig.dpi':        300,
        'savefig.bbox':       'tight',
        'savefig.facecolor':  'white',
    })

    print(f"\n── {p['display_name']} requirements ──────────────────────")
    print(f"  Font       : {p['font']}  ({p['min_pt']}–{p['max_pt']} pt body,  {p['panel_label_pt']} pt panel labels)")
    print(f"  Panel labels: {'uppercase' if p['panel_case']=='upper' else 'lowercase'}, {'bold' if p['panel_bold'] else 'not bold'}")
    print(f"  Column width: {p['col_single_mm']} mm single / {p['col_double_mm']} mm double")
    print(f"  DPI         : {p['dpi_line']} (line art) / {p['dpi_halftone']} (halftone)")
    print(f"  Color mode  : {p['color_mode']}")
    print(f"  Formats     : {', '.join(p['formats'])}")
    print(f"  Min linewidth: {p['min_linewidth_pt']} pt")
    print(f"  Notes       : {p['notes']}")
    print(f"  Guidelines  : {p['url']}\n")
    return p


def style_ax(ax):
    """Apply L-frame style: remove top/right spines, set grid and tick params."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(SPINE_COLOR)
    ax.spines['left'].set_linewidth(SPINE_WIDTH)
    ax.spines['bottom'].set_color(SPINE_COLOR)
    ax.spines['bottom'].set_linewidth(SPINE_WIDTH)
    ax.grid(axis='y', color=GRID_COLOR, linewidth=0.5, alpha=0.5, zorder=0)
    ax.tick_params(axis='both', which='both', labelsize=TICK_SIZE,
                   colors='#333333', length=3.5, width=SPINE_WIDTH)


def style_ax_heatmap(ax):
    """Style for heatmaps / confusion matrices: remove all spines and ticks."""
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)


def bar_labels(ax, bars, fmt="{:.2f}", color=None, offset=0.01):
    """Add value labels on top of bars. color=None → auto white/dark."""
    for bar in bars:
        h = bar.get_height()
        c = color
        if c is None:
            face = bar.get_facecolor()
            lum = 0.299 * face[0] + 0.587 * face[1] + 0.114 * face[2]
            c = 'white' if lum < 0.5 else '#333333'
        ax.text(bar.get_x() + bar.get_width() / 2, h + offset,
                fmt.format(h), ha='center', va='bottom',
                fontsize=ANNOT_SIZE, color=c, fontweight='bold')


def stat_annot(ax, x1, x2, y, h, p_val, color='#333333'):
    """Draw a significance bracket between two x-positions.

    Parameters
    ----------
    ax    : matplotlib Axes
    x1    : left bar x position (0-indexed)
    x2    : right bar x position
    y     : y level of bracket base
    h     : height of bracket ticks above y
    p_val : float — auto-converted to ns / * / ** / *** / ****
    color : bracket and label colour
    """
    if p_val > 0.05:   label = 'ns'
    elif p_val > 0.01: label = '*'
    elif p_val > 0.001: label = '**'
    elif p_val > 0.0001: label = '***'
    else:              label = '****'
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y],
            lw=0.7, color=color, clip_on=False)
    ax.text((x1 + x2) / 2, y + h, label,
            ha='center', va='bottom', fontsize=ANNOT_SIZE, color=color)


def panel_label(ax, letter, x=-0.12, y=1.08):
    """Add bold panel letter at top-left of axis.

    Convention: uppercase (A,B,C) for Cell/JCI/PNAS; lowercase (a,b,c) for Nature family.
    Pass letter.upper() or letter.lower() as appropriate.
    """
    ax.text(x, y, letter, transform=ax.transAxes,
            fontsize=LABEL_SIZE + 2, fontweight='bold', va='top', ha='left',
            color='#000000')


def save(fig, path, **kwargs):
    """Save figure at 300 dpi, tight bounding box, white background."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white', **kwargs)
    plt.close(fig)
    print(f"  Saved: {path}")


def get_palette(name='okabe_ito'):
    """Return a palette dict by name.

    Options: 'okabe_ito' (default), 'tol_bright', 'tol_muted'
    """
    palettes = {'okabe_ito': OKABE_ITO, 'tol_bright': TOL_BRIGHT, 'tol_muted': TOL_MUTED}
    key = name.lower().replace('-', '_').replace(' ', '_')
    if key not in palettes:
        raise ValueError(f"Unknown palette '{name}'. Choose from: {list(palettes)}")
    return palettes[key]
