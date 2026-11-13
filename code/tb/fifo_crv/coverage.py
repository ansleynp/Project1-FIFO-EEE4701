"""Functional coverage for the FIFO verification plan"""
"""Records occupancy, read/write operations, reset, pointer wraparound,
and write data during testing. Tracks coverage bins and crosses to show
which FIFO scenerios were exercised or missed."""

from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_section, coverage_db

# C1, C2, X1: occupancy, operation, and their combinations
@coverage_section(
    CoverPoint("top.occ", xf=lambda occ, op: occ,
               bins=["empty", "near_empty", "partial", "near_full", "full"]),
    CoverPoint("top.op", xf=lambda occ, op: op,
               bins=["idle", "write", "read", "both"]),
    CoverCross("top.occ_x_op", items=["top.occ", "top.op"])
)
def traffic(occ, op):
    pass


# C3, X2: reset and write enable, including a write during reset
@coverage_section(
    CoverPoint("top.reset", xf=lambda rst, wr: rst, bins=[0, 1]),
    CoverPoint("top.wr", xf=lambda rst, wr: wr, bins=[0, 1]),
    CoverCross("top.reset_x_wr", items=["top.reset", "top.wr"])
)
def reset_write(rst, wr):
    pass


# C4: expected pointer wraparound
@CoverPoint("top.wrap", xf=lambda kind: kind, bins=["none", "write", "read"])
def wrap(kind):
    pass


# C5: data values of accepted writes
@CoverPoint("top.data", xf=lambda kind: kind, bins=["zero", "max", "other"])
def data_value(kind):
    pass


class FifoCoverage:
    def __init__(self, width=8, depth=8):
        self.depth = depth
        self.max_data = (1 << width) - 1
        self.write_ptr = 0
        self.read_ptr = 0

    def reset(self):
        # Matches the reset performed by driver.reset().
        self.write_ptr = 0
        self.read_ptr = 0
        reset_write(0, 0)

    def sample(self, sample):
        # Every observation is sampled after the scoreboard checks it.
        wr = sample["wr_en"]
        rd = sample["rd_en"]
        if sample["rst_n"] == 0:
            self.write_ptr = 0
            self.read_ptr = 0
            reset_write(0, wr)
            return

        reset_write(1, wr)
        count = sample["pre_count"]
        if count == 0:
            occ = "empty"
        elif count == self.depth:
            occ = "full"
        elif count == 1:
            occ = "near_empty"
        elif count == self.depth - 1:
            occ = "near_full"
        else:
            occ = "partial"

        if wr and rd:
            op = "both"
        elif wr:
            op = "write"
        elif rd:
            op = "read"
        else:
            op = "idle"
        traffic(occ, op)

        # Only accepted operations move the expected pointers.
        write_ok = wr and count < self.depth
        read_ok = rd and count > 0
        write_wrap = write_ok and self.write_ptr == self.depth - 1
        read_wrap = read_ok and self.read_ptr == self.depth - 1
        if write_wrap:
            wrap("write")
        if read_wrap:
            wrap("read")
        if not write_wrap and not read_wrap:
            wrap("none")

        if write_ok:
            value = sample["wr_data"]
            if value == 0:
                data_value("zero")
            elif value == self.max_data:
                data_value("max")
            else:
                data_value("other")
            self.write_ptr = (self.write_ptr + 1) % self.depth
        if read_ok:
            self.read_ptr = (self.read_ptr + 1) % self.depth

    def report(self, log):
        log.info("FUNCTIONAL COVERAGE RESULTS")
        for label, name in [
            ("C1 Occupancy", "top.occ"),
            ("C2 Operations", "top.op"),
            ("C3 Reset", "top.reset"),
            ("C4 Pointer wrap", "top.wrap"),
            ("C5 Write data", "top.data"),
            ("X1 Occupancy x operation", "top.occ_x_op"),
            ("X2 Reset x write", "top.reset_x_wr"),
        ]:
            entry = coverage_db[name]
            missing = [str(bin_name) for bin_name, hits in
                       entry.detailed_coverage.items() if hits == 0]
            log.info(f"{label}: {entry.cover_percentage:.1f}%")
            if missing:
                log.info(f"  Missing: {', '.join(missing)}")