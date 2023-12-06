"""
解释器
"""
from python.compiler import Bytecode, BytecodeType


class Stack:
    """
    栈
    """

    def __init__(self) -> None:
        self.stack: list[int] = []

    def push(self, item: int) -> None:
        """
        入栈操作

        :param item: 传入一个整数
        """
        self.stack.append(item)

    def pop(self) -> int:
        """
        出栈

        :return: 返回一个整数
        """
        return self.stack.pop()

    def peek(self) -> int:
        """
        查看栈顶元素

        :return: 返回整数元素的值
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

    def interpret(self) -> None:
        """
        解释字节码列表

        :raises RuntimeError: 遇到除加减运算之外的符合时抛出错误
        """
        for bc in self.bytecode:
            # Interpret this bytecode operator.
            if bc.type == BytecodeType.PUSH:
                self.stack.push(bc.value)
            elif bc.type == BytecodeType.BINOP:
                right: int | float = self.stack.pop()
                left: int | float = self.stack.pop()
                if bc.value == "+":
                    result: int | float = left + right
                elif bc.value == "-":
                    result: int | float = left - right
                else:
                    raise RuntimeError(f"Unknown operator {bc.value}.")
                self.stack.push(result)

        print("Done!")
        print(self.stack)


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
