# InclusionIQ
### Listen Better. Lead Better.

**InclusionIQ** is an AI-powered tool that analyzes anonymous employee survey feedback to generate actionable insights on workplace culture and leadership. It helps organizations better understand employee experiences and supports data-driven decision-making.

## Why I Built It
Organizations often struggle to interpret large volumes of qualitative employee feedback. As a sociology student with an interest in human resources, I created InclusionIQ to bridge the gap between employee voice and leadership action.

## How It Works
1. **Input:** Users upload or paste anonymous survey responses.
2. **AI Analysis:** The system identifies themes, sentiment, strengths, and areas for improvement.
3. **Insights:** Actionable recommendations are generated for HR teams and managers.
4. **Output:** Results are presented in a clear and easy-to-understand summary.

## Key Features
- Theme extraction from open-ended responses
- Sentiment analysis
- Quantitative summaries of survey ratings
- Department-level filtering
- Actionable recommendations
- Downloadable Markdown insight report
- Ethical and privacy-focused design

## Demo Materials
- Streamlit app: `app.py`
- Sample dataset: `sample_data/employee_feedback_sample.csv`
- Sample report: `docs/sample_report.md`
- Prototype analysis script: `src/analysis_prototype.py`
- Prototype output example: `docs/prototype_output.md`

These files demonstrate the type of anonymous survey data InclusionIQ is designed to analyze, the kind of workplace insight report it can generate, the early analysis logic behind the prototype, example prototype output, and the interactive Streamlit experience.

## How to Run the Streamlit App
1. Clone or download this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
streamlit run app.py
```

The app loads the fictional sample dataset by default and can also analyze an uploaded CSV with the same columns.

## How to Run the Prototype Script
1. Clone or download this repository.
2. Open the project folder in a code editor or terminal.
3. Run the prototype script:

```bash
python src/analysis_prototype.py
```

The script reads the fictional sample dataset, calculates average workplace scores, identifies recurring themes, estimates overall sentiment, and prints recommended actions.

## Technologies Used
- OpenAI Codex
- Python for prototype analysis logic
- Streamlit for the dashboard app
- Pandas for data loading and filtering
- JavaScript for future interface development
- HTML/CSS for interface design

## Ethical Considerations
InclusionIQ analyzes only anonymized and voluntary feedback. The tool is intended to support organizational improvement and should not be used to evaluate individual employees.

## Future Improvements

- Enhanced dashboard visualizations for easier interpretation of insights
- Real-time feedback analysis
- Integration with HR platforms and survey tools
- Downloadable workplace insight reports
- Expanded theme detection and AI-assisted recommendations

## Author
**Kathryn Buckley**  
Sociology Student, Lamar University
