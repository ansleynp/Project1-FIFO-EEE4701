"""FIFO Monitor"""
"""Captures input signals and FIFO state before each rising clock edge,
then records the updated outputs after the edge. Provides transaction 
observations for the scoredbaord to verify."""

from cocotb.triggers import RisingEdge, FallingEdge, Timer

class FifoMonitor:
    def __init__(self, dut):
        self.dut = dut

    async def observe_cycle(self):
        # Wait for the driver to apply inputs
        await FallingEdge(self.dut.clk)
        await Timer(1, units="ns")

        # Capture inputs and FIFO state before the rising edge
        before = {
            "rst_n": int(self.dut.rst_n.value),
            "wr_en": int(self.dut.wr_en.value),
            "rd_en": int(self.dut.rd_en.value),
            "wr_data": int(self.dut.wr_data.value),
            "pre_count": int(self.dut.count.value),
            "pre_full": int(self.dut.full.value),
            "pre_empty": int(self.dut.empty.value),
        }

        # Capture valid head data before the read occurs
        before["pre_rd_data"] = (
            int(self.dut.rd_data.value)
            if not before["pre_empty"] else None
        )

        # Wait for the operation to complete
        await RisingEdge(self.dut.clk)
        await Timer(1, units="ns")

        # Capture outputs after the rising edge
        after = {
            "post_count": int(self.dut.count.value),
            "post_full": int(self.dut.full.value),
            "post_empty": int(self.dut.empty.value),
        }

        after["post_rd_data"] = (
            int(self.dut.rd_data.value)
            if not after["post_empty"] else None
        )

        return {**before, **after}