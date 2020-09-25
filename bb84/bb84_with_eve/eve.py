import random
from node import Node
import argparse

class Eve(Node):
    def __init__(self, p):
        self.p = p
        return super().__init__("Eve")

    def recv_qubits_and_strategy(self, to):
        for i in range(self.N):
            q = self.conn.recvQubit()
            print(i)
            if random.random() < self.p:
                basis = random.randint(0,1)
                self.bases.append(basis)
                if basis == 1:
                    q.H()
                outcome = q.measure()
                self.raw_key.append(outcome)
                q2 = self.encode_qubit(outcome, basis)
                self.conn.sendQubit(q2, to)
            else:
                self.conn.sendQubit(q, to)
                self.raw_key.append("X")

    def compare_bases(self):
        for i in range(self.N):
            if self.bases_1[i] == self.bases_2[i]:
                self.sifted_key.append(self.raw_key[i])


    def main(self):
        self.set_size(self.recv_classical_integer())
        print(self.N)
        self.recv_qubits_and_strategy("Bob")
        self.bases_1 = self.recv_bases()
        self.bases_2 = self.recv_bases()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start Eve.')
    parser.add_argument('p', metavar='p', type=float, help='Eve strategy (probability to measure and resend)')
    args = parser.parse_args()
    eve = Eve(args.p)
    eve.main()
    print(eve)
    print(eve.bases_1)
    print(eve.bases_2)

