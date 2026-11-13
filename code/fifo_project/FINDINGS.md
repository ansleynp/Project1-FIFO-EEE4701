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

None all 8 release mutants were found! However, some mutants survived our earlier tests before we added the missing cases. We used two of those earlier survivors to explain what our first tests missed and how we fixed it.

| Mutant | What it changes | Reachable by my stimulus? | Observable by my checks? | Why it survived |
|--------|-----------------|---------------------------|--------------------------|-----------------|
| full_offbyone (earlier survivor) | Sets full one entry too early. | No, not in the early three-write test. | Yes, once we reach the nearly full condition and check the full flag. | **Reachability:** Our first tests did not fill the FIFO far enough to trigger the mistake. The fill-to-full test reached that condition and caught it. |
| ignore_empty (earlier survivor) | Allows a read while the FIFO is empty. | No, not before we added read-while-empty testing. | Yes, the scoreboard can check the count and flags after the read request. | **Reachability:** Our earlier tests never requested a read while the FIFO was empty. The empty-boundary test reached that case and caught it. |

The final hidden result was 18/20, so two hidden mutants still survived. The hidden grader did not give us their names or the changes they made, so we cannot say exactly why those two survived. The examples above are real survivors from our earlier released-pool testing, not guesses about the hidden mutants.

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

1. **Reachability:** The random regression uses one fixed seed and 600 transactions. A bug that only happens after a different or longer sequence of reads and writes could still be missed.
2. **Reachability:** We run the tests using the default FIFO width and depth. A bug that only happens with other parameter values would not be reached by this run.

**If I had another day:** I would run the constrained-random test with several different seeds to try more read/write sequences and see whether the hidden mutation score improves.
