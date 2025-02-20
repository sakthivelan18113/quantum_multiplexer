from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer 
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Create a Quantum Circuit with 3 qubits (A, B, S) and 1 classical bit for measurement
qc = QuantumCircuit(3, 1)
simulator = AerSimulator()

# Input state preparation (Optional: Set inputs |A> and |B>)
qc.h(0)  # Example: Apply Hadamard to A (creates superposition)
qc.x(1)  # Example: Set B to |1> (X gate flips |0> to |1>)

# Quantum Multiplexer using CNOT and Toffoli Gates
qc.cx(2, 0)  # Controlled-NOT with S as control, A as target
qc.ccx(2, 1, 0)  # Toffoli gate: If S=1, B overwrites A

# Measure the output (A qubit)
qc.measure(0, 0)

# Simulate the circuit
#simulator = Aer.get_backend('aer_simulator')
compiled_circuit = transpile(qc, simulator)
#qobj = assemble(compiled_circuit)
job = simulator.run(qc, shots=1024)
#result = (qc, simulator).result()
result = job.result()
counts = result.get_counts()

# Display Results
qc.draw('mpl')
plot_histogram(counts)
plt.show()