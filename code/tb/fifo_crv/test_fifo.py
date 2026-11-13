"""Project 1 Code
"""
import random

import cocotb
import vsc
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

from models.fifo_model import FifoModel

WIDTH = 8
DEPTH = 8
MASK = (1 << WIDTH) - 1


@vsc.randobj
class FifoTxn:
    def __init__(self, width=WIDTH):
        self.wr_en = vsc.rand_bit_t(1)
        self.rd_en = vsc.rand_bit_t(1)
        self.wr_data = vsc.rand_bit_t(width)

    # TODO: add a non-random `count` field and constraints that bias wr_en/rd_en
    # toward the boundaries (write hard when nearly empty, read hard when nearly
    # full) and force frequent simultaneous read+write. Uniform random rarely
    # fills or drains an 8-deep FIFO.


@cocotb.test()
async def test_crv(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    model = FifoModel(WIDTH, DEPTH)

    # reset
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.wr_data.value = 0
    dut.rst_n.value = 0
    for _ in range(3):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    model.reset()
    await FallingEdge(dut.clk)

    random.seed(1)
    txn = FifoTxn()
    for _ in range(40):                      # TODO: far too short to fill/drain
        txn.randomize()
        wr, rd, data = int(txn.wr_en), int(txn.rd_en), int(txn.wr_data)
        dut.wr_en.value = wr
        dut.rd_en.value = rd
        dut.wr_data.value = data
        model.step(wr, data, rd)
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        # weak scoreboard: only the count is compared to the model
        assert int(dut.count.value) == model.count, \
            f"count {int(dut.count.value)} != model {model.count}"
        # TODO: also check full, empty, and rd_data (the FWFT head) every cycle.
        await FallingEdge(dut.clk)

@cocotb.test()
async def test_driver_directed(dut):
    from driver import FifoDriver

    # Start the clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    driver = FifoDriver(dut)

    # Reset the FIFO
    await driver.reset()
    assert int(dut.count.value) == 0

    # Write 42
    await driver.drive(wr_en=1, wr_data=42)
    assert int(dut.count.value) == 1
    assert int(dut.rd_data.value) == 42

    # Read the value
    await driver.drive(rd_en=1)
    assert int(dut.count.value) == 0

    # Return to idle
    await driver.drive()

    dut._log.info("FIFO driver directed test passed")

@cocotb.test()
async def test_monitor_directed(dut):
    from driver import FifoDriver
    from monitor import FifoMonitor

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    driver = FifoDriver(dut)
    monitor = FifoMonitor(dut)

    await driver.reset()

    # Observe a write operation
    write_task = cocotb.start_soon(monitor.observe_cycle())

    await driver.drive(wr_en=1, wr_data=42)
    write_sample = await write_task

    assert write_sample["wr_en"] == 1
    assert write_sample["wr_data"] == 42
    assert write_sample["pre_count"] == 0
    assert write_sample["post_count"] == 1
    assert write_sample["post_rd_data"] == 42

    # Observe a read operation
    read_task = cocotb.start_soon(monitor.observe_cycle())

    await driver.drive(rd_en=1)
    read_sample = await read_task

    assert read_sample["rd_en"] == 1
    assert read_sample["pre_rd_data"] == 42
    assert read_sample["post_count"] == 0
    assert read_sample["post_empty"] == 1

    dut._log.info("FIFO monitor directed test passed")

@cocotb.test()
async def test_scoreboard_directed(dut):
    from driver import FifoDriver
    from monitor import FifoMonitor
    from scoreboard import FifoScoreboard

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    driver = FifoDriver(dut)
    monitor = FifoMonitor(dut)
    scoreboard = FifoScoreboard(WIDTH, DEPTH)

    # Reset the FIFO and reference model
    await driver.reset()
    scoreboard.reset()

    # Basic transactions to test scoreboard integration
    transactions = [
        (1, 0, 42),   # Write 42
        (1, 0, 99),   # Write 99
        (1, 1, 17),   # Read and write simultaneously
        (0, 1, 0),    # Read
        (0, 1, 0),    # Read
        (1, 1, 55),   # Read/write while empty
        (0, 1, 0),    # Read
        (0, 0, 0),    # Idle
    ]

    for wr, rd, data in transactions:
        # Start observing the next clock cycle
        monitor_task = cocotb.start_soon(
            monitor.observe_cycle()
        )

        # Apply the requested transaction
        await driver.drive(
            wr_en=wr,
            rd_en=rd,
            wr_data=data,
        )

        # Get the monitor's observations
        sample = await monitor_task

        # Check the observations against the reference model
        scoreboard.check(sample)

    dut._log.info(
        f"FIFO scoreboard passed "
        f"{scoreboard.cycles_checked} cycles"
    )