# Data Leakage Checklist

**Data leakage** = the model gets information during training that it would not have when making a real prediction. It makes results look better than they really are.

| # | Possible leakage source | Risk | Safeguard |
|---|---|---|---|
| 1 | Failure-mode columns TWF, HDF, PWF, OSF, RNF | High - recorded after the failure; any mode = 1 almost always means failure | Excluded from model inputs (`pp.excluded_columns()`), automatic assert in Notebook 5 |
| 2 | Target `Machine failure` used to build features | High | No engineered feature uses the target; it is used only to describe features |
| 3 | `UDI` row number | Medium - an ID may accidentally encode order | Excluded |
| 4 | `Product ID` | Medium - unique ID; its letter duplicates `Type` | Excluded; `Type` used instead |
| 5 | Fake time features (lag, rolling, failure history) | High - no real timestamps exist | Not created |
| 6 | Scaling / encoding fitted on the full dataset | Medium | Level 2: split train/test first, fit transforms on train only |
| 7 | Outlier rules or bin edges chosen with test data | Low | Bins are fixed 50-minute bands; no rows removed |
| 8 | Duplicate rows across train/test | Low | 0 exact duplicates found |
| 9 | Oversampling before splitting (Level 2) | Medium | Apply any resampling only inside the training set |

Status: Level 1 dataset `data/processed/engineered_data.csv` still contains the target and failure modes (needed for labels and analysis), but the list of allowed model inputs excludes them.
