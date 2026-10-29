# Antibiotic Time-Out

Interactive antibiotic stewardship training for hospital physicians and nurses, designed by Rodolfo J. Salas-Auvert, M.D.

## What's here

| File | Purpose |
| --- | --- |
| `index.html` | The complete module: practice track (case review, body map explorer, antibiotic reference) and CME track. |
| `cases.json` | Approved teaching cases. The page rotates among approved cases for each decision. |
| `labels.json` | Official FDA label facts for each antibiotic, with retrieval dates and a change log. |
| `scripts/refresh_labels.py` | Refreshes `labels.json` from openFDA by DailyMed set ID. |
| `.github/workflows/refresh-labels.yml` | Runs the refresh weekly and commits any change. |
| `favicon.svg` | Hourglass mark. |

## Publishing with GitHub Pages

Settings → Pages → Build and deployment → Deploy from a branch → `main` / root.

## Content status

Educational content under physician review. Not yet accredited for continuing education credit. Drug information is retrieved automatically from official sources and must be verified against the current prescribing information and local guidance before clinical use.
