"""
编译器
"""
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any, Generator

from .parser import BinOp, ExprStatement, Float, Int, Program, TreeNode, UnaryOp


class BytecodeType(StrEnum):
    """
    字节码类型
    """

    BINOP = auto()
    UNARYOP = auto()
    PUSH = auto()
    POP = auto()

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


# type 需要 Python 3.12 以上版本支持
# assert version_info.major == 3 and version_info.minor >= 12
# type BytecodeGenerator = Generator[Bytecode, None, None]


class Compiler:
    """
    编译器类
    """

    def __init__(self, tree: TreeNode) -> None:
        self.tree: TreeNode = tree

    def compile(self) -> Generator[Bytecode, None, None]:
        """
        编译方法
        """
        yield from self._compile(self.tree)

    def _compile(self, tree: TreeNode) -> Generator[Bytecode, None, None]:
        """
        访问者模式编译方法
        """
        node_name: str = tree.__class__.__name__
        compile_method: Any | None = getattr(self, f"compile_{node_name}", None)
        if compile_method is None:
            raise RuntimeError(f"Can't compile {node_name}.")
        yield from compile_method(tree)

    def compile_Program(self, program: Program) -> Generator[Bytecode, None, None]:  # pylint: disable=C0103
        """
        编译程序
        """
        for statement in program.statements:
            yield from self._compile(statement)

    def compile_ExprStatement(  # pylint: disable=C0103
        self, expression: ExprStatement
    ) -> Generator[Bytecode, None, None]:
        """
        编译表达式
        """
        yield from self._compile(expression.expr)
        yield Bytecode(BytecodeType.POP)

    def compile_UnaryOp(self, tree: UnaryOp) -> Generator[Bytecode, None, None]:  # pylint: disable=C0103
        """
        编译一元运算符
        """
        yield from self._compile(tree.value)
        yield Bytecode(BytecodeType.UNARYOP, tree.op)

    def compile_BinOp(self, tree: BinOp) -> Generator[Bytecode, None, None]:  # pylint: disable=C0103
        """
        编译二元运算符
        """
        yield from self._compile(tree.left)
        yield from self._compile(tree.right)
        yield Bytecode(BytecodeType.BINOP, tree.op)

    def compile_Int(self, tree: Int) -> Generator[Bytecode, None, None]:  # pylint: disable=C0103
        """
        编译整数
        """
        yield Bytecode(BytecodeType.PUSH, tree.value)

    def compile_Float(self, tree: Float) -> Generator[Bytecode, None, None]:  # pylint: disable=C0103
        """
        编译浮点数
        """
        yield Bytecode(BytecodeType.PUSH, tree.value)


if __name__ == "__main__":
    from python.parser import Parser
    from python.tokenizer import Tokenizer

    compiler = Compiler(Parser(list(Tokenizer("3 + 5 - 7 + 1.2 + 2.4 - 3.6"))).parse())
    for bc in compiler.compile():
        print(bc)
