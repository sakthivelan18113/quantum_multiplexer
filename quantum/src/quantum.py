from qiskit import QuantumCircuit
from qiskit_aer import Aer 
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt


# Create a quantum circuit with 3 qubits (2 data qubits and 1 control qubit)
qc = QuantumCircuit(3)
# Select the AerSimulator backend (simulator for quantum circuits)
simulator = AerSimulator()


# Initialize qubits: 
# qubit 0: Control qubit (1 bit)
# qubit 1: Data qubit 1
# qubit 2: Data qubit 2

# Apply an arbitrary state to the data qubits
qc.x(1)  # Set qubit 1 to 1 (this is our first input state)
qc.x(2)  # Set qubit 2 to 1 (this is our second input state)

# Control qubit is 0, so data qubit 2 should be selected
# Apply a CX gate with control qubit 0 and target qubit 2 (MUX control)
qc.cx(0, 2)

# Now run the quantum circuit on a simulator
simulator = Aer.get_backend('statevector_simulator')
job = simulator.run(qc, shots=1024)
#result = (qc, simulator).result()
result = job.result()
counts = result.get_counts(qc)
print(counts)
# Get the final statevector (resulting quantum state)
#statevector = result.get_statevector()

# Display the quantum circuit
qc.draw('mpl')
plt.show()
# Show the statevector
#print("Statevector: ", statevector)
