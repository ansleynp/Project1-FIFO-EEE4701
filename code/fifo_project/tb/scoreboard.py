"""FIFO scoreboard"""
"""Uses the provided reference model to track expected FIFO behavior. 
Compares the monitor's observations with the expected count, status flags, 
and read data before and after each clock edge."""

from models.fifo_model import FifoModel

class FifoScoreboard:
    def __init__(self, width=8, depth=8):
        self.model = FifoModel(width, depth)
        self.cycles_checked = 0

    def reset(self):
        self.model.reset()
        self.cycles_checked = 0

    def _check_state(self, sample, stage):
        expected = {
            "count": self.model.count,
            "full": int(self.model.full),
            "empty": int(self.model.empty),
        }

        # Check count and status flags
        for name, value in expected.items():
            observed = sample[f"{stage}_{name}"]

            assert observed == value, (
                f"Cycle {self.cycles_checked} ({stage}): "
                f"{name} expected {value}, observed {observed}"
            )

        # Check read data only when FIFO is not empty
        if not self.model.empty:
            observed_head = sample[f"{stage}_rd_data"]

            assert observed_head == self.model.head, (
                f"Cycle {self.cycles_checked} ({stage}): "
                f"rd_data expected {self.model.head}, "
                f"observed {observed_head}"
            )

    def check(self, sample):
        self.cycles_checked += 1

        if sample["rst_n"] == 0:
            # Reset takes priority over reads and writes
            self.model.reset()
        else:
            # Check the FIFO state before the operation
            self._check_state(sample, "pre")

            # Update expected state using the requested inputs
            self.model.step(
                wr_en=sample["wr_en"],
                wr_data=sample["wr_data"],
                rd_en=sample["rd_en"],
            )

        # Check the updated FIFO state
        self._check_state(sample, "post")