# Project 1 — FIFO Verification

**EEE 4701 — Fall 2026**  
**Team:** Ansley Pennywitt and Christian Reyes

This project verifies a synchronous FIFO using cocotb and constrained-random testing with pyvsc.

The `code/fifo_project/tb/` folder contains the driver, monitor, and scoreboard. The `code/fifo_project/crv/` folder contains the transactions, tests, and functional coverage model.

## Running the Tests

From the `code` folder, run:

```bash
just test
just mutate
```

## Results

- Functional coverage: 43/43 bins (100%)
- Released mutation tests: 8/8 found (100%)

More details are provided in `vplan.md`, `FINDINGS.md`, and `REPORT.pdf` in code/fifo_project.

**Demo video:** [(https://drive.google.com/file/d/1ch63vOX2c8s4oTzHvKewPHdQu7IE_PaK/view?usp=sharing)]