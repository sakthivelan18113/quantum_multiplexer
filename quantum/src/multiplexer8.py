from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a Quantum Circuit with 6 qubits (D0-D7, S0, S1, S2) and 1 classical bit for measurement
qc = QuantumCircuit(11, 1)
simulator = AerSimulator()

# Input state preparation (Setting up data inputs D0-D7)
qc.x(0)  # Set D0 = 1
qc.x(2)  # Set D2 = 1
qc.x(4)  # Set D4 = 1
qc.x(6)  # Set D6 = 1

# Select lines (S0, S1, S2) - Example: Set S2 S1 S0 = 101 (Selecting D5)
qc.x(3)  # S0 = 1
qc.x(5)  # S2 = 1

# Quantum Multiplexer using CNOT and Toffoli Gates
qc.ccx(3, 4, 0)  # If S0 and S1 = 1, D1 overwrites D0
qc.ccx(3, 5, 2)  # If S0 and S2 = 1, D3 overwrites D2
qc.ccx(4, 5, 7)  # If S1 and S2 = 1, D5 overwrites D4
qc.ccx(3, 4, 6)  # If S0, S1 = 1, D7 overwrites D6

# Measure the final output
qc.measure(0, 0)

# Simulate the circuit
compiled_circuit = transpile(qc, simulator)
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

# Display Results
qc.draw('mpl')
plot_histogram(counts)
plt.show()

