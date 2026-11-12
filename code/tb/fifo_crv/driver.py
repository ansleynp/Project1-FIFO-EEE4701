"""FIFO Driver"""

from cocotb.triggers import RisingEdge, FallingEdge, Timer

class FifoDriver:
    def __init__(self, dut):
        self.dut = dut

    async def reset(self):
        # Initialize FIFO inputs and assert reset
        self.dut.rst_n.value = 0
        self.dut.wr_en.value = 0
        self.dut.rd_en.value = 0
        self.dut.wr_data.value = 0

        # Hold reset for three rising clock edges
        for _ in range(3):
            await RisingEdge(self.dut.clk)
            await Timer(1, units="ns")

        # Release reset on a falling edge
        await FallingEdge(self.dut.clk)
        self.dut.rst_n.value = 1

    async def drive(self, wr_en=0, rd_en=0, wr_data=0):
        # Apply inputs before the next rising edge
        await FallingEdge(self.dut.clk)

        self.dut.wr_en.value = wr_en
        self.dut.rd_en.value = rd_en
        self.dut.wr_data.value = wr_data

        # Wait for the FIFO to process the operation
        await RisingEdge(self.dut.clk)
        await Timer(1, units="ns")