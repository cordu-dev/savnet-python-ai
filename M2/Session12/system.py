import os

# Be careful, the user intent can be malicious.
# E.g. command injection.
# aa/bb/cc ; cat .env
dirs_path = input("Give me nested strucute of dirs:")

returned_value = os.system(f"mkdir -p {dirs_path}")
print(returned_value)
