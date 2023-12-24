"""
编译器测试
"""
from python.compiler import Bytecode, BytecodeType, Compiler
from python.parser import BinOp, Float, Int, UnaryOp


def test_compile_addition():
    """
    测试编译加法运算
    """
    tree = BinOp(
        "+",
        Int(3),
        Int(5),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.PUSH, 5),
        Bytecode(BytecodeType.BINOP, "+"),
    ]


def test_compile_subtraction():
    """
    测试编译减法运算
    """
    tree = BinOp(
        "-",
        Int(5),
        Int(2),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 5),
        Bytecode(BytecodeType.PUSH, 2),
        Bytecode(BytecodeType.BINOP, "-"),
    ]


def test_compile_nested_additions_and_subtractions():
    """
    测试编译嵌套加减法运算
    """
    tree = BinOp(
        "-",
        BinOp(
            "+",
            BinOp(
                "+",
                BinOp(
                    "-",
                    BinOp(
                        "+",
                        Int(3),
                        Int(5),
                    ),
                    Int(7),
                ),
                Float(1.2),
            ),
            Float(2.4),
        ),
        Float(3.6),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.PUSH, 5),
        Bytecode(BytecodeType.BINOP, "+"),
        Bytecode(BytecodeType.PUSH, 7),
        Bytecode(BytecodeType.BINOP, "-"),
        Bytecode(BytecodeType.PUSH, 1.2),
        Bytecode(BytecodeType.BINOP, "+"),
        Bytecode(BytecodeType.PUSH, 2.4),
        Bytecode(BytecodeType.BINOP, "+"),
        Bytecode(BytecodeType.PUSH, 3.6),
        Bytecode(BytecodeType.BINOP, "-"),
    ]


def test_compile_unary_minus():
    """
    测试编译一元减号运算符
    """
    tree = UnaryOp("-", Int(3))
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.UNARYOP, "-"),
    ]


def test_compile_unary_plus():
    """
    测试编译一元加号运算符
    """
    tree = UnaryOp("+", Int(3))
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.UNARYOP, "+"),
    ]


def test_compile_unary_operations():
    """
    测试编译一元运算符
    """
    tree = UnaryOp(
        "-",
        UnaryOp(
            "-",
            UnaryOp(
                "+",
                UnaryOp(
                    "+",
                    Float(3.5),
                ),
            ),
        ),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 3.5),
        Bytecode(BytecodeType.UNARYOP, "+"),
        Bytecode(BytecodeType.UNARYOP, "+"),
        Bytecode(BytecodeType.UNARYOP, "-"),
        Bytecode(BytecodeType.UNARYOP, "-"),
    ]


def test_compile_multiplication():
    """
    测试编译乘法
    """
    tree = BinOp(
        "*",
        Int(3),
        Float(3.14),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.PUSH, 3.14),
        Bytecode(BytecodeType.BINOP, "*"),
    ]


def test_compile_division():
    """
    测试编译除法
    """
    tree = BinOp(
        "/",
        Int(1),
        Int(2),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 1),
        Bytecode(BytecodeType.PUSH, 2),
        Bytecode(BytecodeType.BINOP, "/"),
    ]


def test_compile_exponentiation():
    """
    测试编译幂运算
    """
    tree = BinOp(
        "**",
        Float(0.1),
        Float(3.14),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 0.1),
        Bytecode(BytecodeType.PUSH, 3.14),
        Bytecode(BytecodeType.BINOP, "**"),
    ]


def test_compile_modulo():
    """
    测试编译取模
    """
    tree = BinOp(
        "%",
        Int(-3),
        Float(-5.6),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, -3),
        Bytecode(BytecodeType.PUSH, -5.6),
        Bytecode(BytecodeType.BINOP, "%"),
    ]
