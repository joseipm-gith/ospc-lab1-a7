
## Task 1: report.py memory
| Orders | Table | Peak memory (KB) | Elapsed |
| 1,000,000 | 106 MiB | 507096 | 1.37 s |
| 2,000,000 | 211 MiB | 857196 | 2.26 s |
| 4,000,000 | 423 MiB | 1569204 | 4.44 s |
| 8,400,000 | 887 MiB | killed (exit 137), oom_kill 2 | |
memory.max = 2147483648

## Task 2: extracts.sh
Files empty (0 bytes), exit status 0, PIPESTATUS 2 0 0

## Task 3: audit.py
Sample: 0.85 s elapsed, 1.65 user, 0.22 system, 129536 KB
Full: 44.72 s elapsed, 32.53 user, 13.31 system, 634252 KB
strace -c (sample): openat 100686, write 100001, close 100673
