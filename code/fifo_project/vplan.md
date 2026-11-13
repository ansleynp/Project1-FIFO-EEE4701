# Verification plan — Project 1 Constrained-Random Verification of a Synchronous FIFO

**Author: Ansley Pennywitt, Christian Reyes** **Spec version: fifo.md** **Date: 11/12/26**

## 1. Scope

**In scope:**  We will test the provided FIFO to make sure it follows the specification. We will check reset, reading and writing data, reading and writing at the same time, full and empty conditions, the FIFO count, data ordering, and pointer wraparound. We will use the FIFO's default settings. Our testbench will have a driver, monitor, and scoreboard. We will use directed tests, constrained-random tests, functional coverage, and mutation testing to see whether the FIFO works correctly and whether our tests can catch mistakes.

**Out of scope:** We will not check the value of rd_data when the FIFO is empty, because the specification only says the data is valid when the FIFO is not empty. We also will not check the contents of the FIFO's internal memory after reset. The project handout mentions an almost_full signal and an optional first-word fall-through (FWFT) mode. The provided FIFO does not have an almost_full signal, and FWFT is always enabled, so there is no mode to switch on or off. We will still check that rd_data shows the oldest value when the FIFO contains data.

**Assumptions about the environment:** TThe testbench will provide the clock and inputs to the FIFO. We will assume the inputs are valid 0 or 1 values and are stable before each rising clock edge. Each test will start with a reset so the FIFO begins empty. We will also send read and write requests when the FIFO is full or empty, because the specification explains what should happen in those cases.

## 2. Feature list

One row per behavior the spec requires. `Req` cites a line or section of the
spec — if you cannot cite one, that is a spec gap and it belongs in section 5.

| ID | Feature | Req | Priority | How it is verified |
|----|---------|-----|----------|--------------------|
| F1 | Reset | Behavior 1 | H | Use directed tests to make sure reset clears the count and sets the full and empty flags correctly, even if a read or write is requested. |
| F2 | Writing data | Behavior 2 | H | Use random and directed writes with different data values and different FIFO counts. |
| F3 | Reading data | Behavior 3 | H | Use random and directed reads to make sure valid data can be removed from the FIFO correctly. |
| F4 | Reading and writing together | Behavior 4; Corner cases | H | Request a read and write at the same time, including when the FIFO is full or empty, and check which requests are accepted. |
| F5 | Full and empty flags | Behavior 5 | H | Check that full is set only when the FIFO is full and empty is set only when it contains no data. |
| F6 | FIFO count | Ports; Behaviors 1, 4–5 | H | Check that the count increases after a valid write, decreases after a valid read, and stays correct during other operations. |
| F7 | Writing while full and reading while empty | Behaviors 2–3; Corner cases | H | Try writing when full and reading when empty to make sure those requests are ignored without changing the stored data. |
| F8 | Data order and FWFT | Ports; Behaviors 3 and 6 | H | Use a reference queue to check that data comes out in the same order it went in and that rd_data shows the oldest stored value. |
| F9 | Pointer wraparound | Corner cases | H | Perform enough reads and writes to make the pointers wrap around, then check that the data is still in the correct order. |


## 3. Coverage model

Coverpoints and their bins. A cross earns its place only if the interaction is
where a bug would hide — say which bug.

| ID | Coverpoint | Bins | Why these bins |
|----|-----------|------|----------------|
| C1 | FIFO count | Empty (0), near-empty (1), partial (2–6), near-full (7), full (8) | Makes sure we test the FIFO at different fill levels, especially near empty and full. |
| C2 | Read/write requests | Neither, write only, read only, both | Makes sure we try every combination of the read and write inputs. |
| C3 | Reset | Reset active, reset inactive | Makes sure we include both reset and normal operation. |
| C4 | Pointer wraparound | No wrap, write pointer wraps, read pointer wraps | Makes sure we reach cases where the pointers return to the start. |
| C5 | Write data | Zero, maximum value, other values | Makes sure we test different kinds of data, including the smallest and largest values. |
| C6 | Write enable | Off, on | Lets us track whether a write was requested during reset. |

**Crosses**

| ID | Cross | The interaction it is aimed at |
|----|-------|-------------------------------|
| X1 | FIFO count × read/write requests | We want to try all four request combinations at each fill level. This may catch problems when the FIFO is full, empty, or almost at either limit. |
| X2 | Reset × write enable | We want to test writes both with and without reset. In particular, a write during reset should not change the FIFO's reset result. This also covers the project's Security & Trust example. |

**Illegal / ignore bins:** We will not exclude reads while empty or writes while full, because the FIFO specification describes how to handle them. The normal count and operation coverage will be collected when reset is inactive. Reset and write-enable coverage will be collected during both reset and normal operation. We will not check the output data when the FIFO is empty because its value is not guaranteed. We do not plan to exclude any other read/write combinations.

## 4. Test matrix

Every feature maps to at least one test; every test traces back to a feature.
An untraceable test is a test nobody can defend.

| Test | Features | Kind | Pass criterion |
|------|----------|------|----------------|
| T1 — Reset | F1, F5, F6 | Directed | Reset clears the count, makes `empty` true, and makes `full` false, even when a read or write is requested. |
| T2 — Reading and writing | F2, F3, F6, F8 | CRV and directed | Valid reads and writes update the count correctly, and data stays in the right order. |
| T3 — Read and write together | F4, F6, F8 | CRV and directed | When both requests are allowed, both happen and the count stays the same. Boundary cases also follow the specification. |
| T4 — Count and flags | F5, F6 | CRV | The count stays within the FIFO's limits, and the full and empty flags match the count. |
| T5 — Full FIFO | F4, F5, F7 | CRV and directed | A write while full is ignored. A read is still allowed, including when both inputs are on. |
| T6 — Empty FIFO | F4, F5, F7 | CRV and directed | A read while empty is ignored. A write is still allowed, including when both inputs are on. |
| T7 — Data order and pointer wraparound | F8, F9 | CRV and directed | Data remains in the correct order after many reads and writes, including pointer wraparound. |
| T8 — Write request during reset | F1 | Directed and coverage | A write during reset does not add data, and the reset/write combination is recorded by coverage. |

**Planned constrained-random testing:** We will use three types of random traffic: one that favors writing, one that favors reading, and one that mixes both. In the write-heavy part, writes will have a 9-to-1 weight over no write, while reads will be less likely. In the read-heavy part, we will do the opposite. In the mixed part, we will favor writing when the FIFO is almost empty and reading when it is almost full. We will also give zero, maximum, and other data values different weights so all three types are tested. These weights guide the random test; they do not guarantee exact percentages in a run.

We plan to use seed 1 for a run of 600 random transactions, changing traffic type every 25 transactions. Using a fixed seed will let us repeat the same test, and we will record the seed and the command used. The scoreboard will compare the FIFO's outputs to a reference queue after each operation. If coverage shows that a case is missing, we will adjust the random constraints or add a directed test to reach it.

## 5. Risk and spec ambiguity

| # | Ambiguity or risk | Where in the spec | How I resolved it | Residual |
|---|-------------------|-------------------|-------------------|----------|
| 1 | The handout mentions almost_full and optional FWFT, but they do not match the provided FIFO interface. | Project handout; FIFO specification | Follow the provided FIFO specification. We will test the FWFT behavior that is built into the FIFO and will not expect an almost_full output. | We may need to ask the instructor if these handout differences matter. |
| 2 | The output data is not guaranteed to be valid when the FIFO is empty. | Ports | Only compare rd_data when the FIFO contains data. | We will not check what the output shows while empty. |
| 3 | The testbench could check signals too early or too late. | Clock and reset behavior | Apply inputs before the rising clock edge and check the outputs after they update. | Timing problems in the testbench could cause false failures or missed bugs. |
| 4 | Random tests might not reach full, empty, or pointer-wraparound cases often enough. | Corner cases | Use different random traffic patterns, check coverage, and add directed tests if needed. | A few specific cases may still be missed. |
| 5 | The FIFO's internal read and write pointers are not outputs. | FIFO interface; Corner cases | Track successful reads and writes to estimate when each pointer should wrap around. | We will be checking the expected wraparound rather than looking at the internal pointers directly. |
| 6 | Repeating one random sequence might miss bugs that other sequences would catch. | Constrained-random testing | Keep a seed so the test is repeatable and use mutation testing to see what kinds of errors the tests catch. | Some mutants may still survive. |

## 6. Closure criteria

State the numbers *before* you start, so closure is a measurement and not a
negotiation.

- Functional coverage target: **100%** of the model in section 3
- Mutation target: **90%** on the hidden pool
- Assertions: We currently plan to use a functional coverpoint rather than SystemVerilog assertions for the required Security & Trust condition. If assertions are added, we will also check that their triggering conditions are exercised.
- What I will report as **not verified**: Any unresolved coverage gaps, surviving mutants, untested parameter configurations, or behaviors not defined by the provided FIFO specification.
