"""
测试解释器
"""

import pytest

from python.compiler import Compiler
from python.interpreter import Interpreter
from python.parser import Parser
from python.tokenizer import Tokenizer


def run_computation(code: str) -> int:
    """
    运行计算
    """
    tokens = list(Tokenizer(code))
    tree = Parser(tokens).parse()
    bytecode = list(Compiler(tree).compile())
    interpreter = Interpreter(bytecode)
    interpreter.interpret()
    return interpreter.stack.pop()


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
    assert run_computation(code) == result


@pytest.mark.parametrize(
    ["code", "result"],
    [
        ("103.6 + 5.4", 109),
        ("5.5 - 2", 3.5),
        ("1 + .2", 1.2),
        ("100.0625 - 9.5", 90.5625),
    ],
)
def test_arithmetic_with_floats(code: str, result: int):
    """
    测试浮点数运算
    """
    assert run_computation(code) == result


@pytest.mark.parametrize(
    ["code", "result"],
    [
        ("1 + 2 + 3 + 4 + 5", 15),
        ("1 - 2 - 3", -4),
        ("1 - 2 + 3 - 4 + 5 - 6", -3),
    ],
)
def test_sequences_of_additions_and_subtractions(code: str, result: int):
    """
    测试连续加减法
    """
    assert run_computation(code) == result
