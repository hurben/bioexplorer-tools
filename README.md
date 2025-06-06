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