from cqc.pythonLib import CQCConnection, qubit
import random
import time

import argparse

N = 20

def main():
    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob", N.to_bytes((N.bit_length() + 7) // 8, byteorder='big'))
        key = []
        bases = []
        for i in range(N):
            bit = random.randint(0,1)
            key.append(bit)
            basis = random.randint(0,1) 
            bases.append(basis)
            q = qubit(Alice)
            if bit == 1:
                q.X()
            if basis == 1:
                q.H()
            Alice.sendQubit(q, "Bob")
    
        print("Alice bases : {}".format(bases))
        print("Alice key : {}".format(key))

        bob_bases = []
        for i in range(N):
            bob_bases.append(int.from_bytes(Alice.recvClassical(), byteorder="big"))
    
        for x in bases:
            Alice.sendClassical("Bob", x.to_bytes(1, byteorder="big"))
            time.sleep(0.01)        

        sifted_key = []

        for i in range(N):
            if bob_bases[i] == bases[i]:
                sifted_key.append(key[i])

        print("Alice's sifted key : {}".format(sifted_key))
        exit()


