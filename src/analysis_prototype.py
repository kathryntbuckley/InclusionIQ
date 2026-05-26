"""
InclusionIQ analysis prototype

This script analyzes a fictional employee feedback dataset and prints a basic
workplace insight summary. It is intended as an early prototype demonstrating
how InclusionIQ can transform anonymous survey responses into usable insights.
"""

import csv
from collections import Counter
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "sample_data" / "employee_feedback_sample.csv"

THEME_KEYWORDS = {
    "Leadership Communication": ["communication", "leadership", "updates", "expectations", "transparent", "unclear"],
    "Advancement and Development": ["advancement", "development", "promotions", "career", "growth", "opportunities"],
    "Team Support": ["supportive", "team", "coworkers", "included", "respectful"],
    "Psychological Safety": ["speaking up", "comfortable", "concerns", "feedback", "questions"],
    "Fairness": ["fair", "fairness", "criteria", "decided", "opportunities"],
}

SCORE_FIELDS = [
    "respect_score",
    "communication_score",
    "fairness_score",
    "belonging_score",
]


def load_feedback(path):
    """Load employee feedback rows from a CSV file."""
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def calculate_average_scores(rows):
    """Calculate average Likert scores for each survey category."""
    averages = {}
    for field in SCORE_FIELDS:
        scores = [int(row[field]) for row in rows if row.get(field)]
        averages[field] = round(sum(scores) / len(scores), 2) if scores else 0
    return averages


def identify_themes(rows):
    """Identify recurring themes based on simple keyword matching."""
    theme_counts = Counter()
    comments = " ".join(row["comment"].lower() for row in rows)

    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in comments:
                theme_counts[theme] += comments.count(keyword)

    return theme_counts.most_common()


def classify_overall_sentiment(averages):
    """Estimate overall sentiment from average survey scores."""
    overall_average = sum(averages.values()) / len(averages)

    if overall_average >= 4:
        return "Positive"
    if overall_average >= 3:
        return "Mixed-positive"
    return "Needs attention"


def generate_recommendations(themes):
    """Generate simple recommendations based on recurring themes."""
    recommendations = []
    theme_names = [theme for theme, _count in themes]

    if "Leadership Communication" in theme_names:
        recommendations.append("Create a consistent communication process for policy, scheduling, and role expectation updates.")
    if "Advancement and Development" in theme_names:
        recommendations.append("Clarify promotion criteria, development pathways, and internal mobility options.")
    if "Psychological Safety" in theme_names:
        recommendations.append("Encourage managers to invite input and respond constructively to employee concerns.")
    if "Team Support" in theme_names:
        recommendations.append("Recognize and reinforce supportive team behaviors already working well.")
    if "Fairness" in theme_names:
        recommendations.append("Review how opportunities are communicated and distributed across teams.")

    return recommendations


def print_report(rows, averages, themes, sentiment, recommendations):
    """Print a readable report to the terminal."""
    print("# InclusionIQ Prototype Analysis")
    print()
    print(f"Responses analyzed: {len(rows)}")
    print(f"Overall sentiment: {sentiment}")
    print()

    print("## Average Scores")
    for field, average in averages.items():
        label = field.replace("_", " ").title()
        print(f"- {label}: {average}/5")
    print()

    print("## Top Themes")
    for theme, count in themes[:5]:
        print(f"- {theme}: {count} keyword matches")
    print()

    print("## Recommended Actions")
    for recommendation in recommendations:
        print(f"- {recommendation}")
    print()

    print("## Ethical Note")
    print("This prototype uses fictional, anonymized sample data and is designed to support organizational improvement, not evaluate individual employees.")


def main():
    rows = load_feedback(DATA_PATH)
    averages = calculate_average_scores(rows)
    themes = identify_themes(rows)
    sentiment = classify_overall_sentiment(averages)
    recommendations = generate_recommendations(themes)
    print_report(rows, averages, themes, sentiment, recommendations)


if __name__ == "__main__":
    main()
