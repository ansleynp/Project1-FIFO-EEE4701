# Contributions — Project-Group 3

**Members:** Ansley Pennywitt (an855434) · Christian Reyes (ch784988)
**Repo:** [https://github.com/ansleynp/Project1-FIFO-EEE4701.git]
**Track:** Project 1 - Constrained-Random Verification of a Synchronous FIFO
**Last updated:** 11/12 · **through milestone:** M4

---

## How to read this file

Each milestone section lists what each member owned, with the commits, files, or
tags that show it. "Helped with the testbench" is not a contribution record.
"Wrote the constrained-random sequence and its coverage bins — `tb/seq_rw.py`,
commits `a1b2c3d`..`e4f5g6h`" is.

Work that is genuinely shared gets its own row and says how it was shared
(pairing, review, a split you can describe). Do not inflate, and do not
flatten real differences into a polite fiction — an honest record of an uneven
milestone reads far better than a uniform one nobody believes.

---

## M1 — Initial Repo Setup

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
| Ansley Pennywitt | Created the initial repository setup and later removed files and directories that were not needed. | commits: 8fdeb5f, 0d04175 | 100% |

**Shared or paired work:** We discussed how to organize the project, but Ansley made the initial setup changes.

**What slipped, and who picked it up:** The first setup did not have the final tb/ and crv/ folder structure. Ansley organized those folders later in commit e25eea9.

## M2 — Testbench Components

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
| Ansley Pennywitt | Implemented FIFO driver + added directed test to verify basic functionality | tb/driver.py, crv/test_fifo.py commits: 0ff34ba, 01673d9 | %30 |
| Ansley Pennywitt | Implemented FIFO monitor + added directed test to verify basic functionality | tb/monitor.py, crv/test_fifo.py commit: a43d47d | 25% |
| Christian Reyes | Implemented FIFO scoreboard + added directed test to verify basic functionality | tb/scoreboard.py, crv/test_fifo.py commit: 712a3d2 | 30% |
| Ansley Pennywitt | Connected the driver, monitor, and scoreboard to the main test. | crv/test_fifo.py commit: 8284176 | 15% |

**Shared or paired work:** We worked on separate parts of the testbench. Ansley combined the components so they could be tested together.

**What slipped, and who picked it up:** The driver, monitor, and scoreboard were first developed separately, so they still needed to be connected. Ansley handled the integration in commit 8284176.

**Changes to the division of labor since M1, and why:** We divided the testbench by component. Ansley handled the driver and monitor, and Christian handled the scoreboard.

## M3 — CRV and coverage

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
| Christian Reyes | Added constrained-random FIFO stimulus, including fill and drain modes. | crv/test_fifo.py commit: 1f9f8d4 | 40% |
| Ansley Pennywitt | Functional coverage implementation and integration (coverpoints, crosses, and coverage reporting) | crv/coverage.py, crv/test_fifo.py commit: 74e4dd7 | 40% |
| Christian Reyes | Wrote the initial verification plan. | vplan.md commit: 4279865 | 10% |
| Ansley Pennywitt | Made updates to the verification plan and contribution records. | vplan.md, CONTRIBUTIONS.md commit: 7283ae4 | 10% |

**Shared or paired work:** Christian worked on the random stimulus while Ansley worked on coverage and putting the test files together. We also both contributed to the verification plan.

**What slipped, and who picked it up:** The random transactions and coverage code were initially integrated into the main test file. Ansley later separated the transaction class into transactions.py during the final organization work in M4.

**Changes to the division of labor since M2, and why:** After finishing the testbench components, Christian focused on random stimulus and Ansley focused on functional coverage and test integration.

## M4 — Final Testing and documentation

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
| Christian Reyes | Filled in the mutation findings and documented the results. | FINDINGS.md commit: 1b847ed | 25% |
| Christian Reyes | Cleaned up the verification-plan template. | vplan.md commit: 6e43376 | 10% |
| Ansley Pennywitt | Added a larger directed corner-case test for full, empty, simultaneous requests, reset, and pointer wraparound. | crv/test_fifo.py commit: 7efb0f2 | 30% |
| Ansley Pennywitt | Saved the functional coverage report and organized the project into crv/ and tb/. | coverage.yml, project folders commits: 93aa9f6 e25eea9 | 20% |
| Ansley Pennywitt | Refactored the transactions into a separate module as part of the final code organization. | crv/transactions.py commit: 4131b13 | 15% |

**Shared or paired work:** We divided the final work between testing/code organization and documentation. Ansley handled the added tests and coverage report, while Christian handled FINDINGS.md and vplan cleanup.

**What slipped, and who picked it up:** The coverage results were initially printed during the test but not saved as the required YAML report. Ansley added coverage.yml in commit 93aa9f6. The released mutation score is 8/8, but the reported hidden score of 18/20 means there are still two hidden mutants the tests did not find.

---

## Whole-project summary

One row per member, across all four milestones. This is the row a reader checks
first, so it must be consistent with the four sections above.

| Member | Principal contributions (all four milestones) | Overall share |
|--------|-----------------------------------------------|--------------:|
| Ansley Pennywitt | Initial repository setup, driver and monitor, testbench integration, functional coverage, corner-case testing, coverage report, and file organization. | 50% |
| Christian Reyes | Scoreboard, constrained-random stimulus and fill/drain modes, initial verification plan, findings, and documentation cleanup. | 50% |

**The three things this team did that we would each defend in an interview:**

1. Built a FIFO testbench with a separate driver, monitor, and scoreboard that checks the FIFO against a reference model.
2. Added constrained-random tests and functional coverage to exercise different FIFO states and combinations of reads and writes.
3. Added directed corner-case tests and used mutation testing to measure how many faults the testbench could find.

## Non-code contributions

Real work that leaves a thin git trace — and is graded all the same. Cite the
artifact where one exists.

| Member | Contribution | Where it shows |
|--------|--------------|----------------|
| Christian Reyes | Wrote the first version of the verification plan and later cleaned up the format. | vplan.md commits: 4279865, 6e43376 |
| Christian Reyes | Updated the team contribution record and wrote the mutation findings. | CONTRIBUTIONS.md FINDINGS.md commits: d7369bd, 1b847ed |
| Ansley Pennywitt | Updated the verification plan and kept the contribution records organized. | vplan.md, CONTRIBUTIONS.md commit: 7283ae4 |

## AI assistance

AI was used to help with code organization, reviewing the coverage model, and writing parts of the documentation. The specific uses, who verified the work, and the results are recorded in ai_log.md

---

## Attestation

- [x] Every claim above can be traced to the repo history.
- [x] This file was updated at each milestone, not reconstructed at the end.
- [x] Every member has read this file and agrees it is accurate.

