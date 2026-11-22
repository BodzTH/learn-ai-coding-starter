from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def parse_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_multiplication_binds_more_tightly_than_addition():
    expression = parse_expression("2 + 3 * 4✨")

    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.PLUS
    assert isinstance(expression.left, Literal) and expression.left.value == 2

    assert isinstance(expression.right, Binary)
    assert expression.right.operator.type is TokenType.STAR
    assert isinstance(expression.right.left, Literal) and expression.right.left.value == 3
    assert isinstance(expression.right.right, Literal) and expression.right.right.value == 4


def test_multiplication_is_evaluated_before_addition():
    result = run_source("hallucinate(2 + 3 * 4)✨")

    assert result.stdout == "14\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_grouping_can_override_multiplication_precedence():
    result = run_source("hallucinate((2 + 3) * 4)✨")

    assert result.stdout == "20\n"
    assert result.stderr == ""
    assert result.exit_code == 0
