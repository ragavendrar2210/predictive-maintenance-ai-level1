# Predictive Maintenance & Equipment Failure Intelligence System — Level 1 (Foundations)

Second-year CSE college project. Level 1 covers data understanding, cleaning, EDA, hypothesis testing and leakage-safe feature engineering. **No ML models are trained at this level.**

## Dataset
- **AI4I 2020 Predictive Maintenance Dataset**, UCI Machine Learning Repository
- https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
- File: `data/raw/ai4i2020.csv` (10,000 rows, 14 columns), licence CC BY 4.0 (S. Matzka, 2020)
- Target: `Machine failure` (339 failures = 3.39%)

If the CSV is missing, Notebook 01 downloads it automatically; otherwise download the ZIP from the link above and put `ai4i2020.csv` in `data/raw/`.

## Installation
```bash
python -m venv venv
# Windows: venv\Scripts\activate    macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
jupyter lab
```
Google Colab: upload the whole folder, open a notebook from `notebooks/`, and run `!pip install seaborn` if needed.

## Execution order
Open the `notebooks/` folder and run each notebook top-to-bottom (**Run → Run All Cells**):
1. `01_data_understanding.ipynb` — structure, data dictionary, failure counts
2. `02_data_cleaning.ipynb` — validation, outlier investigation → `data/processed/cleaned_data.csv`
3. `03_eda.ipynb` — visualisations and interpretations
4. `04_statistics.ipynb` — Mann–Whitney U, Welch t-test, chi-square, Holm correction, effect sizes
5. `05_feature_engineering.ipynb` — new features, leakage checks → `data/processed/engineered_data.csv`

## Folder structure
```
predictive-maintenance-ai/
├── data/raw/ai4i2020.csv
├── data/processed/cleaned_data.csv, engineered_data.csv
├── notebooks/01 … 05 .ipynb
├── src/preprocessing.py
├── reports/sensor_data_dictionary.csv, failure_rate_report.md,
│           outlier_investigation.md, leakage_checklist.md
├── requirements.txt
└── README.md
```

## Key findings
- No missing values, no duplicates, no implausible readings → 0 rows removed.
- Failures are associated with higher torque, lower/extreme rotational speed, higher tool wear (risk ≈ 15% above 200 min) and slightly higher air temperature.
- Product type L fails most (3.9%) vs H (2.1%); significant but very weak (Cramér's V = 0.04).
- Engineered features: temperature difference, temperature ratio, torque×rpm, power in watts, tool-wear bands.

## Limitations
- Synthetic dataset; results may not transfer to real machines.
- Strong class imbalance (3.39% failures).
- No timestamps or repeated machines → no lag/rolling/history features.
- Statistical results show association, not causation.
- Small label inconsistencies exist in the original data (kept as provided).
