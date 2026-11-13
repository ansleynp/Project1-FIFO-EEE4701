"""Project 1 Constrained-Random Verification of a Synchronous FIFO
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

        # These are provided by the test, not randomized
        self.count = vsc.uint32_t(0)
        self.mode = vsc.uint8_t(0)

    @vsc.constraint
    def operation_constraint(self):

        # Mode 0: Mostly writes to fill the FIFO
        with vsc.if_then(self.mode == 0):
            vsc.dist(self.wr_en, [
                vsc.weight(0, 1),
                vsc.weight(1, 9)
            ])
            vsc.dist(self.rd_en, [
                vsc.weight(0, 9),
                vsc.weight(1, 1)
            ])

        # Mode 1: Mostly reads to empty the FIFO
        with vsc.else_if(self.mode == 1):
            vsc.dist(self.wr_en, [
                vsc.weight(0, 9),
                vsc.weight(1, 1)
            ])
            vsc.dist(self.rd_en, [
                vsc.weight(0, 1),
                vsc.weight(1, 9)
            ])

        # Mode 2: Mixed read/write traffic
        with vsc.else_then:

            # When nearly empty, favor writes
            with vsc.if_then(self.count <= 1):
                vsc.dist(self.wr_en, [
                    vsc.weight(0, 3),
                    vsc.weight(1, 7)
                ])
                vsc.dist(self.rd_en, [
                    vsc.weight(0, 6),
                    vsc.weight(1, 4)
                ])

            # When nearly full, favor reads
            with vsc.else_if(self.count >= DEPTH - 1):
                vsc.dist(self.wr_en, [
                    vsc.weight(0, 6),
                    vsc.weight(1, 4)
                ])
                vsc.dist(self.rd_en, [
                    vsc.weight(0, 3),
                    vsc.weight(1, 7)
                ])

            # Otherwise, favor simultaneous requests
            with vsc.else_then:
                vsc.dist(self.wr_en, [
                    vsc.weight(0, 3),
                    vsc.weight(1, 7)
                ])
                vsc.dist(self.rd_en, [
                    vsc.weight(0, 3),
                    vsc.weight(1, 7)
                ])

@cocotb.test()
async def test_crv(dut):
    from driver import FifoDriver
    from monitor import FifoMonitor
    from scoreboard import FifoScoreboard
    from coverage import FifoCoverage

    # Keep the random test reproducible
    random.seed(1)

    # Start the clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Set up verification components
    driver = FifoDriver(dut)
    monitor = FifoMonitor(dut)
    scoreboard = FifoScoreboard(WIDTH, DEPTH)
    coverage = FifoCoverage(WIDTH, DEPTH)

    await driver.reset()
    scoreboard.reset()
    coverage.reset()

    txn = FifoTxn()

    # Track important cases reached during the test
    full_cycles = 0
    empty_cycles = 0
    simultaneous = 0
    write_while_full = 0
    read_while_empty = 0
    both_while_full = 0
    both_while_empty = 0

    # Generate 600 constrained-random transactions
    for i in range(600):

        # Tell the generator the current FIFO count
        count = scoreboard.model.count
        txn.count = count

        # Switch traffic type every 25 transactions
        txn.mode = (i // 25) % 3

        # Generate a random transaction
        txn.randomize()

        wr = int(txn.wr_en)
        rd = int(txn.rd_en)
        data = int(txn.wr_data)

        # Record which situations occurred
        if count == DEPTH:
            full_cycles += 1
            if wr:
                write_while_full += 1
            if wr and rd:
                both_while_full += 1

        if count == 0:
            empty_cycles += 1
            if rd:
                read_while_empty += 1
            if wr and rd:
                both_while_empty += 1

        if wr and rd:
            simultaneous += 1
        
        # Monitor the next transaction
        monitor_task = cocotb.start_soon(
            monitor.observe_cycle()
        )

        # Apply the randomized inputs
        await driver.drive(
            wr_en=wr,
            rd_en=rd,
            wr_data=data
        )

        # Get the observed values
        sample = await monitor_task

        # Check the FIFO against the reference model
        scoreboard.check(sample)

        coverage.sample(sample)

    # Test a write request during reset
    dut.rst_n.value = 0

    monitor_task = cocotb.start_soon(
        monitor.observe_cycle()
    )

    await driver.drive(
        wr_en=1,
        rd_en=0,
        wr_data=55
    )

    sample = await monitor_task
    scoreboard.check(sample)
    coverage.sample(sample)

    # Display functional coverage results
    coverage.report(dut._log)

    # Print a summary of the test
    dut._log.info("CRV TEST RESULTS")
    dut._log.info(f"Cycles checked: {scoreboard.cycles_checked}")
    dut._log.info(f"Cycles at full: {full_cycles}")
    dut._log.info(f"Cycles at empty: {empty_cycles}")
    dut._log.info(f"Simultaneous requests: {simultaneous}")
    dut._log.info(f"Writes while full: {write_while_full}")
    dut._log.info(f"Reads while empty: {read_while_empty}")
    dut._log.info(f"Both while full: {both_while_full}")
    dut._log.info(f"Both while empty: {both_while_empty}")

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