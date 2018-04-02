# Reader-Writers Problem

1. Version 1 - Readers are prioritized, writers are allowed to starve
1. Version 2 - Writers are prioritized, readers are allowed to starve
1. Version 3 - No starvation

```
% python3 reader_writer_tests.py
Test finished in 3.42 s: 99800 reads and 100 writes by 200 readers and 100 writers; read wait time: 5.2957 ms (avg), 58.396 ms (max), write wait time: 1959.0 ms (avg), 2611.6 ms (max)
Test finished in 3.09 s: 99800 reads and 100 writes by 200 readers and 100 writers; read wait time: 5.2585 ms (avg), 294.98 ms (max), write wait time: 129.96 ms (avg), 260.94 ms (max)
Test finished in 3.93 s: 99400 reads and 400 writes by 200 readers and 100 writers; read wait time: 4.7577 ms (avg), 34.313 ms (max), write wait time: 530.57 ms (avg), 2946.4 ms (max)
Test finished in 3.89 s: 99400 reads and 400 writes by 200 readers and 100 writers; read wait time: 6.8608 ms (avg), 1091.6 ms (max), write wait time: 131.96 ms (avg), 1050.4 ms (max)
Test finished in 15.1 s: 95200 reads and 4700 writes by 200 readers and 100 writers; read wait time: 4.8324 ms (avg), 40.489 ms (max), write wait time: 165.34 ms (avg), 1.3891e+04 ms (max)
Test finished in 15.3 s: 95200 reads and 4700 writes by 200 readers and 100 writers; read wait time: 31.038 ms (avg), 1.2579e+04 ms (max), write wait time: 133.69 ms (avg), 1.2319e+04 ms (max)
Test finished in 89.6 s: 66600 reads and 33300 writes by 200 readers and 100 writers; read wait time: 4.3148 ms (avg), 28.83 ms (max), write wait time: 135.05 ms (avg), 8.7441e+04 ms (max)
Test finished in 91.2 s: 66600 reads and 33300 writes by 200 readers and 100 writers; read wait time: 272.28 ms (avg), 8.9323e+04 ms (max), write wait time: 133.96 ms (avg), 8.7661e+04 ms (max)
```
