from .tokens import TokenType
from .ast_nodes import (
    NumberNode,
    StringNode,
    VariableNode,
    BinaryOperationNode,
    AssignmentNode,
    PrintNode,
    ProgramNode,
    GroupNode,
    FunctionCallNode,
    FunctionDefinitionNode,
    ReturnNode,
    BooleanNode,
    IfNode,
)
import sys


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def check(self, type, msg):
        tok = self.current()
        if type != tok.type:
            print(f"Error on line {tok.line} column {tok.column}: {msg}")
            fuck()
            sys.exit(1)

    def parse(self):
        statements = []

        while self.current().type != TokenType.EOF:
            statements.append(
                self.parse_statement()
            )

        return ProgramNode(statements)

    def parse_body(self):
        body = []

        while self.current().type != TokenType.END:
            body.append(self.parse_statement())

        self.advance()  # consume END
        return body

    def parse_statement(self):
        token = self.current()
        self.advance()

        match token.type:
            case TokenType.PRINT : return PrintNode(self.parse_primary())
            case TokenType.RETURN: return ReturnNode(self.parse_expression())
            case TokenType.FUNCTION: return self.parse_function()

            case TokenType.IF:
                condition = self.parse_expression()
                body = self.parse_body()

                return IfNode(
                    condition,
                    body
                )

            case TokenType.IDENTIFIER:
                name = token.value

                match self.current().type:
                    case TokenType.ASSIGN:
                        self.advance()

                        value = self.parse_expression()

                        return AssignmentNode(
                            name,
                            value
                        )

                    case TokenType.LPAREN:
                        self.position -= 1
                        return self.parse_primary()

            case _:
                raise Exception(
                    f"Unknown statement: {token}"
                )

    def parse_function(self):
        name = self.current().value
        self.advance()

        parameters = []
        self.check(TokenType.LPAREN, "Expected '(' after function name")
        self.advance()

        while self.current().type != TokenType.RPAREN:
            self.check(TokenType.IDENTIFIER, "Expected parameter name")

            parameters.append(self.current().value)
            self.advance()

            if self.current().type != TokenType.COMMA:
                break
            self.advance()

        self.check(TokenType.RPAREN, "Expected ')'")
        self.advance()

        body = self.parse_body()

        return FunctionDefinitionNode(
            name,
            parameters,
            body
        )


    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_addition()

        while self.current().type in (
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator = self.current()
            self.advance()
            right = self.parse_addition()

            left = BinaryOperationNode(
                left,
                operator.value,
                right
            )

        return left

    def parse_addition(self):
        left = self.parse_multiplication()

        while self.current().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self.current()
            self.advance()
            right = self.parse_multiplication()

            left = BinaryOperationNode(
                left,
                operator.value,
                right
            )

        return left


    def parse_multiplication(self):
        left = self.parse_primary()

        while self.current().type in (
            TokenType.STAR,
            TokenType.SLASH,
        ):
            operator = self.current()
            self.advance()
            right = self.parse_primary()

            left = BinaryOperationNode(
                left,
                operator.value,
                right
            )

        return left


    def parse_primary(self):
        token = self.current()
        self.advance()

        match token.type:
            case TokenType.LPAREN:
                expression = self.parse_expression()

                self.check(TokenType.RPAREN, "Expected ')'")
                self.advance()

                return GroupNode(expression)


            case TokenType.STRING: return StringNode(token.value)
            case TokenType.NUMBER: return NumberNode(token.value)
            case TokenType.TRUE:   return BooleanNode(True)
            case TokenType.FALSE:  return BooleanNode(False)

            case TokenType.IDENTIFIER if self.current().type == TokenType.LPAREN:
                self.advance()

                arguments = []

                while self.current().type != TokenType.RPAREN:
                    arguments.append(self.parse_expression())                    

                    if self.current().type != TokenType.COMMA:
                        break
                    self.advance()

                self.check(TokenType.RPAREN, "Expected ')'")
                self.advance()

                return FunctionCallNode(
                    token.value,
                    arguments
                )

            case _:
                return VariableNode(token.value)


        print(f"Error on line {token.line} column {token.column}: Unexpected token: '{token.value}'")
        sys.exit(1)


