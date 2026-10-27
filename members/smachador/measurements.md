# Lab 1 — Measurements
GitHub username: smachador

## Section 5.1 — Permissions
Initial permissions: -rw-r--r--
Error: Permission denied
Fix: chmod +x run_report.sh
New permissions: -rwxr-xr-x

## Section 5.2 — Task 1: Memory

| Orders | Table size (MiB) | Elapsed (s) | User (s) | System (s) | Peak memory (KB) |
|---|---|---|---|---|---|
| 1,000,000 | 106 | 2.28 | 2.31 | 0.31 | 507404 |
| 2,000,000 | 211 | 3.87 | 3.91 | 0.57 | 857696 |
| 4,000,000 | 423 | 7.38 | 6.94 | 1.04 | 1564440 |

Full dataset: 8,400,000 orders, 887 MiB table.
Exit status: 137 (SIGKILL).
Memory events: oom 2, oom_kill 2.
Estimated full dataset peak memory: approximately 3.0 GiB.

Observation: The program exceeds the container memory limit. Using python3 -u confirms stdout buffering caused the loaded message to be missing from the tee log.

## Section 5.3 — Task 2: Extracting Data

Script output: extracts: done
Exit status: 0
Result: All six regional CSV files were empty (0 bytes).

Manual pipeline exit statuses: 2 0 0.
Cause: Incorrect relative input file path.
The grep error is hidden by 2>/dev/null.
Bash normally reports the status of the last pipeline command.

Suggested fix: Correct the input path and enable set -euo pipefail.

