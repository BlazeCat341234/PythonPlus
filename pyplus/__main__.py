
from pyplus.compiler import Compiler
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("No source path provided.")
    print("Usage: python3 -m pyplus <source path>")
    sys.exit(1)

source_path = Path(sys.argv[1])

try:
    source = source_path.read_text(encoding="utf-8")
except OSError as error:
    print(f"Could not read source file: {error}")
    sys.exit(1)

compiler = Compiler()
python_code = compiler.compile(source)

output_path = Path("generated/output.py")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(python_code, encoding="utf-8")

print()
print("Generated Python:")
print("-----------------")
print(python_code)
print()

print("Result:")
print("-------")
exec(python_code)
