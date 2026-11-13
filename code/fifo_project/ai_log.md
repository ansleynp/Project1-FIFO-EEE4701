# AI assistance - Project 1 Constrained-Random Verification of a Synchronous FIFO

**Members:** Ansley Pennywitt (an855434) · Christian Reyes (ch784988)

Consistent with the course policy and your `ctm` record: name where an assistant
was used on capstone work, and who verified the output. The verifier is a named
person, always.

| Where | Used for | Verified by | Where the verification shows |
|-------|----------|-------------|------------------------------|
| tb/scoreboard.py | Helped review the scoreboard logic for comparing FIFO outputs with the reference model, including count, full, empty, and read data. | Christian Reyes | tb/scoreboard.py, the test_scoreboard_directed() test in crv/test_fifo.py |
| vplan.md | Helped review the planned test features and rewrite the wording in simpler language. | Christian Reyes | Final vplan.md, checked against code/dut/specs/fifo.md and the planned tests. |
| crv/transactions.py and crv/test_fifo.py | Helped move the transaction class and its constraints into a separate file without changing the existing tests. | Ansley Pennywitt | The two Python files and the passing just test / released just mutate results. |
| crv/coverage.py and coverage.yml | Helped review the coverage model and generate a YAML coverage report. | Ansley Pennywitt | coverage.yml reports 43/43 coverage bins hit (100%) |

# Check the Machine 

**Assistant used:** a general-purpose frontier assistant, web interface, November 2026

---

## 1. Task

**Prompt (verbatim):**

```text
I'm working on a college digital verification project where we're verifying a synchronous FIFO using Python, cocotb, and pyvsc.

I have attached the FIFO specification, our current transaction constraints, testbench, and functional coverage model.

I want you to review these files and suggest an improved version of the constrained-random constraints in transactions.py. The goal is to generate a good mix of FIFO operations, including reads, writes, simultaneous reads and writes, and operations when the FIFO is nearly full or nearly empty.

Please provide:

1. Your proposed replacement code for the constraints in transactions.py.
2. An explanation of what you changed and why.
3. What improvements you expect these changes to make to our testing and functional coverage.
4. Any possible problems or limitations with your suggested constraints.

Please keep the existing transaction class and its interface compatible with test_fifo.py. Do not modify the other files.

Do not assume your changes work or claim you have tested them. I will run the tests separately to check your suggestions.
```

**Files supplied:** `code/dut/specs/fifo.md`, `crv/transactions.py`, `crv/test_fifo.py`, and `crv/coverage.py`.

**What the AI produced:** Replacement constraints that use different random weights depending on the FIFO count and traffic mode. It predicted more simultaneous operations and better full/empty cross coverage. It also changed the data-value weights.

---

## 2. Before

**Prediction 1 —** I think the AI might add constraints that prevent reads when the FIFO is empty or writes when it is full. It might treat these operations as invalid, even though the FIFO specification explains how they should be handled. This would prevent us from testing some important boundary conditions.
*Evidence that would show it:* I will review the generated constraints and run the testbench to see whether reads while empty and writes while full are still being generated. I will also check coverage.yml to see if any occupancy and operation combinations are missing.

**Prediction 2 —** I think the AI might change the random weights in a way that makes certain operations happen more often but actually makes it harder to reach full and empty conditions. This could happen if the constraints favor reads when the FIFO is nearly full and writes when it is nearly empty too heavily.
*Evidence that would show it:* I will compare the number of full, empty, and simultaneous read/write cycles before and after using the AI's constraints. I will also compare the functional coverage percentages and bin counts to see whether the suggested changes improved or reduced coverage.

**Review criteria I am checking against:**

1. The generated constraints must follow the FIFO specification and keep the transaction values within their allowed ranges. They should still allow read requests while empty and write requests while full.
2. The constraints should generate a good mix of writes, reads, simultaneous operations, and full and empty conditions.
3. The suggested changes should work with our existing testbench, and any claims about improving the random distribution or functional coverage should be supported by simulation results.

---

## 3. After

**What I ran:** I temporarily replaced crv/transactions.py with the code from the other AI, without making changes to the rest of the testbench, then ran:

```bash
just test
```

**Raw output:**

```text
********************************************************************************************
** TEST                                STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
********************************************************************************************
** test_fifo.test_crv                   PASS        6041.00          17.03        354.62  **
** test_fifo.test_driver_directed       PASS          71.00           0.00      23227.50  **
** test_fifo.test_monitor_directed      PASS          61.00           0.00      20291.60  **
** test_fifo.test_scoreboard_directed   PASS         121.00           0.01      16234.25  **
** test_fifo.test_fifo_corner_cases     PASS        1221.00           0.09      13135.92  **
********************************************************************************************
** TESTS=5 PASS=5 FAIL=0 SKIP=0                     7515.01          19.91        377.45  **
********************************************************************************************

top:
  cover_percentage: 100.0
  coverage: 43
  size: 43
```

**The number:** 43/43 coverage bins (100%) for both the original and AI-generated constraints. All 20 occupancy × operation combinations were covered in both runs.

| Measurement | Original | AI-generated |
|---|---:|---:|
| Empty cycles | 40 | 14 |
| Full cycles | 40 | 52 |
| Near-empty cycles | 69 | 41 |
| Near-full cycles | 96 | 111 |
| Simultaneous read/write requests | 191 | 244 |
| Full × write-only | 12 | 22 |
| Empty × read-only | 8 | 1 |
| Occupancy × operation bins covered | 20/20 | 20/20 |
| Total coverage bins covered | 43/43 | 43/43 |

**Against each prediction:**

| # | Predicted | Observed | Verdict |
|---|-----------|----------|---------|
| 1 | The AI might block reads while empty or writes while full. | Both still occurred: empty × read-only had 1 hit and full × write-only had 22 hits. | Refuted |
| 2 | Changing the weights might make the full and empty cases harder to reach. | Empty visits dropped from 40 to 14, but full visits increased from 40 to 52. Simultaneous requests also increased. | Partly confirmed |

**Anything I did not predict:** The AI kept 100% coverage, but made the empty × read-only case much less common (8 hits down to 1). This shows that a bin can be marked covered even if it is barely exercised. The AI predicted improved cross coverage, but both runs were already 20/20, so there were no uncovered bins for it to close. Its code changed the traffic distribution, but did not improve the coverage percentage.

---

## 4. Takeaway

**The class of failure (or of success):** The AI-generated constraints worked with our testbench and reached all the defined coverage bins. However, its claim that coverage would improve was not supported by the overall percentage, since the original code had already reached 100%. Some cases became more common while others became less common.

**Where it connects:** This connects to functional coverage and constrained-random verification. Hitting a bin once makes it count as covered, but that does not tell us whether the test exercises that situation often enough. We needed the actual hit counts to evaluate the AI's claim.

**What I would change in how I framed the request:** Next time I would ask the AI to compare the expected hit counts for specific boundary cases instead of just claiming better overall coverage. I would also ask it to explain any tradeoffs it expects in the random distribution.

---

## Disclosure

- [x] Every prompt above is verbatim and complete.
- [x] I have marked every edit I made to the generated output.
- [x] The tool is described by class, not by product name.
- [x] Section 2 was written before the prompt was sent.
