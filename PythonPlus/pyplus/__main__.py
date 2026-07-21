from pyplus.compiler import Compiler

with open("examples/hello.pyplus") as f:
    source = f.read()

compiler = Compiler()

python_code = compiler.compile(source)

with open("generated/output.py", "w") as f:
    f.write(python_code)

print("Generated Python:")
print("----------------")
print(python_code)

exec(python_code)
