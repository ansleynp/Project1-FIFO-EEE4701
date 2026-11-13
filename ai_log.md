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