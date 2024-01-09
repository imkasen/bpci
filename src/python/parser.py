"""
解析器
"""
from __future__ import annotations

from dataclasses import dataclass

from .tokenizer import Token, TokenType


@dataclass
class TreeNode:
    """
    树节点
    """

    # pass


@dataclass
class Program(TreeNode):
    """
    程序节点
    """

    statements: list[Statement]


@dataclass
class Statement(TreeNode):
    """
    语句节点
    """

    # pass


@dataclass
class ExprStatement(Statement):
    """
    表达式语句节点
    """

    expr: Expr


@dataclass
class Expr(TreeNode):
    """
    表达式节点
    """

    # pass


@dataclass
class UnaryOp(Expr):
    """
    一元运算
    """

    op: str
    value: Expr


@dataclass
class BinOp(Expr):
    """
    二元运算
    """

    op: str
    left: Expr
    right: Expr


@dataclass
class Int(Expr):
    """
    整数
    """

    value: int


@dataclass
class Float(Expr):
    """
    浮点数
    """

    value: float


def print_ast(tree: TreeNode, depth: int = 0) -> None:
    """
    打印抽象语法树
    """
    indent: str = "    " * depth
    node_name: str = tree.__class__.__name__
    match tree:  # 结构模式匹配从 Python 3.10 引入
        case Program(statements):
            print(f"{indent}{node_name}([\n", end="")
            for statement in statements:
                print_ast(statement, depth + 1)
                print(",")
            print(f",\n{indent}])", end="")
        case ExprStatement(expr):
            print(f"{indent}{node_name}(\n", end="")
            print_ast(expr, depth + 1)
            print(f",\n{indent})", end="")
        case UnaryOp(op, value):
            print(f"{indent}{node_name}(\n{indent}    {op!r},")
            print_ast(value, depth + 1)
            print(f",\n{indent})", end="")
        case BinOp(op, left, right):
            print(f"{indent}{node_name}(\n{indent}    {op!r},")
            print_ast(left, depth + 1)
            print(",")
            print_ast(right, depth + 1)
            print(f",\n{indent})", end="")
        case Int(value) | Float(value):
            print(f"{indent}{node_name}({value!r})", end="")
        case _:
            raise RuntimeError(f"Can't print a node of type {node_name}")
    if depth == 0:
        print()


class Parser:
    """
    解析器类

    program := statement* EOF

    statement := expr_statement
    expr_statement := computation NEWLINE

    computation := term ( (PLUS | MINUS) term )*
    term := unary ( (MUL | DIV | MOD) unary )*
    unary := PLUS unary | MINUS unary | exponentiation
    exponentiation := atom EXP unary | atom
    atom := LPAREN computation RPAREN | number
    number := INT | FLOAT
    """

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.next_token_index: int = 0  # Points to the next token to be consumed.

    def eat(self, expected_token_type: TokenType) -> Token:
        """
        Returns the next token if it is of the expected type.

        If the next token is not of the expected type, this raises an error.
        """
        next_token: Token = self.tokens[self.next_token_index]
        self.next_token_index += 1
        if next_token.type != expected_token_type:
            raise RuntimeError(f"Expected {expected_token_type}, ate {next_token!r}.")
        return next_token

    def peek(self, skip: int = 0) -> TokenType | None:
        """
        Checks the type of an upcoming token without consuming it.
        """
        peek_at: int = self.next_token_index + skip
        return self.tokens[peek_at].type if peek_at < len(self.tokens) else None

    def parse_number(self) -> Int | Float:
        """
        Parses an integer or a float.

        number := INT | FLOAT
        """
        if self.peek() == TokenType.INT:
            return Int(self.eat(TokenType.INT).value)
        return Float(self.eat(TokenType.FLOAT).value)

    def parse_atom(self) -> Expr:
        """
        Parses a parenthesised expression or a number.

        atom := LPAREN computation RPAREN | number
        """
        if self.peek() == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result: Expr = self.parse_computation()
            self.eat(TokenType.RPAREN)
        else:
            result = self.parse_number()
        return result

    def parse_exponentiation(self) -> Expr:
        """
        Parses an exponentiation operator.

        exponentiation := atom EXP unary | atom
        """
        result: Expr = self.parse_atom()
        if self.peek() == TokenType.EXP:
            self.eat(TokenType.EXP)
            result = BinOp("**", result, self.parse_unary())
        return result

    def parse_unary(self) -> Expr:
        """
        Parses an unary operator.

        unary := PLUS unary | MINUS unary | exponentiation
        """
        if (next_token_type := self.peek()) in {TokenType.PLUS, TokenType.MINUS}:
            op: str = "+" if next_token_type == TokenType.PLUS else "-"
            self.eat(next_token_type)
            value: Expr = self.parse_unary()
            return UnaryOp(op, value)
        return self.parse_exponentiation()  # No unary operators in sight.

    def parse_term(self) -> Expr:
        """
        Parses an expression with multiplications, divisions, and modulo operations.

        term := unary ( (MUL | DIV | MOD) unary )*
        """
        result: Expr = self.parse_unary()

        TYPES_TO_OPS: dict[TokenType, str] = {  # pylint: disable=C0103
            TokenType.MUL: "*",
            TokenType.DIV: "/",
            TokenType.MOD: "%",
        }

        while (next_token_type := self.peek()) in TYPES_TO_OPS:
            op: str = TYPES_TO_OPS[next_token_type]
            self.eat(next_token_type)
            right: Expr = self.parse_unary()
            result = BinOp(op, result, right)

        return result

    def parse_computation(self) -> Expr:
        """
        Parses a computation.

        computation := term ( (PLUS | MINUS) term )*
        """
        result: Expr = self.parse_term()

        while (next_token_type := self.peek()) in {TokenType.PLUS, TokenType.MINUS}:
            op: str = "+" if next_token_type == TokenType.PLUS else "-"
            self.eat(next_token_type)
            right: Expr = self.parse_term()
            result = BinOp(op, result, right)

        return result

    def parse_expr_statement(self) -> ExprStatement:
        """
        Parses a standalone expression.

        expr_statement := computation NEWLINE
        """
        expr = ExprStatement(self.parse_computation())
        self.eat(TokenType.NEWLINE)
        return expr

    def parse_statement(self) -> Statement:
        """
        Parses a statement.

        statement := expr_statement
        """
        return self.parse_expr_statement()

    def parse(self) -> Program:
        """Parses the program."""
        program = Program([])
        while self.peek() != TokenType.EOF:
            program.statements.append(self.parse_statement())
        self.eat(TokenType.EOF)
        return program


if __name__ == "__main__":
    from .tokenizer import Tokenizer

    CODE = """1 % -2
5 ** -3 / 5
1 * 2 + 2 ** 3"""
    parser = Parser(list(Tokenizer(CODE)))
    print_ast(parser.parse())
