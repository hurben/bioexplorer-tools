# 🧪 bioexplorer-tools

This repository contains a collection of lightweight, interactive tools for data exploration and visualization, built primarily using [Streamlit](https://streamlit.io/). These tools are designed to be modular, extensible, and easy to launch for quick testing and prototyping.

---

## 🚀 Available Apps

### 🔬 1. `volcano_plot_app/` – Volcano Plot Viewer

A highly customizable volcano plot visualizer.

**Features:**
- Upload your own data or load an example dataset
- Adjust thresholds for `Cohen's d` and `-log10(adj_pval)`
- Set axis ranges and colors using HEX codes
- Highlight positive/negative features in real time
- View dynamic annotation counts and export filtered features as CSV

**Run the app:**

```bash
cd volcano_plot_app
streamlit run volcano_plot_with_sliders.py
```

## 🔧 Repository Structure

- volcano_plot_app

```bash
bioexplorer-tools/
├── volcano_plot_app/                     # Streamlit app: interactive volcano plot viewer
│   ├── test_data/                        # Example input data
│   │   └── linear_regression.cVSneg.proteomics.tsv
│   ├── volcano_plot_with_sliders.py     # Main Streamlit app script
│   └── requirements.txt                 # Dependencies for this app (pip-based)
├── filtered_volcano_features.csv         # Example output file (downloaded via app)
├── linear_regression.cVSneg.proteomics.tsv # Example input (copied to root for convenience)
└── README.md                             # Project documentation
```

### 🧬 2. `venn_diagram_app/` – Venn Diagram Builder

An interactive Venn diagram app that allows you to define up to 3 feature sets using custom filters across one or more uploaded TSV files.

**Features:**
- Upload 1 or more tab-separated (TSV) files
- Define up to 3 feature lists using user-defined filters (e.g., `adj_pval < 0.05 and cohen_d > 0.5`)
- Use any column as the feature identifier
- Visualize overlaps using 2-set or 3-set Venn diagrams
- View and export a full set combination table showing feature membership across lists
- Load example datasets (`testdata1` / `testdata2`) or reset all uploads with one click

**Run the app:**

```bash
cd venn_diagram_app
streamlit run venn_diagram_app.py
```

```bash
bioexplorer-tools/
├── venn_diagram_app/                       # Venn diagram builder
│   ├── test_data/                         # Example inputs
│   │   ├── linear_regression.cVSneg.proteomics.tsv
│   │   └── linear_regression.cVSpos.proteomics.tsv
└── └── venn_diagram_app.py                 # Main Streamlit app script
```

---

### 📝 3. `markdown_reditor/` – Markdown Reditor

A single-file, browser-based Markdown editor and reader. No installation or server required — open `markdown_reditor.html` directly in any modern browser.

**Features:**
- Open `.md` files via file picker or drag-and-drop; save back to disk
- Live split-pane view: raw Markdown editor (left) and rendered preview (right)
- Draggable resizer between editor and preview panes
- Collapsible Table of Contents sidebar auto-built from headings
- **Highlighter pen tool** — click a color in the toolbar and drag over any text in the preview to highlight it (supports cross-paragraph selections); highlights are saved to `localStorage`
- Annotations panel listing all highlights with click-to-scroll and per-item delete
- Three themes: Light, Sepia, Dark — cycles with one button, persisted across sessions
- Tab-key support and live cursor position (`Ln / Col`) display in the editor
- No build step, no dependencies beyond [marked.js](https://marked.dev/) via CDN

**Usage:**

No server needed. Just open the file:

```bash
open markdown_reditor/markdown_reditor.html   # macOS
# or double-click the file in Finder
```

**Keyboard shortcuts:**

| Shortcut | Action |
|---|---|
| `⌘ O` | Open file |
| `⌘ S` | Save / download file |
| `⌘ E` | Toggle editor pane |
| `⌘ K` | Toggle Table of Contents |
| `Esc` | Deactivate highlighter pen |

```bash
bioexplorer-tools/
├── markdown_reditor/
│   └── markdown_reditor.html             # Self-contained single-file app (HTML + CSS + JS)
```