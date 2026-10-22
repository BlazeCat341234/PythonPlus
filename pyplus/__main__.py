from pyplus.compiler import Compiler
import sys

# Updated upstream
if len(sys.argv) < 2:
    print("No source path provided.")
    print("Usage: python3 -m pyplus <source path>")
    sys.exit(1)

with open(sys.argv[1]) as f:
# =======
    with open("examples/functions.pyplus") as f:
    # Stashed changes
        source = f.read()

    compiler = Compiler()

    python_code = compiler.compile(source)

    with open("generated/output.py", "w") as f:
        f.write(python_code)

print()
print("Generated Python:")
print("-----------------")
print(python_code)
print()

print("Result:")
print("-------")
exec(python_code)
