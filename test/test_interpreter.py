"""
测试解释器
"""

import pytest

from python.compiler import Compiler
from python.interpreter import Interpreter
from python.parser import Parser
from python.tokenizer import Tokenizer


@pytest.mark.parametrize(
    ["code", "result"],
    [
        ("3 + 5", 8),
        ("5 - 2", 3),
        ("1 + 2", 3),
        ("1 - 9", -8),
    ],
)
def test_simple_arithmetic(code: str, result: int):
    """
    测试简单的运算

    :param code: 源代码
    :param result: 结果
    """
    tokens = list(Tokenizer(code))
    tree = Parser(tokens).parse()
    bytecode = list(Compiler(tree).compile())
    interpreter = Interpreter(bytecode)
    interpreter.interpret()
    assert interpreter.stack.pop() == result
