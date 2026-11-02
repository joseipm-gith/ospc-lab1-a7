
# Individual Measurements — Jose

## Machine
- Model: MacBook Pro 13-inch (2017)
- OS: macOS Ventura 13.7.8
- Physical cores: 2
- Logical threads: 4

## Task 2 — Extracts
### Symptom
All six regional extraction files contained zero rows.

### Diagnosis
The script used an incorrect relative path to the input CSV file.

### Fix
Changed extracts.sh to read from the DATA variable,
using the correct input file path.
Added set -euo pipefail for error handling.

### Verification
All six regional extraction files PASS tools/check.py.

### Performance measurements
Before: Not recorded.
After: 13.23 s elapsed, 8.70 s user, 11.15 s system, 7772 KB peak memory


## Task 3 — Audit (Before Optimization)
- Dataset: 8,400,000 orders
- Elapsed time: 233.89 s
- User CPU time: 179.78 s
- System CPU time: 52.97 s
- Peak memory: 640120 KB

### System Calls (100,000-order sample)
- write: 100001 calls
- openat: 100689 calls
- close: 100677 calls

## Worker Experiment

The statistics step was tested with 1, 2, 4, 8,
and 16 workers, three runs per configuration.

| Workers | Average elapsed time |
|---|---|
| 1 | 65.54 s |
| 2 | 54.13 s |
| 4 | 55.63 s |
| 8 | 54.78 s |
| 16 | 63.44 s |

The fastest average time was achieved with 2 workers.
Using more workers did not consistently improve performance.

Full results: members/joseipm-gith/sweep.csv

