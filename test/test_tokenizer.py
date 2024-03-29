"""
分词器测试
"""
import pytest

from python.tokenizer import Token, Tokenizer, TokenType


@pytest.mark.parametrize(
    ["code", "token"],
    [
        ("+", Token(TokenType.PLUS)),
        ("-", Token(TokenType.MINUS)),
        ("3", Token(TokenType.INT, 3)),
        ("61", Token(TokenType.INT, 61)),
        ("72345", Token(TokenType.INT, 72345)),
        ("9142351643", Token(TokenType.INT, 9142351643)),
        ("642357413455672", Token(TokenType.INT, 642357413455672)),
        ("1.2", Token(TokenType.FLOAT, 1.2)),
        (".12", Token(TokenType.FLOAT, 0.12)),
        ("73.", Token(TokenType.FLOAT, 73.0)),
        ("0.005", Token(TokenType.FLOAT, 0.005)),
        ("123.456", Token(TokenType.FLOAT, 123.456)),
        ("(", Token(TokenType.LPAREN)),
        (")", Token(TokenType.RPAREN)),
        ("*", Token(TokenType.MUL)),
        ("**", Token(TokenType.EXP)),
        ("/", Token(TokenType.DIV)),
        ("%", Token(TokenType.MOD)),
    ],
)
def test_tokenizer_recognises_each_token(code: str, token: Token):
    """
    单独测试每个标记

    :param code: 单个代码字符
    :param token: 对应的标记类型
    """
    assert Tokenizer(code).next_token() == token


@pytest.mark.parametrize(
    ["code", "token"],
    [
        (" 61      ", Token(TokenType.INT, 61)),
        ("    72345    ", Token(TokenType.INT, 72345)),
        ("9142351643", Token(TokenType.INT, 9142351643)),
        ("     642357413455672", Token(TokenType.INT, 642357413455672)),
    ],
)
def test_tokenizer_long_integers(code: str, token: Token):
    """
    测试较长的整数
    """
    tokens = list(Tokenizer(code))
    assert tokens == [token, Token(TokenType.NEWLINE), Token(TokenType.EOF)]


def test_tokenizer_addition():
    """
    测试 + 标记
    """
    tokens = list(Tokenizer("3 + 5"))
    assert tokens == [
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
        Token(TokenType.NEWLINE),
        Token(TokenType.EOF),
    ]


def test_tokenizer_subtraction():
    """
    测试 - 标记
    """
    tokens = list(Tokenizer("3 - 6"))
    assert tokens == [
        Token(TokenType.INT, 3),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 6),
        Token(TokenType.NEWLINE),
        Token(TokenType.EOF),
    ]


def test_tokenizer_additions_and_subtractions():
    """
    测试 + 和 - 标记
    """
    tokens = list(Tokenizer("1 + 2 + 3 + 4 - 5 - 6 + 7 - 8"))
    assert tokens == [
        Token(TokenType.INT, 1),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 4),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 6),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 7),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 8),
        Token(TokenType.NEWLINE),
        Token(TokenType.EOF),
    ]


def test_tokenizer_additions_and_subtractions_with_whitespace():
    """
    测试空格标记
    """
    tokens = list(Tokenizer("     1+       2   +3+4-5  -   6 + 7  - 8        "))
    assert tokens == [
        Token(TokenType.INT, 1),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 4),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 6),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 7),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 8),
        Token(TokenType.NEWLINE),
        Token(TokenType.EOF),
    ]


def test_tokenizer_raises_error_on_garbage():
    """
    测试未知标记
    """
    with pytest.raises(RuntimeError):
        list(Tokenizer("$"))


def test_tokenizer_lone_period_is_error():
    """
    测试单个小数点
    """
    # Make sure we don't get a float out of a single period `.`.
    with pytest.raises(RuntimeError):
        list(Tokenizer("  .  "))


def test_tokenizer_parentheses_in_code():
    """
    测试小括号
    """
    tokens = list(Tokenizer("( 1 ( 2 ) 3 ( ) 4"))
    assert tokens == [
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 1),
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 2),
        Token(TokenType.RPAREN),
        Token(TokenType.INT, 3),
        Token(TokenType.LPAREN),
        Token(TokenType.RPAREN),
        Token(TokenType.INT, 4),
        Token(TokenType.NEWLINE),
        Token(TokenType.EOF),
    ]


def test_tokenizer_distinguishes_mul_and_exp():
    """
    测试区分 * 和 **
    """
    tokens = list(Tokenizer("1 * 2 ** 3 * 4 ** 5"))
    assert tokens == [
        Token(TokenType.INT, 1),
        Token(TokenType.MUL),
        Token(TokenType.INT, 2),
        Token(TokenType.EXP),
        Token(TokenType.INT, 3),
        Token(TokenType.MUL),
        Token(TokenType.INT, 4),
        Token(TokenType.EXP),
        Token(TokenType.INT, 5),
        Token(TokenType.NEWLINE),
        Token(TokenType.EOF),
    ]


@pytest.mark.parametrize(
    "code",
    [
        ("\n\n\n1 + 2\n3 + 4\n"),  # Extras at the beginning.
        ("1 + 2\n\n\n3 + 4\n"),  # Extras in the middle.
        ("1 + 2\n3 + 4\n\n\n"),  # Extras at the end.
        ("\n\n\n1 + 2\n\n\n3 + 4\n\n\n"),  # Extras everywhere.
    ],
)
def test_tokenizer_ignores_extra_newlines(code: str):
    """
    测试忽略额外的 \n
    """
    tokens = list(Tokenizer(code))
    assert tokens == [
        Token(TokenType.INT, 1),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 2),
        Token(TokenType.NEWLINE),
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 4),
        Token(TokenType.NEWLINE),
        Token(TokenType.EOF),
    ]
