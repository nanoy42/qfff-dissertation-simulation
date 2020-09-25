import argparse
from node import Node

class Alice(Node):
    def __init__(self):
        return super().__init__("Alice")

    def main(self):
        self.send_classical_integer("Bob", self.N)
        self.send_classical_integer("Eve", self.N)
        self.send_qubits("Eve")
        self.remote_bases = self.recv_bases()
        self.send_bases("Bob")
        self.send_bases("Eve")
        self.compare_bases()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start Alice.')
    parser.add_argument('N', metavar='N', type=int, help='Number of qubits to send to Bob (please be aware of simulaqron\'s max-qubits paramater')
    args = parser.parse_args()
    N = args.N
    alice = Alice()
    alice.set_size(N)
    alice.main()
    print(alice)

