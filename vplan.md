# Verification plan — Project 1 Constrained-Random Verification of a Synchronous FIFO

**Author: Ansley Pennywitt, Christian Reyes** **Spec version: fifo.md** **Date: 11/12/26**

> A vplan is an argument that "done" is definable before you write tests. Every
> row here should be something you could defend in a signoff meeting. Rows you
> cannot defend are the honest content of the Risk section, not omissions.

## 1. Scope

**In scope:** This project will verify the provided synchronous FIFO against its specification. Testing will cover reset behavior, read and write operations, simultaneous reads and writes, full and empty conditions, FIFO count, data ordering, and pointer wraparound. We will use a cocotb testbench with constrained-random stimulus, functional coverage, and mutation testing to check these behaviors.

**Out of scope:** We will not verify the value of rd_data when the FIFO is empty, since the specification only guarantees valid data when the FIFO is not empty. We will also not verify the contents of the internal memory after reset, since the specification only defines the FIFO's reset behavior through its occupancy and status flags. The project handout also mentions an almost_full signal and an optional FWFT mode, but neither is supported by the provided FIFO design.

**Assumptions about the environment:** The testbench will provide the clock and input signals to the FIFO. We will assume the inputs have defined binary values and are stable when sampled at the rising clock edge. Each test will begin with a reset so the FIFO starts in a known state. We will still test read and write requests at the full and empty boundaries, since the specification defines how the FIFO should handle them.

## 2. Feature list

One row per behavior the spec requires. `Req` cites a line or section of the
spec — if you cannot cite one, that is a spec gap and it belongs in section 5.

| ID | Feature | Req | Priority | How it is verified |
|----|---------|-----|----------|--------------------|
| F1 | Reset behavior | Behavior 1 | H | Directed test to check that reset clears count and status flags, including when read or write is requested |
| F2 | Write operations | Behavior 2 | H | CRV to test writes with different data values and FIFO occupancy levels |
| F3 | Read operations | Behavior 3 | H | CRV to test reads at different occupancy levels |
| F4 | Simultaneous read/write | Behavior 4 | H | CRV to test both operations together and check that count remains unchanged when both are accepted |
| F5 | Full and empty flags | Behavior 5 | H | CRV to check that full and empty match the FIFO count |
| F6 | FIFO count | Ports; Behaviors 4–5 | H | CRV to check count changes after accepted reads and writes |
| F7 | Overflow and underflow | Behaviors 2–3 | H | CRV to test writes while full and reads while empty, including simultaneous requests |
| F8 | Data ordering and FWFT | Ports; Behaviors 3 and 6 | H | CRV to check that data is read in the same order it was written and that rd_data shows the oldest value |
| F9 | Pointer wraparound | Corner cases | H | CRV with enough read and write operations to exercise pointer wraparound while checking data ordering |
| F10 | Parameterization | Parameters | M | Simulation with selected WIDTH and DEPTH configurations to verify operation beyond the default settings |

## 3. Coverage model

Coverpoints and their bins. A cross earns its place only if the interaction is
where a bug would hide — say which bug.

| ID | Coverpoint | Bins | Why these bins |
|----|-----------|------|----------------|
| C1 | FIFO occupancy | Empty (0), near-empty (1), partial (2–6), near-full (7), full (8) | Checks that testing reaches different FIFO occupancy levels, especially the full and empty boundaries. |
| C2 | Read/write operations | Idle, write only, read only, simultaneous read/write | Ensures that all four combinations of read and write requests are exercised. |
| C3 | Reset | Asserted, deasserted | Checks that testing includes both reset and normal FIFO operation. |
| C4 | Pointer wraparound | No wraparound, write pointer wraparound, read pointer wraparound | Ensures that reads and writes continue to work when the pointers return to the beginning of memory. |
| C5 | Write data values | Zero, maximum value, other values | Checks that different data values are written into the FIFO, including boundary values for the configured data width. |

**Crosses**

| ID | Cross | The interaction it is aimed at |
|----|-------|-------------------------------|
| X1 | FIFO occupancy × read/write operations | Checks how read and write requests behave at different occupancy levels. This can reveal bugs involving writes while full, reads while empty, and simultaneous operations at the boundaries. |
| X2 | Reset × write enable | Checks that write requests during reset are exercised. This can reveal bugs where a write is incorrectly accepted while reset is asserted. |

**Illegal / ignore bins:** The FIFO specification defines the behavior of writes while full and reads while empty, so these conditions will not be excluded from coverage. Normal occupancy and operation coverage will only be sampled when reset is inactive, since reset takes priority over read and write requests. The value of rd_data when the FIFO is empty will not be checked because the specification does not guarantee valid data in that condition. No additional read/write combinations are identified as illegal by the specification.

## 4. Test matrix

Every feature maps to at least one test; every test traces back to a feature.
An untraceable test is a test nobody can defend.

| Test | Features | Kind | Pass criterion |
|------|----------|------|----------------|
| T1 — Reset | F1, F5, F6 | Directed | Reset clears the FIFO count and sets the full and empty flags correctly. Read and write requests during reset do not change the reset result. |
| T2 — Read and write operations | F2, F3, F6, F8 | CRV | Accepted writes and reads update the count correctly, and data remains in the correct order. |
| T3 — Simultaneous read/write | F4, F6, F8 | CRV | Both operations succeed when the FIFO is neither full nor empty, and the count remains unchanged. |
| T4 — Count and status flags | F5, F6 | CRV | The count remains within the FIFO's capacity, and full and empty are asserted at the correct occupancy levels. |
| T5 — Full boundary | F4, F5, F7 | CRV | Writes are ignored when full, while valid reads are accepted, including simultaneous read/write requests. |
| T6 — Empty boundary | F4, F5, F7 | CRV | Reads are ignored when empty, while valid writes are accepted, including simultaneous read/write requests. |
| T7 — Data ordering and pointer wraparound | F8, F9 | CRV | Data remains in the correct FIFO order through repeated reads and writes, including when both the read and write pointers wrap around. |
| T8 — Parameter configurations | F10 | Simulation | The FIFO operates correctly with the selected WIDTH and DEPTH configurations. |
| T9 — Reset with write request | F1 | Directed / coverage | A write request during reset is exercised and recorded, and the reset behavior matches the specification. |

## 5. Risk and spec ambiguity

| # | Ambiguity or risk | Where in the spec | How I resolved it | Residual |
|---|-------------------|-------------------|-------------------|----------|
| 1 | The project instructions mention an almost_full signal and optional FWFT operation, but neither is configurable in the provided design. | Project handout; FIFO Parameters and Ports | We will verify the features defined in the provided FIFO specification and document the differences. | Instructor clarification may be needed. |
| 2 | rd_data is only guaranteed to be valid when the FIFO is not empty. | Ports | The scoreboard will only check rd_data when valid data is present. | The value of rd_data while empty will not be verified. |
| 3 | The driver and monitor could sample signals at the wrong time, causing incorrect test results. | Ports; Behavior | Inputs will be applied before rising clock edges, and outputs will be sampled after they settle. | Timing will need to be checked during integration and longer regressions. |
| 4 | Random transactions may not reach full, empty, or pointer-wraparound conditions often enough. | Corner cases | Constraints will be adjusted based on the coverage results to reach missing scenarios. | Coverage gaps may remain and will need to be documented. |
| 5 | The specification does not identify every supported WIDTH and DEPTH configuration. | Parameters | Testing will begin with the default configuration, and additional configurations will be selected by the team. | Behavior outside the tested configurations will not be verified. |
| 6 | The FIFO's internal read and write pointers are not exposed as output signals. | FIFO interface and corner cases | Track accepted reads and writes to determine when pointer wraparound should occur. | The coverage model will rely on tracking pointer movement rather than directly observing the internal pointers.

## 6. Closure criteria

State the numbers *before* you start, so closure is a measurement and not a
negotiation.

- Functional coverage target: **100%** of the model in section 3
- Mutation target: **90%** on the hidden pool
- Assertions: We currently plan to use a functional coverpoint rather than SystemVerilog assertions for the required Security & Trust condition. If assertions are added, we will also check that their triggering conditions are exercised.
- What I will report as **not verified**: Any unresolved coverage gaps, surviving mutants, untested parameter configurations, or behaviors not defined by the provided FIFO specification.
