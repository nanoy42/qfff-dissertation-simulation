import cirq

qubit = cirq.NamedQubit("q")

circuit = cirq.Circuit(
    cirq.H(qubit),
    cirq.measure(qubit, key='m')
)
print("Circuit:")
print(circuit)

# Simulate the circuit several times.
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results:")
print(result)
