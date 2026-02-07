import os
import sys

print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

try:
    os.makedirs("logs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    print("Directories created successfully.")
except Exception as e:
    print(f"Error creating directories: {e}")

with open("test_output.txt", "w") as f:
    f.write("Test script ran successfully.\n")

print("Test script completed.")
