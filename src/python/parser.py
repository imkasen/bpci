"""
解析器
"""
from dataclasses import dataclass

from python.tokenizer import Token, TokenType


@dataclass
class TreeNode:
    """
    树节点
    """

    # pass


@dataclass
class Expr(TreeNode):
    """
    表达式节点
    """

    # pass


@dataclass
class BinOp(Expr):
    """
    二进制运算
    """

    op: str
    left: Expr
    right: Expr


@dataclass
class Int(Expr):
    """
    整数运算
    """

    value: int


@dataclass
class Float(Expr):
    """
    浮点数运算
    """

    value: float


def print_ast(tree: TreeNode, depth: int = 0) -> None:
    """
    打印抽象语法树
    """
    indent: str = "    " * depth
    node_name: str = tree.__class__.__name__
    match tree:  # 结构模式匹配从 Python 3.10 引入
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

    program := computation
    computation := number ( (PLUS | MINUS) number )*
    number := INT | FLOAT
    """

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.next_token_index: int = 0
        """Points to the next token to be consumed."""

    def eat(self, expected_token_type: TokenType) -> Token:
        """Returns the next token if it is of the expected type.

        If the next token is not of the expected type, this raises an error.
        """
        next_token: Token = self.tokens[self.next_token_index]
        self.next_token_index += 1
        if next_token.type != expected_token_type:
            raise RuntimeError(f"Expected {expected_token_type}, ate {next_token!r}.")
        return next_token

    def peek(self, skip: int = 0) -> TokenType | None:
        """Checks the type of an upcoming token without consuming it."""
        peek_at: int = self.next_token_index + skip
        return self.tokens[peek_at].type if peek_at < len(self.tokens) else None

    def parse_number(self) -> Int | Float:
        """Parses an integer or a float."""
        if self.peek() == TokenType.INT:
            return Int(self.eat(TokenType.INT).value)
        return Float(self.eat(TokenType.FLOAT).value)

    def parse_computation(self) -> Expr:
        """Parses a computation."""
        result: Expr
        result = self.parse_number()

        while (next_token_type := self.peek()) in {TokenType.PLUS, TokenType.MINUS}:
            op: str = "+" if next_token_type == TokenType.PLUS else "-"
            self.eat(next_token_type)
            right: Expr = self.parse_number()
            result = BinOp(op, result, right)

        return result

    def parse(self) -> Expr:
        """Parses the program.

        program := computation EOF
        """
        computation: Expr = self.parse_computation()
        self.eat(TokenType.EOF)
        return computation


if __name__ == "__main__":
    from python.tokenizer import Tokenizer

    CODE = "3 + 5 - 7 + 1.2 + 2.4 - 3.6"
    parser = Parser(list(Tokenizer(CODE)))
    print(parser.parse())
