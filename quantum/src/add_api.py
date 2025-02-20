from qiskit_ibm_runtime import QiskitRuntimeService

# Replace "YOUR_NEW_API_TOKEN" with the new API key from IBM Quantum Dashboard
QiskitRuntimeService.save_account(channel="ibm_quantum", token="a246f66e60a5d48863150889053b64bc6c47cca967eaa56853094c6b847006e0ffcfebbd5cb6a1d5d94fffac91d6a5a90eb6c250a601a4343cdc34ccca72ec39", overwrite=True)

print("✅ New IBM Quantum API Token has been saved successfully!")
