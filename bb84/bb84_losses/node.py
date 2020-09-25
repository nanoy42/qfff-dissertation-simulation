import random
import time

from cqc.pythonLib import CQCConnection, qubit

TEMPLATE = """
NAME : {}
BASES : {}
KEY : {}
SIFTED KEY : {}
"""

class Node:

    def __init__(self, name):
        self.conn = CQCConnection(name)
        self.name = name
        self.N = 0
        self.bases = []
        self.raw_key = []
        self.sifted_key = []
        self.remote_bases = []

    def __del__(self):
        self.conn.__exit__(None, None, None)

    def set_size(self, N):
        self.N = N

    def send_classical_integer(self, to, integer):
        self.conn.sendClassical(to, integer.to_bytes((integer.bit_length() + 7) // 8, byteorder="big"))

    def recv_classical_integer(self):
        return int.from_bytes(self.conn.recvClassical(), byteorder="big")

    def send_bases(self, to):
        msg = b''
        for i, base in enumerate(self.bases):
            msg += base.to_bytes(1, byteorder="big")
        self.conn.sendClassical(to, msg)

    def recv_bases(self):
        res = []
        msg = self.conn.recvClassical()
        for i in range(self.N):
            res.append(msg[i])
        return res

    def compare_bases(self):
        for i in range(self.N):
            if self.bases[i] == self.remote_bases[i]:
                self.sifted_key.append(self.raw_key[i])

    def encode_qubit(self, bit, basis):
        q = qubit(self.conn)
        if bit == 1:
            q.X()
        if basis == 1:
            q.H()
        return q

    def send_qubits(self, to):
        for i in range(self.N):
            basis = random.randint(0, 1)
            bit = random.randint(0, 1)
            self.bases.append(basis)
            self.raw_key.append(bit)
            q = self.encode_qubit(bit, basis)
            self.conn.sendQubit(q, to)

    def recv_qubits(self):
        for i in range(self.N):
            basis = random.randint(0, 1)
            self.bases.append(basis)
            q = self.conn.recvQubit()
            if basis == 1:
                q.H()
            self.raw_key.append(q.measure())

    def __str__(self):
        return TEMPLATE.format(self.name, self.bases, self.raw_key, self.sifted_key)

    def main(self):
        pass