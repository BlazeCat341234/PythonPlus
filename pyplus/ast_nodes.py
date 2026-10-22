from dataclasses import dataclass as dc
from typing import Any


@dc
class NumberNode:
    value : Any

@dc
class StringNode:
    value : Any

@dc
class FunctionCallNode:
    name      : Any
    arguments : Any

@dc
class FunctionDefinitionNode:
    name       : Any
    parameters : Any
    body       : Any

@dc
class VariableNode:
    name : Any

@dc
class BinaryOperationNode:
    left     : Any
    operator : Any
    right    : Any

@dc
class GroupNode:
    expression : Any

@dc
class AssignmentNode:
    name  : Any
    value : Any

@dc
class IfNode:
    condition : Any
    body      : Any

@dc
class BooleanNode:
    value : Any

@dc
class ReturnNode:
    value : Any

@dc
class PrintNode:
    value : Any

@dc
class ProgramNode:
    statements : Any
