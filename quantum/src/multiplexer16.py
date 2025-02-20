from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit_aer.noise import NoiseModel, errors
from qiskit_aer.noise.errors import thermal_relaxation_error
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

# **1️⃣ Quantum Circuit Diagram (Multiplexer 16:1)**
qc = QuantumCircuit(20, 1)  # 16 data + 4 select qubits + 1 output
simulator = AerSimulator()

# Input state preparation (Example: Set specific D inputs to 1)
qc.x(0)   # D0 = 1
qc.x(3)   # D3 = 1
qc.x(7)   # D7 = 1
qc.x(12)  # D12 = 1

# Select lines (S0, S1, S2, S3) - Example: Select D10 (S3 S2 S1 S0 = 1010)
qc.x(17)  # S1 = 1
qc.x(19)  # S3 = 1

# Quantum Multiplexer Logic (Controlled selection)
qc.ccx(16, 17, 0)   # If S0 and S1 = 1, D1 overwrites D0
qc.ccx(16, 18, 2)   # If S0 and S2 = 1, D3 overwrites D2
qc.ccx(17, 18, 4)   # If S1 and S2 = 1, D5 overwrites D4
qc.ccx(16, 17, 6)   # If S0 and S1 = 1, D7 overwrites D6
qc.ccx(18, 19, 8)   # If S2 and S3 = 1, D9 overwrites D8
qc.ccx(16, 19, 10)  # If S0 and S3 = 1, D11 overwrites D10
qc.ccx(17, 19, 12)  # If S1 and S3 = 1, D13 overwrites D12
qc.ccx(18, 19, 14)  # If S2 and S3 = 1, D15 overwrites D14

# Measure the final output
qc.measure(0, 0)

# **Figure 1: Quantum Circuit Diagram**
plt.figure(figsize=(10, 5))
qc.draw('mpl')
plt.title("Figure 1: Quantum Circuit Diagram (16:1 Multiplexer)")
plt.show(block=True)

# **2️⃣ Ideal Simulation (Aer Simulator)**
compiled_circuit = transpile(qc, simulator)
job = simulator.run(compiled_circuit, shots=1024)
result = job.result()
counts_ideal = result.get_counts()

# **Figure 2: Ideal Simulation Histogram**
plt.figure(figsize=(10, 5))
plot_histogram(counts_ideal, title="Figure 2: Ideal Simulation (No Noise)", bar_labels=True)
plt.show(block=True)

# **3️⃣ Simulate with Noise (Error Probability Analysis)**
noise_model = NoiseModel()

# ✅ Apply stronger noise model
thermal_error = thermal_relaxation_error(t1=1e3, t2=2e3, time=0.1)
depolarizing_error = errors.depolarizing_error(0.2, 1)

# Apply noise to single-qubit gates
noise_model.add_all_qubit_quantum_error(thermal_error, ['u1', 'u2', 'u3'])
noise_model.add_all_qubit_quantum_error(depolarizing_error, ['u1', 'u2', 'u3'])

# Apply noise to CNOT gates (higher probability of error)
cnot_error = errors.depolarizing_error(0.3, 2)
noise_model.add_all_qubit_quantum_error(cnot_error, ['cx'])

# Simulate noisy circuit
noisy_simulator = AerSimulator(noise_model=noise_model)
job_noisy = noisy_simulator.run(compiled_circuit, shots=1024)
result_noisy = job_noisy.result()
counts_noisy = result_noisy.get_counts()

# **Figure 3: Noisy Simulation Histogram**
plt.figure(figsize=(10, 5))
plot_histogram(counts_noisy, title="Figure 3: Noisy Simulation (Error Effects in Aer Simulator)", bar_labels=True)
plt.show(block=True)

# **4️⃣ Run on Real IBM Quantum Hardware Using Sampler**
print("\n🚀 Running on IBM Quantum Hardware...")
service = QiskitRuntimeService()
backend = service.backend("ibm_sherbrooke")  # ✅ Choose an available IBM backend

# ✅ Use Sampler primitive instead of backend.run()
sampler = Sampler()  # Corrected: No 'backend' argument

try:
    job_real = sampler.run(compiled_circuit, backend=backend)  # ✅ Pass backend in run()
    result_real = job_real.result()
    counts_real = result_real.quasi_dists[0].binary_probabilities()

    print("\n✅ IBM Quantum Execution Completed Successfully!")
    print("\n🔍 Debug: IBM Quantum Measurement Data:", counts_real)

    # **Figure 4: Real Quantum Hardware Results**
    plt.figure(figsize=(12, 6))
    plot_histogram(counts_real, title="Figure 4: Real Quantum Hardware Results (IBM Machine)", bar_labels=True)
    plt.show(block=True)

    # **5️⃣ Noise Mitigation (Compare Noisy vs. Real Execution)**
    plt.figure(figsize=(12, 6))
    plot_histogram([counts_noisy, counts_real], title="Figure 5: Noise Mitigation on Quantum Multiplexer", legend=["Noisy Simulation", "IBM Quantum"])
    plt.show(block=True)

except Exception as e:
    print("\n❌ Error: IBM Quantum Execution Failed!")
    print("🔍 Debug Info:", e)