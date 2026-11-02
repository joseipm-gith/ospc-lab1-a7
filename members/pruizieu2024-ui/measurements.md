# Measurements: Paula Ruiz (@pruizieu2024-ui)

## Machine
- Laptop: Apple MacBook Pro 14-inch M3 Pro Nov 2023, macOS Sequoia 15.6
- Cores and threads: 11 cores (5 performance + 6 efficiency), 11 threads
- CPUs in the container (`nproc`): 11
- Container memory limit: 2 GiB, no swap

## Task 4: segments.py, whole file (8.4 million orders)

`/usr/bin/time -f "$T" python3 steps/segments.py`

| Version | Elapsed | User | System | Peak memory |
|---|---|---|---|---|
| Before (loop over rows, strptime per order) | 27.63 s | 28.24 s | 0.25 s | 750,452 KB |
| First fix (labels built as text columns) | 5.88 s | 6.22 s | 0.53 s | 1,652,532 KB |
| Final fix (group on integers, labels at the end) | 3.99 s | 4.44 s | 0.41 s | 1,259,600 KB |

## Task 4: profile on the sample (100,000 orders)

`DATA=~/data/sales_2025_sample.csv python3 -m cProfile -s tottime steps/segments.py`

- Before: 3,646,598 function calls in 1.040 s. `segment()`, `strptime`, `locale.getlocale` and `locale.normalize` each called about 100,000 times (once per order); `strptime` cumtime 0.545 s.
- After: 452,338 function calls in 0.283 s; no function called once per order.

## Worker experiment

`bash tools/sweep.sh pruizieu2024-ui`, results in `sweep.csv` in this folder.
