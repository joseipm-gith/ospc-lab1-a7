# Measurements: myustiieu2024-hue

Laptop: Apple MacBook Air 13-inch M4 2025, macOS 15.6.1, nproc = 10

## Task 3: audit.py (before the fix)

| Data | Elapsed | User | System | Peak memory |
|---|---|---|---|---|
| Sample (100,000 orders) | 0.65 s | 1.27 s | 0.15 s | 129044 KB |
| Full (8,400,000 orders) | 41.16 s | 30.43 s | 11.51 s | 634872 KB |

System calls on the sample (strace -c):

| Call | Count |
|---|---|
| openat | 100,686 |
| write | 100,001 |
| close | 100,673 |
| total | 301,360 |



## Task 3: audit.py (after the fix)

| Data | Elapsed | User | System | Peak memory |
|---|---|---|---|---|
| Full (8,400,000 orders) | 9.56 s | 9.99 s | 0.35 s | 634744 KB |

System calls on the sample (strace -c): openat 686, write 17, close 673, total 1,376