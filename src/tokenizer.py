"""
分词器
"""
from dataclasses import dataclass
from enum import StrEnum, auto
from string import digits
from sys import version_info
from typing import Any, Generator

# StrEnum 从 Python 3.11 开始引入
assert version_info.major == 3 and version_info.minor >= 11


class TokenType(StrEnum):
    """
    标记类型

    :param StrEnum: 继承自 StrEnum，Python 3.11 引入
    """

    INT = auto()
    PLUS = auto()
    MINUS = auto()
    EOF = auto()


@dataclass
class Token:
    """
    标记
    """

    type: TokenType
    value: Any = None


class Tokenizer:
    """
    分词器类
    """

    def __init__(self, code: str) -> None:
        self.code: str = code
        self.ptr: int = 0

    def next_token(self) -> Token:
        """
        获取下一个标记

        :raises RuntimeError: 当获取的标记不是 +、- 或数字时抛出错误
        :return: Token 类型
        """
        while self.ptr < len(self.code) and self.code[self.ptr] == " ":
            self.ptr += 1

        if self.ptr == len(self.code):
            return Token(TokenType.EOF)

        char: str = self.code[self.ptr]
        self.ptr += 1
        if char == "+":
            return Token(TokenType.PLUS)
        if char == "-":
            return Token(TokenType.MINUS)
        if char in digits:
            return Token(TokenType.INT, int(char))
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
