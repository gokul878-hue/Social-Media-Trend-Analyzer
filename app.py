"""Streamlit dashboard for the Social Media Trend Analyzer project."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
RESULTS_FILE = BASE_DIR / "results" / "trend_summary.csv"
GITHUB_URL = "https://github.com/gokul878-hue/Social-Media-Trend-Analyzer"

st.set_page_config(
    page_title="Social Media Trend Analyzer",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px;}
    .hero {
        padding: 2.3rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #172554 0%, #312e81 55%, #581c87 100%);
        border: 1px solid rgba(255,255,255,.12);
        margin-bottom: 1.4rem;
    }
    .hero h1 {margin: 0; color: #ffffff; font-size: 2.35rem;}
    .hero p {margin: .65rem 0 0; color: #dbeafe; font-size: 1.05rem;}
    .pipeline-step {
        min-height: 112px;
        padding: 1rem;
        border-radius: 14px;
        background: #172033;
        border: 1px solid #334155;
    }
    .pipeline-step strong {color: #93c5fd;}
    .small-note {color: #94a3b8; font-size: .9rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_results() -> pd.DataFrame:
    """Load the version-controlled summary produced by Hadoop."""
    frame = pd.read_csv(RESULTS_FILE)
    required = {"type", "rank", "term", "frequency"}
    if not required.issubset(frame.columns):
        raise ValueError("The results file does not have the expected columns.")
    frame["frequency"] = pd.to_numeric(frame["frequency"], errors="raise")
    return frame


def trend_chart(frame: pd.DataFrame, title: str, color: str):
    """Create a readable horizontal bar chart for Streamlit."""
    plot_data = frame.sort_values("frequency", ascending=True)
    figure, axis = plt.subplots(figsize=(9.5, 5.4))
    bars = axis.barh(plot_data["term"], plot_data["frequency"], color=color)
    axis.set_title(title, fontsize=16, fontweight="bold", pad=14)
    axis.set_xlabel("Frequency")
    axis.grid(axis="x", linestyle="--", alpha=0.3)
    axis.bar_label(bars, padding=4, fmt="{:,.0f}")
    for spine_name in ("top", "right", "left"):
        axis.spines[spine_name].set_visible(False)
    figure.tight_layout()
    return figure


try:
    results = load_results()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Unable to load trend results: {error}")
    st.stop()

keywords = results[results["type"] == "keyword"].sort_values("rank")
hashtags = results[results["type"] == "hashtag"].sort_values("rank")

st.markdown(
    """
    <section class="hero">
      <h1>📊 Social Media Trend Analyzer</h1>
      <p>HDFS + Hadoop Streaming MapReduce + YARN + Python visualization</p>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Posts processed", "50,000")
metric_2.metric("Reduced trends", "144")
metric_3.metric("Failed shuffles", "0")
metric_4.metric("Mapper outputs", "2")

st.sidebar.header("Dashboard controls")
top_n = st.sidebar.slider("Number of trends", min_value=5, max_value=10, value=10)
st.sidebar.info(
    "The dashboard displays results produced by the Hadoop job. "
    "Hadoop processing runs separately in GitHub Codespaces."
)
st.sidebar.link_button("View source on GitHub", GITHUB_URL)

dashboard_tab, pipeline_tab, data_tab, about_tab = st.tabs(
    ["Trend dashboard", "Processing pipeline", "Result data", "About"]
)

with dashboard_tab:
    st.subheader("Top trends from the processed dataset")
    st.caption(
        "Counts are based on 50,000 deterministic synthetic posts generated with seed 42."
    )

    keyword_tab, hashtag_tab = st.tabs(["Keywords", "Hashtags"])
    with keyword_tab:
        selected = keywords.head(top_n)
        st.pyplot(
            trend_chart(selected, f"Top {top_n} Trending Keywords", "#2563eb"),
            clear_figure=True,
        )
        st.dataframe(
            selected[["rank", "term", "frequency"]],
            column_config={
                "rank": "Rank",
                "term": "Keyword",
                "frequency": st.column_config.NumberColumn("Frequency", format="%d"),
            },
            hide_index=True,
            use_container_width=True,
        )

    with hashtag_tab:
        selected = hashtags.head(top_n)
        st.pyplot(
            trend_chart(selected, f"Top {top_n} Trending Hashtags", "#7c3aed"),
            clear_figure=True,
        )
        st.dataframe(
            selected[["rank", "term", "frequency"]],
            column_config={
                "rank": "Rank",
                "term": "Hashtag",
                "frequency": st.column_config.NumberColumn("Frequency", format="%d"),
            },
            hide_index=True,
            use_container_width=True,
        )

with pipeline_tab:
    st.subheader("How the system works")
    columns = st.columns(4)
    steps = [
        ("1. Dataset", "50,000 CSV posts are generated reproducibly."),
        ("2. HDFS", "The input file is stored at /social_media/input."),
        ("3. Mapper", "Python extracts normalized keywords and hashtags."),
        ("4. Reducer", "Hadoop groups keys and totals their frequencies."),
    ]
    for column, (title, detail) in zip(columns, steps):
        column.markdown(
            f'<div class="pipeline-step"><strong>{title}</strong><br><br>{detail}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Mapper output example")
    st.code("K:python\t1\nH:#ai\t1", language="text")
    st.markdown("#### Reducer output example")
    st.code("K:python\t9522\nH:#ai\t6257", language="text")
    st.success(
        "The completed Hadoop run used YARN, merged two mapper outputs, "
        "produced 144 reduced records, and reported zero failed shuffles."
    )

with data_tab:
    st.subheader("Downloadable result summary")
    display_results = results.copy()
    display_results.columns = ["Type", "Rank", "Term", "Frequency"]
    st.dataframe(display_results, hide_index=True, use_container_width=True)
    st.download_button(
        "Download results as CSV",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="social_media_trends.csv",
        mime="text/csv",
    )

with about_tab:
    st.subheader("About the project")
    st.write(
        "This college Big Data mini-project demonstrates distributed text analytics "
        "with HDFS, Hadoop Streaming MapReduce, YARN, and Python. The web dashboard "
        "presents the version-controlled output of the successfully completed Hadoop job."
    )
    st.warning(
        "The included dataset is synthetic. The frequency results should not be presented "
        "as measurements of activity on a real social-media platform."
    )
    st.markdown(
        "**Future scope:** real-time permitted APIs, time-window trends, sentiment analysis, "
        "phrase extraction, multilingual processing, and a multi-node Hadoop cluster."
    )

st.divider()
st.caption("Built with Apache Hadoop, Python, Matplotlib, Streamlit, Git, and GitHub.")
