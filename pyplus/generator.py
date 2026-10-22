from .ast_nodes import *
import sys

class Generator:

    @classmethod
    def generate(cls, node, level=0):
        ind = "\t" * level

        match node:
            case ProgramNode(stmts):
                output = []

                for stmt in stmts:
                    output.append(
                        cls.generate(stmt, level)
                    )

                return "\n".join(output)


            # Literals
            case BooleanNode (value): return str(value)
            case NumberNode  (value): return str(value)
            case StringNode  (value): return f'"{value}"'
            case VariableNode(name):  return name

            # Expressions
            case GroupNode(expression):
                return f"({cls.generate(node.expression)})"

            case BinaryOperationNode(lhs, op, rhs):
                left = cls.generate(lhs)
                right = cls.generate(rhs)
                return f"({left} {op} {right})"

            case FunctionCallNode(name, args):
                arguments = ", ".join(
                    cls.generate(arg)
                    for arg in args
                )

                return f"{ind}{name}({arguments})"

            # Statements
            case AssignmentNode(name, value):
                return f"{ind}{name} = {cls.generate(value)}"

            case PrintNode(value):
                return f"{ind}print({cls.generate(value)})"

            case ReturnNode(value):
                return f"{ind}return {cls.generate(value)}"

            # Function definitions
            case IfNode(cond, body):
                lines = [
                    f"{ind}if {cls.generate(cond)}:"
                ] + [
                    cls.generate(stmt, level + 1)
                    for stmt in body
                ]

                return "\n".join(lines)

            case FunctionDefinitionNode(name, param, body):
                parameters = ", ".join(param)

                lines = [
                    f"{ind}def {name}({parameters}):"
                ]

                if len(body) == 0:
                    lines += [f"{ind}\tpass"]

                for statement in body:
                    lines += [cls.generate(
                        statement,
                        level + 1
                    )]

                return "\n".join(lines)

        print(f"Unknown node: {node}")
        sys.exit(1)

