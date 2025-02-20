from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_provider import IBMProvider
import matplotlib.pyplot as plt

provider = IBMProvider(token='9fd5ef868f9cf76eefa7791a4d466ef84728224667b3a1b8f44dd83f418c53567038de60573ae9e96e92538baa088f75aeb06e3a0e3f4ad5d03152ea2b20207d')

# Load your IBM Quantum account
#IBMQ.load_account()

# Define a Quantum Register with named qubits
qreg = QuantumRegister(7, name="mux")
creg = ClassicalRegister(1, name="cbit")

# Create the circuit with named registers
qc = QuantumCircuit(qreg, creg)

# Quantum Multiplexer Logic
qc.ccx(qreg[5], qreg[6], qreg[1])  # If S1=1 and S0=1, copy D to output
qc.ccx(qreg[5], qreg[6], qreg[2])  # If S1=1 and S0=0, copy C to output
qc.ccx(qreg[5], qreg[6], qreg[3])  # If S1=0 and S0=1, copy B to output
qc.ccx(qreg[5], qreg[6], qreg[4])  # If S1=0 and S0=0, copy A to output

# Controlled XOR gates to move selected input to output qubit (q[0])
qc.cx(qreg[1], qreg[0])
qc.cx(qreg[2], qreg[0])
qc.cx(qreg[3], qreg[0])
qc.cx(qreg[4], qreg[0])

# Measurement
qc.measure(qreg[0], creg[0])

# Get the least busy backend
#provider = IBMProvider(instance="ibm-q/open/main")
#backends = provider.backends()

# Find the backend with the name "ibmq_qasm_simulator"
simulator_backend = provider.get_backend('ibm_kyiv')
print(simulator_backend)
#simulator_backend = next((backend for backend in backends if backend.name() == "ibmq_qasm_simulator"), None)

# Run the job on the quantum backend
job = simulator_backend.run(qc, shots=1024)

# Get the results
result = job.result()

# Get the counts (outcome frequencies)
counts = result.get_counts(qc)

# Plot the histogram of the results
plt.bar(counts.keys(), counts.values())
plt.xlabel('Measurement Outcomes')
plt.ylabel('Frequency')
plt.title('Histogram of Quantum Circuit Measurement Results')
plt.show()