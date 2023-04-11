import pytest

from script_args_parser.helpers import split_string_by_semicolon


@pytest.mark.parametrize('input, expected_output', (
    ('', ['']),
    ('  ', ['  ']),
    ('abc', ['abc']),
    ('  abc   ', ['  abc   ']),
    (';', ['', '']),
    ('abc;xyz', ['abc', 'xyz']),
    (r'abc\;xyz', [r'abc\;xyz']),
    ('";"', ['";"']),
    (';;', ['', '', '']),
))
def test_split_string_by_semicolon(input: str, expected_output: list[str]):
    assert split_string_by_semicolon(input) == expected_output
