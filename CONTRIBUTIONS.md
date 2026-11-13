# Contributions — Project-Group 3 · <track>

**Members:** Ansley Pennywitt (an855434) · Christian Reyes (ch784988)
**Repo:** [<URL>](https://github.com/ansleynp/Project1-FIFO-EEE4701.git)
**Track:** Project 1 - Constrained-Random Verification of a Synchronous FIFO
**Last updated:** 11/12 · **through milestone:** M2

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
| Ansley | Created repo + configured the repo setup | commit: 8fdeb5f | 5% |

**Shared or paired work:** Shared discussions only about what we think is best for the repo setup to start off with.

**What slipped, and who picked it up:**
Didn't include correct directories to start off had to to add a tb/ and crv/ later on (picked up by Ansley Pennywitt)

## M2 — Testbench Components

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
| Ansley Pennywitt | Implemented FIFO driver + added directed test to verify basic functionality | tb/driver.py, tb/test_fifo.py commits: 0ff34ba, 01673d9 |               |
| Ansley Pennywitt | Implemented FIFO monitor + added directed test to verify basic functionality | tb/monitor.py, tb/test_fifo.py commit: a43d47d |               |
| Christian Reyes | Implemented FIFO scoreboard + added directed test to verify basic functionality | tb/scoreboard.py, tb/test_fifo.py commit: 712a3d2 | 30% |

**Shared or paired work:**

**What slipped, and who picked it up:**

**Changes to the division of labor since M1, and why:**

## M3 — CRV and coverage

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
| Christian Reyes | Added constrained-random FIFO stimulus, including fill and drain modes. | code/fifo_project/crv/test_fifo.py commit: 1f9f8d4 | 40% |
| Ansley Pennywitt | Functional coverage implementation and integration (coverpoints, crosses, and coverage reporting) | tb/coverage.py, tb/test_fifo.py commit: 74e4dd7 |               |
| Christian Reyes | Wrote the initial verification plan. | vplan.md commit: 4279865 | 10% |

**Shared or paired work:**

**What slipped, and who picked it up:**

**Changes to the division of labor since M2, and why:**

## M4 — Final Testing and documentation

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
|        |                 |                                  |               |
| Christian Reyes | Filled in the mutation findings and documented the results. | FINDINGS.md commit: 1b847ed | 25% |
| Christian Reyes | Cleaned up the verification-plan template. | vplan.md commit: 6e43376 | 10% |

**Shared or paired work:**

**What slipped, and who picked it up:**

---

## Whole-project summary

One row per member, across all four milestones. This is the row a reader checks
first, so it must be consistent with the four sections above.

| Member | Principal contributions (all four milestones) | Overall share |
|--------|-----------------------------------------------|--------------:|
| Christian Reyes | Scoreboard, constrained-random stimulus and fill/drain modes, initial verification plan, findings, and documentation cleanup. | 50% |
| Ansley Pennywitt | Initial repository setup, driver and monitor, testbench integration, functional coverage, corner-case testing, coverage report, and file organization. | 50% |

**The three things this team did that we would each defend in an interview:**

1.
2. Added constrained-random tests and functional coverage to exercise different FIFO states and combinations of reads and writes.
3.

## Non-code contributions

Real work that leaves a thin git trace — and is graded all the same. Cite the
artifact where one exists.

| Member | Contribution | Where it shows |
|--------|--------------|----------------|
| Christian Reyes | Wrote the first version of the verification plan and later cleaned up the format. | vplan.md commits: 4279865, 6e43376 |
| Christian Reyes | Updated the team contribution record and wrote the mutation findings. | CONTRIBUTIONS.md FINDINGS.md commits: d7369bd, 1b847ed |

## AI assistance

AI was used to help with code organization, reviewing the coverage model, and writing parts of the documentation. The specific uses, who verified the work, and the results are recorded in ai_log.md

---

## Attestation

- [ ] Every claim above can be traced to the repo history.
- [ ] This file was updated at each milestone, not reconstructed at the end.
- [ ] Every member has read this file and agrees it is accurate.
- [ ] Each member has separately submitted their **confidential individual peer
      eval** — teammates' main contributions, an equity judgment, one sentence
      of evidence each — outside this repo, by the M4 deadline.

