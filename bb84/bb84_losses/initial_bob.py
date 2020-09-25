from cqc.pythonLib import CQCConnection, qubit
import random
import time

with CQCConnection("Bob") as Bob:
    key = []
    bases = []
    N = int.from_bytes(Bob.recvClassical(), byteorder='big')
    for i in range(N):
        basis = random.randint(0,1)
        bases.append(basis)
        q = Bob.recvQubit()
        if basis == 1:
            q.H()
        b = q.measure()
        key.append(b)

    print("Bob basis : {}".format(bases))
    print("Bob key : {}".format(key))

    for x in bases:
        Bob.sendClassical("Alice", x.to_bytes(1, byteorder="big"))
        time.sleep(0.01)
    
    alice_bases = []
    for i in range(N):
        alice_bases.append(int.from_bytes(Bob.recvClassical(), byteorder="big"))

    sifted_key = []

    for i in range(N):
        if alice_bases[i] == bases[i]:
            sifted_key.append(key[i])

    print("Bob's sifted key : {}".format(sifted_key))
    exit()
