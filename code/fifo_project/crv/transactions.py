"""Constrained-random FIFO transaction and pyvsc constraints"""
import vsc

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

    @vsc.constraint
    def data_constraint(self):
        # Give zero and all-ones data a better chance of appearing
        vsc.dist(self.wr_data, [
            vsc.weight(0, 10),
            vsc.weight((1, MASK - 1), 80),
            vsc.weight(MASK, 10)
        ])