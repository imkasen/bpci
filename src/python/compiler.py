"""
编译器
"""
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any, Generator

from python.parser import BinOp, Float, Int


class BytecodeType(StrEnum):
    """
    字节码类型

    :param StrEnum: 继承自 StrEnum，Python 3.11 引入
    """

    BINOP = auto()
    PUSH = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


@dataclass
class Bytecode:
    """
    字节码类
    """

    type: BytecodeType
    value: Any = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type!r}, {self.value!r})"


class Compiler:
    """
    编译器类
    """

    def __init__(self, tree: BinOp) -> None:
        self.tree: BinOp = tree

    def compile(self) -> Generator[Bytecode, None, None]:
        """
        编译方法

        :yield: 返回字节码类
        """
        left: Int | Float = self.tree.left
        yield Bytecode(BytecodeType.PUSH, left.value)

        right: Int | Float = self.tree.right
        yield Bytecode(BytecodeType.PUSH, right.value)

        yield Bytecode(BytecodeType.BINOP, self.tree.op)


if __name__ == "__main__":
    from python.parser import Parser
    from python.tokenizer import Tokenizer

    compiler = Compiler(Parser(list(Tokenizer("3 + 5"))).parse())
    for bc in compiler.compile():
        print(bc)
