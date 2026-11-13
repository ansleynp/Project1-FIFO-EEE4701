"""Project 1 Constrained-Random Verification of a Synchronous FIFO
"""
import random

import cocotb
import vsc
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

from models.fifo_model import FifoModel

from transactions import FifoTxn, WIDTH, DEPTH

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
    occupancy_counts = [0] * (DEPTH + 1)

    # Generate 600 constrained-random transactions
    for i in range(600):

        # Tell the generator the current FIFO count
        count = scoreboard.model.count
        occupancy_counts[count] += 1
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
    dut._log.info("OCCUPANCY COUNTS (before each randomized transaction):")
    for occupancy, cycles in enumerate(occupancy_counts):
        dut._log.info(f"Occupancy {occupancy}: {cycles}")

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

@cocotb.test()
async def test_fifo_corner_cases(dut):
    # Check boundary transitions, data patterns, pointer wraps, and live resets
    from driver import FifoDriver
    from monitor import FifoMonitor
    from scoreboard import FifoScoreboard

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    driver = FifoDriver(dut)
    monitor = FifoMonitor(dut)
    scoreboard = FifoScoreboard(WIDTH, DEPTH)

    await driver.reset()
    scoreboard.reset()

    async def step(wr=0, rd=0, data=0):
        # Always observe and check the same clock edge.
        task = cocotb.start_soon(monitor.observe_cycle())
        await driver.drive(wr_en=wr, rd_en=rd, wr_data=data)
        sample = await task
        scoreboard.check(sample)
        return sample

    patterns = [0x00, 0xFF, 0xAA, 0x55, 0x01, 0xFE, 0x80, 0x7F]

    # Fill the FIFO with distinctive data and attempt an overflow.
    for i in range(DEPTH):
        await step(wr=1, data=patterns[i % len(patterns)])
    assert scoreboard.model.full
    await step(wr=1, data=0x5A)          # Full: write must be ignored
    await step(wr=1, rd=1, data=0xA5)   # Full: read accepted, write ignored
    await step(wr=1, rd=1, data=0x33)   # Part-full: both accepted

    # Drain, attempt underflow, then write+read at empty.
    for _ in range(DEPTH - 1):
        await step(rd=1)
    assert scoreboard.model.empty
    await step(rd=1)                   # Empty: read ignored
    await step(wr=1, rd=1, data=0xFF)  # Empty: write accepted, read ignored
    await step(rd=1)
    assert scoreboard.model.empty

    # Force both pointers to wrap repeatedly, with FIFO ordering checked.
    for i in range(DEPTH * 3):
        await step(wr=1, data=patterns[i % len(patterns)])
        await step(rd=1)

    # Keep one element queued while both read and write are accepted.
    await step(wr=1, data=0x55)
    for i in range(DEPTH * 3):
        await step(wr=1, rd=1, data=patterns[i % len(patterns)])
    await step(rd=1)
    assert scoreboard.model.empty

    # Reset a partially occupied FIFO while a write is requested.
    for data in [0x12, 0x34, 0x56]:
        await step(wr=1, data=data)
    dut.rst_n.value = 0
    await step(wr=1, data=0xA5)
    assert scoreboard.model.empty
    dut.rst_n.value = 1

    # Check fresh data after reset; no previous entries should reappear.
    for data in [0x00, 0xFF, 0xAA, 0x55]:
        await step(wr=1, data=data)
    for _ in range(4):
        await step(rd=1)
    assert scoreboard.model.empty

    # Also test reset while completely full with both enables asserted.
    for i in range(DEPTH):
        await step(wr=1, data=patterns[i % len(patterns)])
    assert scoreboard.model.full
    dut.rst_n.value = 0
    await step(wr=1, rd=1, data=0x5A)
    assert scoreboard.model.empty
    dut.rst_n.value = 1
    await step(wr=1, data=0xE7)
    await step(rd=1)
    assert scoreboard.model.empty

    dut._log.info(
        f"Corner-case test passed {scoreboard.cycles_checked} cycles"
    )