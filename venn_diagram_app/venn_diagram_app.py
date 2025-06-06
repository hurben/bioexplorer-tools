# venn_diagram_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from itertools import combinations
import os
import io

st.set_page_config(layout="wide")
st.title("Venn Diagram App (Up to 3 Feature Sets)")

st.sidebar.header("1️⃣ Upload Your Files")

# Reset button
if st.sidebar.button("🔄 Reset All"):
    st.session_state.uploaded_files = []
    st.rerun()

# Initialize session state for uploaded files if not exists
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Manual file uploader
user_files = st.sidebar.file_uploader("Upload TSV files", accept_multiple_files=True, type="tsv")
if user_files:
    st.session_state.uploaded_files.extend(user_files)

# Test data paths
testdata1_path = "test_data/linear_regression.cVSneg.proteomics.tsv"
testdata2_path = "test_data/linear_regression.cVSpos.proteomics.tsv"

# Load test data buttons
if st.sidebar.button("📂 Load testdata1 (cVSneg)"):
    with open(testdata1_path, "rb") as f:
        bio = io.BytesIO(f.read())
        bio.name = "testdata1.tsv"
        bio.seek(0)
        st.session_state.uploaded_files.append(bio)

if st.sidebar.button("📂 Load testdata2 (cVSpos)"):
    with open(testdata2_path, "rb") as f:
        bio = io.BytesIO(f.read())
        bio.name = "testdata2.tsv"
        bio.seek(0)
        st.session_state.uploaded_files.append(bio)

if len(st.session_state.uploaded_files) < 1:
    st.warning("Please upload at least 1 TSV file to proceed.")
    st.stop()

# Load data
dataframes = {}
for i, uploaded in enumerate(st.session_state.uploaded_files):
    name = f"input_{i+1}"
    if hasattr(uploaded, 'seek'):
        uploaded.seek(0)
    try:
        df = pd.read_csv(uploaded, sep='\t')
        dataframes[name] = df
    except pd.errors.EmptyDataError:
        st.error(f"⚠️ File {name} is empty or could not be parsed.")

st.sidebar.header("Define Feature Lists (Max 3)")

feature_lists = []
list_labels = []

for i in range(3):
    with st.sidebar.expander(f"Define Feature List {i+1}"):
        enable = st.checkbox(f"Enable Feature List {i+1}", value=(i < 2))
        if not enable:
            continue

        input_file = st.selectbox(f"Select Input File", options=list(dataframes.keys()), key=f"input_file_{i}")
        df = dataframes[input_file]

        feature_col = st.text_input("Feature Column", value="feature", key=f"feature_col_{i}")
        if feature_col not in df.columns:
            st.warning(f"'{feature_col}' not in columns of {input_file}")
            continue

        st.markdown("Example: `adj_pval < 0.05 and cohen_d > 0.5`")
        condition = st.text_input("Filter Condition", key=f"condition_{i}")

        try:
            filtered_df = df.query(condition)
            features = filtered_df[feature_col].dropna().astype(str).tolist()
            st.success(f"Filtered {len(features)} features")
            feature_lists.append(set(features))
            list_labels.append(f"{input_file}_list{i+1}")
        except Exception as e:
            st.error(f"Error in condition: {e}")

if len(feature_lists) < 2:
    st.warning("Define at least 2 valid feature lists to visualize Venn diagram.")
    st.stop()

st.header("📊 Venn Diagram")
fig, ax = plt.subplots()

if len(feature_lists) == 2:
    venn2(feature_lists, set_labels=list_labels)
elif len(feature_lists) == 3:
    venn3(feature_lists, set_labels=list_labels)
else:
    st.error("Only 2 to 3 feature lists are supported.")
    st.stop()

st.pyplot(fig)

# Table of set combinations
st.header("📋 Set Combinations Table")
all_features = sorted(set().union(*feature_lists))
output_table = pd.DataFrame(index=all_features)

for i, fset in enumerate(feature_lists):
    output_table[list_labels[i]] = output_table.index.isin(fset).astype(int)

st.dataframe(output_table)
st.download_button("Download Combination Table as CSV", output_table.to_csv().encode(), "venn_combinations.csv")
