# Outlier Investigation

## Method
1. **Physical plausibility check** with wide limits (e.g. air temp 250-350 K, speed 0-10,000 rpm, torque 0-200 Nm, tool wear 0-1000 min). Values outside would be sensor errors.
2. **IQR rule** (below Q1 - 1.5*IQR or above Q3 + 1.5*IQR) - used to *find* unusual values, not to delete them.
3. Box plots and comparison of failure rate inside vs outside the outliers.

## Observations
| Variable | IQR outliers | % | Notes |
|---|---|---|---|
| Air temperature [K] | 0 | 0.00 | 295.3-304.5 K |
| Process temperature [K] | 0 | 0.00 | 305.7-313.8 K |
| Rotational speed [rpm] | 418 | 4.18 | all high speeds (> 1895.5 rpm); failure rate 8.4% |
| Torque [Nm] | 69 | 0.69 | failure rate among them 89.9% |
| Tool wear [min] | 0 | 0.00 | 0-253 min |

No values were physically implausible.

## Decision and justification
**All outliers were kept.** They are physically possible readings (high speed with low torque, very high load) and they are strongly linked to failure - for example, 89.9% of torque outliers are failures compared with 3.4% overall. Removing them would delete the information that predictive maintenance needs most. Rows removed in cleaning: **0**.
