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

## Section 5.4 — Task 3: Auditing

Sample (100,000 orders):
Elapsed: 1.55 s
User: 1.58 s
System: 0.36 s
Peak memory: 130528 KB

Full dataset (8,400,000 orders):
Elapsed: 83.48 s
User: 63.66 s
System: 20.42 s
Peak memory: 634316 KB

System calls (100,000 orders):
openat: 100686
write: 100001
close: 100673
Total: 301360


Diagnosis: The script opens and closes the output file for every order, creating excessive system calls.

Estimated buffered writes for sample: approximately 15 using 128 KiB buffers.


