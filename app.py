"""Streamlit app for exploring InclusionIQ sample feedback."""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.analysis_prototype import (
    SCORE_FIELDS,
    calculate_average_scores,
    classify_overall_sentiment,
    generate_recommendations,
    identify_themes,
)


SAMPLE_DATA_PATH = Path(__file__).resolve().parent / "sample_data" / "employee_feedback_sample.csv"
REQUIRED_COLUMNS = {"department", "comment", *SCORE_FIELDS}
ETHICAL_NOTE = (
    "InclusionIQ is designed for anonymized, voluntary feedback and should be "
    "used to support organizational improvement, not to evaluate individual employees."
)


@st.cache_data
def load_sample_data():
    return pd.read_csv(SAMPLE_DATA_PATH)


def format_score_label(field):
    return field.replace("_", " ").replace("score", "").strip().title()


def validate_columns(dataframe):
    return sorted(REQUIRED_COLUMNS.difference(dataframe.columns))


def prepare_feedback(dataframe):
    cleaned = dataframe.copy()
    cleaned["department"] = cleaned["department"].fillna("Unspecified").astype(str)
    cleaned["comment"] = cleaned["comment"].fillna("").astype(str)

    for field in SCORE_FIELDS:
        cleaned[field] = pd.to_numeric(cleaned[field], errors="coerce")

    return cleaned.dropna(subset=SCORE_FIELDS)


def analyze_feedback(dataframe):
    rows = dataframe.to_dict("records")
    averages = calculate_average_scores(rows)
    themes = identify_themes(rows)
    sentiment = classify_overall_sentiment(averages)
    recommendations = generate_recommendations(themes)
    overall_average = round(sum(averages.values()) / len(averages), 2)

    return {
        "rows": rows,
        "averages": averages,
        "themes": themes,
        "sentiment": sentiment,
        "recommendations": recommendations,
        "overall_average": overall_average,
    }


def build_report(analysis):
    lines = [
        "# InclusionIQ Insight Summary",
        "",
        f"Responses analyzed: {len(analysis['rows'])}",
        f"Overall sentiment: {analysis['sentiment']}",
        f"Average score: {analysis['overall_average']}/5",
        "",
        "## Average Scores",
    ]

    for field, average in analysis["averages"].items():
        lines.append(f"- {format_score_label(field)}: {average}/5")

    lines.extend(["", "## Top Themes"])
    if analysis["themes"]:
        for theme, count in analysis["themes"][:5]:
            lines.append(f"- {theme}: {count} keyword matches")
    else:
        lines.append("- No recurring theme keywords found.")

    lines.extend(["", "## Recommended Actions"])
    if analysis["recommendations"]:
        for recommendation in analysis["recommendations"]:
            lines.append(f"- {recommendation}")
    else:
        lines.append("- Collect more feedback or expand the theme keyword list before recommending action.")

    lines.extend(["", "## Ethical Note", ETHICAL_NOTE])

    return "\n".join(lines)


def main():
    st.set_page_config(page_title="InclusionIQ", layout="wide")

    st.title("InclusionIQ")
    st.caption("Listen Better. Lead Better.")

    uploaded_file = st.sidebar.file_uploader("Employee feedback CSV", type="csv")
    raw_data = pd.read_csv(uploaded_file) if uploaded_file is not None else load_sample_data()
    data_source = uploaded_file.name if uploaded_file is not None else "employee_feedback_sample.csv"

    missing_columns = validate_columns(raw_data)
    if missing_columns:
        st.error("Missing required columns: " + ", ".join(missing_columns))
        st.stop()

    feedback = prepare_feedback(raw_data)
    if feedback.empty:
        st.warning("No complete feedback rows were found.")
        st.stop()

    departments = sorted(feedback["department"].unique())
    selected_departments = st.sidebar.multiselect(
        "Departments",
        departments,
        default=departments,
    )

    filtered_feedback = feedback[feedback["department"].isin(selected_departments)]
    if filtered_feedback.empty:
        st.warning("Select at least one department to analyze.")
        st.stop()

    analysis = analyze_feedback(filtered_feedback)

    metric_columns = st.columns(4)
    metric_columns[0].metric("Responses", len(analysis["rows"]))
    metric_columns[1].metric("Departments", filtered_feedback["department"].nunique())
    metric_columns[2].metric("Average Score", f"{analysis['overall_average']}/5")
    metric_columns[3].metric("Sentiment", analysis["sentiment"])

    st.caption(f"Data source: {data_source}")

    overview_tab, recommendations_tab, data_tab = st.tabs(
        ["Overview", "Recommendations", "Feedback Data"]
    )

    with overview_tab:
        score_summary = pd.DataFrame(
            {
                "Category": [format_score_label(field) for field in analysis["averages"]],
                "Average": list(analysis["averages"].values()),
            }
        )
        st.subheader("Average Scores")
        st.bar_chart(score_summary.set_index("Category"))

        theme_summary = pd.DataFrame(
            analysis["themes"][:5], columns=["Theme", "Keyword Matches"]
        )
        st.subheader("Top Themes")
        if theme_summary.empty:
            st.info("No recurring theme keywords found.")
        else:
            st.bar_chart(theme_summary.set_index("Theme"))

        department_scores = (
            filtered_feedback.groupby("department")[SCORE_FIELDS]
            .mean()
            .rename(columns=format_score_label)
            .round(2)
        )
        st.subheader("Department Averages")
        st.dataframe(department_scores, use_container_width=True)

    with recommendations_tab:
        st.subheader("Recommended Actions")
        if analysis["recommendations"]:
            for recommendation in analysis["recommendations"]:
                st.write(f"- {recommendation}")
        else:
            st.write("- Collect more feedback or expand the theme keyword list before recommending action.")

        st.subheader("Ethical Note")
        st.info(ETHICAL_NOTE)

        st.download_button(
            "Download report",
            data=build_report(analysis),
            file_name="inclusioniq_report.md",
            mime="text/markdown",
        )

    with data_tab:
        display_columns = [
            "response_id",
            "department",
            *SCORE_FIELDS,
            "comment",
        ]
        available_columns = [column for column in display_columns if column in filtered_feedback]
        st.dataframe(filtered_feedback[available_columns], hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()
