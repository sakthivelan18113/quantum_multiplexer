from qiskit_ibm_runtime import QiskitRuntimeService

try:
    service = QiskitRuntimeService()
    print("✅ API Token is working!")
    print("Available IBM Quantum backends:", service.backends())
except Exception as e:
    print("❌ API Token is still not working. Error:", e)
