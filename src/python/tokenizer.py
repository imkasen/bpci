"""
分词器
"""
from dataclasses import dataclass
from enum import StrEnum, auto
from string import digits
from sys import version_info
from typing import Any, Generator

assert version_info.major == 3 and version_info.minor >= 11


class TokenType(StrEnum):  # StrEnum 从 Python 3.11 开始引入
    """
    标记类型
    """

    INT = auto()
    FLOAT = auto()
    PLUS = auto()
    MINUS = auto()
    EOF = auto()
    LPAREN = auto()
    RPAREN = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    EXP = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


CHARS_AS_TOKENS: dict[str, TokenType] = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "%": TokenType.MOD,
}


@dataclass
class Token:
    """
    标记
    """

    type: TokenType
    value: Any = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type!r}, {self.value!r})"


class Tokenizer:
    """
    分词器类
    """

    def __init__(self, code: str) -> None:
        self.code: str = code
        self.ptr: int = 0

    def consume_int(self) -> int:
        """Reads an integer from the source code."""
        start: int = self.ptr
        while self.ptr < len(self.code) and self.code[self.ptr] in digits:
            self.ptr += 1
        return int(self.code[start : self.ptr])

    def consume_decimal(self) -> float:
        """Reads a decimal part that starts with a . and returns it as a float."""
        start: int = self.ptr
        self.ptr += 1
        while self.ptr < len(self.code) and self.code[self.ptr] in digits:
            self.ptr += 1
        float_str: str = self.code[start : self.ptr] if self.ptr - start > 1 else ".0"
        return float(float_str)

    def peek(self, length: int = 1) -> str | None:
        """Returns the substring that will be tokenized next."""
        return self.code[self.ptr : self.ptr + length]

    def next_token(self) -> Token:
        """
        获取下一个标记
        """
        while self.ptr < len(self.code) and self.code[self.ptr] == " ":
            self.ptr += 1

        if self.ptr == len(self.code):
            return Token(TokenType.EOF)

        char: str = self.code[self.ptr]
        if self.peek(length=2) == "**":
            self.ptr += 2
            return Token(TokenType.EXP)
        if char in CHARS_AS_TOKENS:
            self.ptr += 1
            return Token(CHARS_AS_TOKENS[char])
        if char in digits:
            integer: int = self.consume_int()  # If we found a digit, consume an integer.
            # Is the integer followed by a decimal part?
            if self.ptr < len(self.code) and self.code[self.ptr] == ".":
                decimal: float = self.consume_decimal()
                return Token(TokenType.FLOAT, integer + decimal)
            return Token(TokenType.INT, integer)
        if (  # Floats start with '.', make sure we don't read a lone full stop `.`.
            char == "." and self.ptr + 1 < len(self.code) and self.code[self.ptr + 1] in digits
        ):
            decimal = self.consume_decimal()
            return Token(TokenType.FLOAT, decimal)
        raise RuntimeError(f"Can't tokenize {char!r}.")

    def __iter__(self) -> Generator[Token, None, None]:
        while (token := self.next_token()).type != TokenType.EOF:
            yield token
        yield token  # Yield the EOF token too.


if __name__ == "__main__":
    CODE = "1 + 2 + 3 + 4 - 5 - 6 + 7 - 8"
    tokenizer = Tokenizer(CODE)
    print(CODE)
    for tok in tokenizer:
        print(f"\t{tok.type}, {tok.value}")
