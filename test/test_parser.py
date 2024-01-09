"""
解析器测试
"""
import pytest

from python.parser import BinOp, ExprStatement, Float, Int, Parser, Program, UnaryOp
from python.tokenizer import Token, Tokenizer, TokenType


def test_parsing_addition():
    """
    测试加法
    """
    tokens = [
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "+",
        Int(3),
        Int(5),
    )


def test_parsing_subtraction():
    """
    测试减法
    """
    tokens = [
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 2),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "-",
        Int(5),
        Int(2),
    )


def test_parsing_addition_with_floats():
    """
    测试浮点数加法
    """
    tokens = [
        Token(TokenType.FLOAT, 0.5),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "+",
        Float(0.5),
        Int(5),
    )


def test_parsing_subtraction_with_floats():
    """
    测试浮点数减法
    """
    tokens = [
        Token(TokenType.FLOAT, 5.0),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT, 0.2),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "-",
        Float(5.0),
        Float(0.2),
    )


def test_parsing_single_integer():
    """
    测试解析单个整数
    """
    tokens = [
        Token(TokenType.INT, 3),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == Int(3)


def test_parsing_single_float():
    """
    测试解析单个浮点数
    """
    tokens = [
        Token(TokenType.FLOAT, 3.0),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == Float(3.0)


def test_parsing_addition_then_subtraction():
    """
    测试解析加法和减法
    """
    tokens = [
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT, 0.2),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "-",
        BinOp(
            "+",
            Int(3),
            Int(5),
        ),
        Float(0.2),
    )


def test_parsing_subtraction_then_addition():
    """
    测试解析减法和加法
    """
    tokens = [
        Token(TokenType.INT, 3),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 5),
        Token(TokenType.PLUS),
        Token(TokenType.FLOAT, 0.2),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "+",
        BinOp(
            "-",
            Int(3),
            Int(5),
        ),
        Float(0.2),
    )


def test_parsing_many_additions_and_subtractions():
    """
    测试解析多个加法和减法
    """
    # 3 + 5 - 7 + 1.2 + 2.4 - 3.6
    tokens = [
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 7),
        Token(TokenType.PLUS),
        Token(TokenType.FLOAT, 1.2),
        Token(TokenType.PLUS),
        Token(TokenType.FLOAT, 2.4),
        Token(TokenType.MINUS),
        Token(TokenType.FLOAT, 3.6),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
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


def test_parsing_unary_minus():
    """
    测试一元减号运算符
    """
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.INT, 3),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == UnaryOp("-", Int(3))


def test_parsing_unary_plus():
    """
    测试一元加号运算符
    """
    tokens = [
        Token(TokenType.PLUS),
        Token(TokenType.FLOAT, 3.0),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == UnaryOp("+", Float(3))


def test_parsing_unary_operators():
    """
    测试一元运算符
    """
    # --++3.5 - 2
    tokens = [
        Token(TokenType.MINUS),
        Token(TokenType.MINUS),
        Token(TokenType.PLUS),
        Token(TokenType.PLUS),
        Token(TokenType.FLOAT, 3.5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 2),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "-",
        UnaryOp(
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
        ),
        Int(2),
    )


def test_parsing_parentheses():
    """
    测试解析小括号
    """
    # 1 + ( 2 + 3 )
    tokens = [
        Token(TokenType.INT, 1),
        Token(TokenType.PLUS),
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 3),
        Token(TokenType.RPAREN),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "+",
        Int(1),
        BinOp(
            "+",
            Int(2),
            Int(3),
        ),
    )


def test_parsing_parentheses_around_single_number():
    """
    测试解析单个数字周围的小括号
    """
    # ( ( ( 1 ) ) ) + ( 2 + ( 3 ) )
    tokens = [
        Token(TokenType.LPAREN),
        Token(TokenType.LPAREN),
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 1),
        Token(TokenType.RPAREN),
        Token(TokenType.RPAREN),
        Token(TokenType.RPAREN),
        Token(TokenType.PLUS),
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 3),
        Token(TokenType.RPAREN),
        Token(TokenType.RPAREN),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "+",
        Int(1),
        BinOp(
            "+",
            Int(2),
            Int(3),
        ),
    )


@pytest.mark.parametrize(
    "code",
    [
        "(1",
        "()",
        ") 1 + 2",
        "1 + 2)",
        "1 (+) 2",
        "1 + )2(",
    ],
)
def test_unbalanced_parentheses(code: str):
    """
    测试不成对的小括号
    """
    tokens = list(Tokenizer(code))
    with pytest.raises(RuntimeError):
        Parser(tokens).parse()


def test_parsing_more_operators():
    """
    测试 *、/、%、** 运算符
    """
    # "1 % -2 ** -3 / 5 * 2 + 2 ** 3"
    tokens = [
        Token(TokenType.INT, 1),
        Token(TokenType.MOD),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 2),
        Token(TokenType.EXP),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 3),
        Token(TokenType.DIV),
        Token(TokenType.INT, 5),
        Token(TokenType.MUL),
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 2),
        Token(TokenType.EXP),
        Token(TokenType.INT, 3),
    ]
    tree = Parser(tokens).parse_computation()
    assert tree == BinOp(
        "+",
        BinOp(
            "*",
            BinOp(
                "/",
                BinOp(
                    "%",
                    Int(1),
                    UnaryOp(
                        "-",
                        BinOp(
                            "**",
                            Int(2),
                            UnaryOp(
                                "-",
                                Int(3),
                            ),
                        ),
                    ),
                ),
                Int(5),
            ),
            Int(2),
        ),
        BinOp(
            "**",
            Int(2),
            Int(3),
        ),
    )


def test_parsing_multiple_statements():
    """
    测试解析多语句
    """
    code = "1 % -2\n5 ** -3 / 5\n1 * 2 + 2 ** 3\n"
    tree = Parser(list(Tokenizer(code))).parse()
    assert tree == Program(
        [
            ExprStatement(
                BinOp(
                    "%",
                    Int(1),
                    UnaryOp(
                        "-",
                        Int(2),
                    ),
                ),
            ),
            ExprStatement(
                BinOp(
                    "/",
                    BinOp(
                        "**",
                        Int(5),
                        UnaryOp(
                            "-",
                            Int(3),
                        ),
                    ),
                    Int(5),
                ),
            ),
            ExprStatement(
                BinOp(
                    "+",
                    BinOp(
                        "*",
                        Int(1),
                        Int(2),
                    ),
                    BinOp(
                        "**",
                        Int(2),
                        Int(3),
                    ),
                ),
            ),
        ]
    )
