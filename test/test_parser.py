"""
解析器测试
"""
from python.parser import BinOp, Float, Int, Parser
from python.tokenizer import Token, TokenType


def test_parsing_addition():
    """
    测试加法
    """
    tokens = [
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
        Token(TokenType.EOF),
    ]
    tree = Parser(tokens).parse()
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
        Token(TokenType.EOF),
    ]
    tree = Parser(tokens).parse()
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
        Token(TokenType.EOF),
    ]
    tree = Parser(tokens).parse()
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
        Token(TokenType.EOF),
    ]
    tree = Parser(tokens).parse()
    assert tree == BinOp(
        "-",
        Float(5.0),
        Float(0.2),
    )
