from node import Node

class Bob(Node):
    def __init__(self):
        return super().__init__("Bob")

    def main(self):
        self.set_size(self.recv_classical_integer())
        self.recv_qubits()
        self.send_bases("Alice")
        self.send_bases("Eve")
        self.remote_bases = self.recv_bases()
        self.compare_bases()

if __name__ == "__main__":
    bob = Bob()
    bob.main()
    print(bob)

