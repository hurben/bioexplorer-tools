import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Customizable Volcano Plot Viewer")

# --- Session state to persist example data usage ---
if "use_test" not in st.session_state:
    st.session_state.use_test = False

# --- Sidebar options ---
st.sidebar.header("Test Data Option")
if st.sidebar.button("Load Example Data"):
    st.session_state.use_test = True

if st.sidebar.button("Reset App"):
    st.session_state.use_test = False

st.sidebar.header("Thresholds & Display Settings")
x_thresh = st.sidebar.slider("Cohen's d threshold (absolute)", 0.0, 1.0, 0.2, step=0.01)
y_thresh = st.sidebar.slider("-log10(adj_pval) threshold", 0.0, 10.0, 1.3, step=0.1)

st.sidebar.header("Axis Ranges")
x_min = st.sidebar.number_input("X-axis min", value=-1.0)
x_max = st.sidebar.number_input("X-axis max", value=1.0)
y_min = st.sidebar.number_input("Y-axis min", value=0.0)
y_max = st.sidebar.number_input("Y-axis max", value=10.0)

st.sidebar.header("Highlight Colors")
red_color = st.sidebar.text_input("Positive color (hex)", "#FF0000")
blue_color = st.sidebar.text_input("Negative color (hex)", "#0000FF")
grey_color = st.sidebar.text_input("Non-significant color (hex)", "#B0B0B0")

# --- Load data ---
df = None

if st.session_state.use_test:
    test_path = "test_data/linear_regression.cVSneg.proteomics.tsv"
    try:
        df = pd.read_csv(test_path, sep="\t")
        st.success(f"Loaded test file: {test_path}")
    except Exception as e:
        st.error(f"Failed to load test file: {e}")
else:
    uploaded_file = st.file_uploader("Upload your data file (e.g., .txt or .tsv)", type=["txt", "csv", "tsv"])
    if uploaded_file:
        sep = '\t' if uploaded_file.name.endswith('.txt') or uploaded_file.name.endswith('.tsv') else ','
        df = pd.read_csv(uploaded_file, sep=sep)

# --- Process and visualize ---
if df is not None:
    if not {'feature', 'cohen_d', 'adj_pval'}.issubset(df.columns):
        st.error("File must contain columns: feature, cohen_d, adj_pval")
    else:
        df['neg_log10_adj_pval'] = -np.log10(df['adj_pval'])

        # Assign color group
        conditions = [
            (df['cohen_d'] > x_thresh) & (df['neg_log10_adj_pval'] > y_thresh),
            (df['cohen_d'] < -x_thresh) & (df['neg_log10_adj_pval'] > y_thresh)
        ]
        choices = ['positive', 'negative']
        df['color_group'] = np.select(conditions, choices, default='neutral')

        color_map = {
            'positive': red_color,
            'negative': blue_color,
            'neutral': grey_color
        }

        # Count annotations
        positive_n = df[df['color_group'] == 'positive'].shape[0]
        negative_n = df[df['color_group'] == 'negative'].shape[0]

        # Subset for download
        filtered_df = df[df['color_group'] != 'neutral']

        # Volcano plot
        fig = px.scatter(
            df,
            x='cohen_d',
            y='neg_log10_adj_pval',
            color='color_group',
            color_discrete_map=color_map,
            hover_name='feature',
            labels={'cohen_d': "Cohen's d", 'neg_log10_adj_pval': "-log10(adj_pval)"}
        )

        fig.update_traces(marker=dict(size=8, opacity=0.7))

        # Layout and styling
        fig.update_layout(
            title="Volcano Plot",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=14),
            xaxis=dict(
                range=[x_min, x_max],
                title="Cohen's d",
                title_font=dict(color='black'),
                tickfont=dict(color='black'),
                linecolor='black',
                showline=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                range=[y_min, y_max],
                title="-log10(adj_pval)",
                title_font=dict(color='black'),
                tickfont=dict(color='black'),
                linecolor='black',
                showline=True,
                gridcolor='lightgrey'
            ),
            legend=dict(
                title=dict(text='color_group', font=dict(color='black')),
                font=dict(color='black')
            )
        )

        # Add count annotations to plot corners
        fig.add_annotation(
            x=x_max, y=y_max,
            text=f"Positive: {positive_n}",
            showarrow=False,
            xanchor='right',
            yanchor='top',
            font=dict(color=red_color, size=14)
        )
        fig.add_annotation(
            x=x_min, y=y_max,
            text=f"Negative: {negative_n}",
            showarrow=False,
            xanchor='left',
            yanchor='top',
            font=dict(color=blue_color, size=14)
        )

        # Show plot
        st.plotly_chart(fig, use_container_width=True)

        # Download button
        st.markdown("### Download Filtered Data")
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download filtered features as CSV",
            data=csv,
            file_name='filtered_volcano_features.csv',
            mime='text/csv'
        )
