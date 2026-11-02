# Measurements of fagonzalezieu2024-lgtm (Lab 1, Section 5, in class)

Laptop and container: see `machine.txt`. Taken on 2026-11-02 20:31 UTC, CPUs in the container: 10, memory limit of the container: 2147483648.

All runs use the **original** scripts of the template (copied to `/tmp/lab1_orig`), before our fixes, with `OUT=/tmp/lab1_out` and

```
T='%e s elapsed, %U s user, %S s system, %M KB peak memory'
```

## 5.1 Warm-up: generating the report

```
$ ./run_report.sh; echo "exit status: $?"
bash: line 1: ./run_report.sh: Permission denied
exit status: 126
```

```
$ ls -l run_report.sh
-rw-r--r-- 1 analyst analyst 402 Nov  2 20:31 run_report.sh
```

After our fix (`chmod +x`, committed with mode 100755), in the team repository:

```
$ ls -l run_report.sh; git ls-files -s run_report.sh 2>/dev/null || true
-rwxr-xr-x 1 analyst analyst 565 Nov  2 20:26 run_report.sh
100755 53f8887d5aef948d35dd9e030fe1148577c338b5 0	run_report.sh
```

1. The execute permission (`x`) is missing for everyone: owner, group and others have only `rw-`/`r--`. The shell refuses with *Permission denied*, exit status 126.
2. `bash run_report.sh` executes `bash` (which is executable) and bash only *reads* the script, so read permission is enough.
3. Git stores only 100644 or 100755. The template stored 100644, so on macOS/Linux every clone has `-rw-r--r--`. On Windows the bind-mounted NTFS folder can show every file as `-rwxrwxrwx`, so the script may run there: the permission comes from the mount, not from git.

## 5.2 Task 1: generating the report... again

Memory events of the container **before**:

```
$ cat /sys/fs/cgroup/memory.events
low 0
high 0
max 0
oom 0
oom_kill 0
oom_group_kill 0
sock_throttled 0
```

(`PYTHONUNBUFFERED=1` makes Python print at once, as it does in a terminal, so the *report: loaded* line survives the kill when the output is captured. See question 4.)

```
$ PYTHONUNBUFFERED=1 /usr/bin/time -f "$T" python3 steps/report.py; echo "exit status: $?"
report: loaded 8,400,000 orders (887 MiB)
Command terminated by signal 9
8.52 s elapsed, 8.50 s user, 0.65 s system, 2083856 KB peak memory
exit status: 137
```

Memory events **after** (compare `oom_kill` with the line above):

```
$ cat /sys/fs/cgroup/memory.events
low 0
high 0
max 471
oom 1
oom_kill 1
oom_group_kill 0
sock_throttled 0
```

```
$ head -n 1000001 ~/data/sales_2025.csv > /tmp/orders_1m.csv; DATA=/tmp/orders_1m.csv PYTHONUNBUFFERED=1 /usr/bin/time -f "$T" python3 steps/report.py; echo "exit status: $?"
report: loaded 1,000,000 orders (106 MiB)
report: done
1.16 s elapsed, 1.77 s user, 0.07 s system, 506432 KB peak memory
exit status: 0
```

```
$ head -n 2000001 ~/data/sales_2025.csv > /tmp/orders_2m.csv; DATA=/tmp/orders_2m.csv PYTHONUNBUFFERED=1 /usr/bin/time -f "$T" python3 steps/report.py; echo "exit status: $?"
report: loaded 2,000,000 orders (211 MiB)
report: done
1.92 s elapsed, 2.65 s user, 0.06 s system, 860632 KB peak memory
exit status: 0
```

```
$ head -n 4000001 ~/data/sales_2025.csv > /tmp/orders_4m.csv; DATA=/tmp/orders_4m.csv PYTHONUNBUFFERED=1 /usr/bin/time -f "$T" python3 steps/report.py; echo "exit status: $?"
report: loaded 4,000,000 orders (423 MiB)
report: done
3.71 s elapsed, 4.36 s user, 0.12 s system, 1563816 KB peak memory
exit status: 0
```

```
$ python3 steps/report.py | tee /tmp/report.log; echo "PIPESTATUS: ${PIPESTATUS[@]}"; echo "--- /tmp/report.log:"; cat /tmp/report.log
PIPESTATUS: 137 0
--- /tmp/report.log:
```

| Orders | Size of the table (MiB, printed by report.py) | Peak memory (KB) | Peak memory (GiB) |
|---|---|---|---|
| 1,000,000 | 106 | 506432 | 0.48 |
| 2,000,000 | 211 | 860632 | 0.82 |
| 4,000,000 | 423 | 1563816 | 1.49 |
| 8,400,000 (whole file) | 887 | killed | ~3.1 (estimated) |

1. Exit status 137 = 128 + 9: the process was ended by signal 9, SIGKILL. It was sent by the kernel's out-of-memory killer, because the container's cgroup reached `memory.max` (2 GiB). The `oom_kill` counter in `memory.events` went up by one (and `max` counts how often the limit was hit).
2. The printed size is only the loaded DataFrame. Peak memory is much larger: pandas needs extra memory while parsing the CSV, `pd.to_datetime` and the `revenue` column add copies, and the 12 monthly `months` tables plus `pd.concat` make a second full copy of the data. The peak is several times the table, above the 2 GiB limit.
3. Peak memory grows linearly with the number of orders (about twice for twice the orders). Extrapolating the largest run that finished (4 million) to 8.4 million gives about **3.1 GiB**, more than the 2 GiB of the container.
4. `report: loaded ...` is printed *before* the kill, but when stdout is a pipe (not a terminal) Python buffers its output in a block buffer. The process was killed with SIGKILL before it could flush the buffer, so the line never reached `tee`. With a terminal, stdout is line-buffered and the line appears.

## 5.3 Task 2: extracting data

```
$ bash steps/extracts.sh; echo "exit status: $?"; ls -l $OUT/extracts
extracts: done
exit status: 0
total 0
-rw-r--r-- 1 analyst analyst 0 Nov  2 20:32 Benelux.csv
-rw-r--r-- 1 analyst analyst 0 Nov  2 20:32 DACH.csv
-rw-r--r-- 1 analyst analyst 0 Nov  2 20:32 France.csv
-rw-r--r-- 1 analyst analyst 0 Nov  2 20:32 Iberia.csv
-rw-r--r-- 1 analyst analyst 0 Nov  2 20:32 Italy.csv
-rw-r--r-- 1 analyst analyst 0 Nov  2 20:32 Nordics.csv
```

```
$ grep ",Iberia," ../data/sales_2025.csv | cut -d, -f1,2,4,6,7 | wc -l; echo "PIPESTATUS: ${PIPESTATUS[@]}"; pwd
grep: ../data/sales_2025.csv: No such file or directory
0
PIPESTATUS: 2 0 0
/tmp/lab1_out/extracts
```

1. The script does `cd $OUT/extracts` and then reads the relative path `../data/sales_2025.csv`, i.e. `$OUT/data/sales_2025.csv` (here `/tmp/lab1_out/data/...`, by default `~/data/out/data/...`), which does not exist. `grep` fails (status 2), the pipeline writes nothing, and `>` still creates every file: six files of 0 bytes.
2. Without `set -e`/`pipefail`, the exit status of a pipeline is the one of its last command (`cut`, which succeeds on empty input), and the loop goes on. The last command of the script is `echo extracts: done`, which succeeds, so the script exits 0.
3. `2>/dev/null` hides only the standard error of `grep`: here *No such file or directory*. Errors from `cut`, from the redirection `> "$region.csv"` (e.g. permission denied) and from `cd`/`mkdir` still appear.
4. `-e`: exit as soon as a command fails; `-u`: an unset variable is an error; `-o pipefail`: a pipeline fails if any command in it fails. Adding `set -euo pipefail` at the top (and removing `2>/dev/null`) makes `extracts.sh` stop with grep's error and a non-zero status. The real fix is to read the absolute path `$DATA` (default `$HOME/data/sales_2025.csv`).

## 5.4 Task 3: auditing

```
$ DATA=/home/analyst/data/sales_2025_sample.csv /usr/bin/time -f "$T" python3 steps/audit.py
audit: 100,000 lines written
0.77 s elapsed, 1.25 s user, 0.21 s system, 127740 KB peak memory
```

```
$ /usr/bin/time -f "$T" python3 steps/audit.py
audit: 8,400,000 lines written
41.25 s elapsed, 28.11 s user, 13.91 s system, 634624 KB peak memory
```

```
$ DATA=/home/analyst/data/sales_2025_sample.csv strace -c -e trace=openat,write,close python3 steps/audit.py; ls -l $OUT/audit_2025.csv
audit: 100,000 lines written
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 35.63    0.345806           3    100686        13 openat
 33.88    0.328834           3    100001           write
 30.50    0.296025           2    100673           close
------ ----------- ----------- --------- --------- ----------------
100.00    0.970665           3    301360        13 total
-rw-r--r-- 1 analyst analyst 1952269 Nov  2 20:33 /tmp/lab1_out/audit_2025.csv
```

1. About 100,000 `openat`, 100,000 `write` and 100,000 `close` (one of each per order, plus a few dozen from Python's start-up, imports and `read_csv`): the loop opens the file, writes one line and closes it for every order.
2. On the whole file: user 28.11 s, system 13.91 s, so about **33 %** of the CPU time is spent in the kernel, serving 3 system calls per order (25 million in total). `report.py` (see 5.2) spends almost all its time in user code and only a small share in system time.
3. No. `close` (and a `write`) only hands the data to the kernel's page cache; the kernel writes it to disk later. Only `fsync` forces it onto the disk. So reopening protects only against losing the lines still in Python's own buffer if the program is killed; it does not protect against a power loss or a crash of the machine. A single open file plus `flush()`/`fsync` at chosen points would give the same (or better) guarantee for a tiny fraction of the system calls.
4. The file has 1952269 bytes for the sample. With one open file and a 128 KiB buffer Python makes about size / 131072 `write` calls: about 15 for the 100,000 orders, and about 84 times as many (a few thousand) for the 8.4 million, instead of millions.

