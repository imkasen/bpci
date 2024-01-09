"""
解释器
"""
import operator
from typing import Any

from .compiler import Bytecode

BINOPS_TO_OPERATOR = {
    "**": operator.pow,
    "%": operator.mod,
    "/": operator.truediv,
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,
}


class Stack:
    """
    栈
    """

    def __init__(self) -> None:
        self.stack: list[int] = []

    def push(self, item: int) -> None:
        """
        入栈操作
        """
        self.stack.append(item)

    def pop(self) -> int:
        """
        出栈
        """
        return self.stack.pop()

    def peek(self) -> int:
        """
        查看栈顶元素
        """
        return self.stack[-1]

    def __repr__(self) -> str:
        return f"Stack({self.stack})"


class Interpreter:
    """
    解释器
    """

    def __init__(self, bytecode: list[Bytecode]) -> None:
        self.stack = Stack()
        self.bytecode: list[Bytecode] = bytecode
        self.ptr: int = 0
        self.last_value_popped: Any = None

    def interpret(self) -> None:
        """
        解释字节码列表
        """
        for bc in self.bytecode:
            bc_name: str = bc.type.value
            interpret_method = getattr(self, f"interpret_{bc_name}", None)
            if interpret_method is None:
                raise RuntimeError(f"Can't interpret {bc_name}.")
            interpret_method(bc)

        print("Done!")
        # print(self.stack)
        print(self.last_value_popped)

    def interpret_push(self, bc: Bytecode) -> None:
        """
        解释入栈
        """
        self.stack.push(bc.value)

    def interpret_pop(self, bc: Bytecode) -> None:
        """
        解释弹出
        """
        self.last_value_popped = self.stack.pop()

    def interpret_binop(self, bc: Bytecode) -> None:
        """
        解释二元运算
        """
        right: int = self.stack.pop()
        left: int = self.stack.pop()
        op = BINOPS_TO_OPERATOR.get(bc.value, None)
        if op is not None:
            result = op(left, right)
        else:
            raise RuntimeError(f"Unknown operator {bc.value}.")
        self.stack.push(result)

    def interpret_unaryop(self, bc: Bytecode) -> None:
        """
        解释一元运算
        """
        result: int = self.stack.pop()
        if bc.value == "+":
            pass
        elif bc.value == "-":
            result = -result
        else:
            raise RuntimeError(f"Unknown operator {bc.value}.")
        self.stack.push(result)


if __name__ == "__main__":
    import sys

    from python.compiler import Compiler
    from python.parser import BinOp, Parser
    from python.tokenizer import Tokenizer

    code: str = sys.argv[1]
    tokens = list(Tokenizer(code))
    tree: BinOp = Parser(tokens).parse()
    byte_code = list(Compiler(tree).compile())
    Interpreter(byte_code).interpret()
