# FINDINGS — Project 1 Constrained-Random Verification of a Synchronous FIFO · Ansley Pennywitt · Christian Reyes

## Score

| Pool | found | total | % |
|------|------:|------:|--:|
| released (practice) | 8 | 8 | 100% |
| hidden (reported at grading) | 18 | 20 | 90% |

**Command run:**

```
just mutate
```

## Survivors

None all 8 release mutants were found!

| Mutant | What it changes | Reachable by my stimulus? | Observable by my checks? | Why it survived |
|--------|-----------------|---------------------------|--------------------------|-----------------|
| none | n/a | n/a | n/a | n/a |

## What I changed, and what it bought

| Change | Score before | Score after | Which survivors it caught |
|--------|-------------:|------------:|---------------------------|
| Added a driver, monitor, scoreboard, and reference model checks to the original three-write test. | 1/8 | 5/8 | This helped find more errors involving the empty flag, count, read data, stored data, and pointer wraparound. |
| Added tests that filled the FIFO completely and tried writing while it was full. | 5/8 | 7/8 | full_offbyone and ignore_full |
| Added tests that emptied the FIFO and tried reading while it was empty. | 7/8 | 8/8 | ignore_empty |
| Added tests for simultaneous reads and writes, full/empty boundaries, and pointer wraparound, along with a seeded random test. | 8/8 | 8/8 | No additional released mutants, but these tests checked more situations. |
| For Project 1, added pyvsc transactions and constraints, a 600-cycle seeded random test, and functional coverage. | 8/8 | Still 8/8; first hidden run was 10/20 | We kept finding all released mutants and got a starting score for the hidden pool. The hidden results did not show mutant names. |
| Added test_fifo_corner_cases() to check full and empty conditions, including reads and writes at those limits and simultaneous requests. | 10/20 (hidden) | 18/20 (hidden) | The hidden results do not identify individual mutants, so we cannot say exactly which ones were caught by this change. |


## Residual risk

What this suite still cannot catch, stated plainly. Name a fault class, not a
mutant id — the pool is a sample, not the population.

1. The random regression uses one fixed seed and 600 transactions. A bug that only happens after a different or longer sequence of reads and writes could still be missed.
2. We run the tests using the default FIFO width and depth. A bug that only happens with other parameter values would not be found by this run.

**If I had another day:** I would run the constrained-random test with several different seeds to try more read/write sequences and see whether the hidden mutation score improves.
