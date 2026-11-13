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
| C1 |           |      |  |

**Crosses**

| ID | Cross | The interaction it is aimed at |
|----|-------|-------------------------------|
| X1 |       |  |

**Illegal / ignore bins:** <what is excluded and on what authority in the spec>

## 4. Test matrix

Every feature maps to at least one test; every test traces back to a feature.
An untraceable test is a test nobody can defend.

| Test | Features | Kind | Pass criterion |
|------|----------|------|----------------|
|      |          | directed / random / assertion / formal | |

## 5. Risk and spec ambiguity

| # | Ambiguity or risk | Where in the spec | How I resolved it | Residual |
|---|-------------------|-------------------|-------------------|----------|
| 1 |                   |                   | asked / assumed / tested both | |

## 6. Closure criteria

State the numbers *before* you start, so closure is a measurement and not a
negotiation.

- Functional coverage target: **__%** of the model in section 3
- Mutation target: **__/__** on the hidden pool
- Assertions: every property paired with a passing `cover` (no vacuous passes)
- What I will report as **not verified**:
