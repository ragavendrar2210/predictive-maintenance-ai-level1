# Failure Rate Report (AI4I 2020, 10,000 rows)

## Overall
| Class | Count | % |
|---|---|---|
| No failure (0) | 9,661 | 96.61% |
| Failure (1) | 339 | 3.39% |

The dataset is strongly imbalanced (about 1 failure per 29 rows).

## Failure modes (a row can have more than one)
| Mode | Meaning | Count |
|---|---|---|
| HDF | Heat dissipation failure | 115 |
| OSF | Overstrain failure | 98 |
| PWF | Power failure | 95 |
| TWF | Tool wear failure | 46 |
| RNF | Random failure | 19 |

## By product type
| Type | Rows | Failures | Failure rate |
|---|---|---|---|
| L | 6,000 | 235 | 3.92% |
| M | 2,997 | 83 | 2.77% |
| H | 1,003 | 21 | 2.09% |

Chi-square test: chi2 = 13.75, p = 0.001 (significant), Cramér's V = 0.037 (very weak association).

## By tool-wear band (minutes)
| Band | Rows | Failure rate |
|---|---|---|
| 0-50 | 2,396 | 2.17% |
| 51-100 | 2,271 | 2.33% |
| 101-150 | 2,295 | 2.18% |
| 151-200 | 2,276 | 2.90% |
| 200+ | 762 | 15.49% |

## Important observations
- Failure risk rises sharply once tool wear passes 200 minutes.
- Failures have higher median torque (53.7 vs 39.9 Nm) and lower median speed (1365 vs 1507 rpm).
- Label inconsistencies in the original data: 9 rows have `Machine failure = 1` with no mode flagged; 18 rows have `RNF = 1` with `Machine failure = 0`. Labels were kept as provided.
- These are associations from a synthetic dataset, not proven causes.
