import os

import pytest

from script_args_parser import ArgumentsParser
from script_args_parser.arguments import Argument
from tests.common_fixtures import *  # noqa: F401, F403


@pytest.fixture
def env_var_name():
    return 'UT_STRING_ENV_VALUE'


@pytest.fixture
def arguments_definition():
    return [Argument(
        name='string',
        description='String value',
        type='str',
        cli_arg='--some-string',
    )]


def test_no_value(arguments_definition):
    cli: list[str] = []
    parser = ArgumentsParser(arguments_definition, cli)
    assert parser.arguments_values['string'] is None


def test_value_empty_string(arguments_definition):
    cli: list[str] = ['--some-string', '']
    parser = ArgumentsParser(arguments_definition, cli)
    assert parser.arguments_values['string'] == ''


def test_single_value(arguments_definition):
    cli: list[str] = ['--some-string', 'String Value']
    parser = ArgumentsParser(arguments_definition, cli)
    assert parser.arguments_values['string'] == 'String Value'


def test_multiple_values(arguments_definition):
    cli: list[str] = ['--some-string', 'String Value', '--some-string', 'New Value']
    parser = ArgumentsParser(arguments_definition, cli)
    assert parser.arguments_values['string'] == 'New Value'


def test_switch_but_no_value(arguments_definition):
    cli: list[str] = ['--some-string']
    with pytest.raises(SystemExit):
        ArgumentsParser(arguments_definition, cli)


def test_no_cli_default_set_empty_string(arguments_definition):
    arguments_definition[0].default_value = ''
    cli: list[str] = []
    parser = ArgumentsParser(arguments_definition, cli)
    assert parser.arguments_values['string'] == ''


@pytest.mark.parametrize('tested_value', [
    'Some string',
    '',
    '  Some string',
])
def test_no_cli_default_set(arguments_definition, tested_value):
    arguments_definition[0].default_value = tested_value
    cli: list[str] = []
    parser = ArgumentsParser(arguments_definition, cli)
    assert parser.arguments_values['string'] == tested_value


@pytest.mark.parametrize('tested_value', [
    'Some string',
    '',
    '  Some string',
])
def test_no_cli_env_set(arguments_definition_with_env, env_var, tested_value):
    os.environ[env_var] = tested_value
    cli: list[str] = []
    parser = ArgumentsParser(arguments_definition_with_env, cli)
    assert parser.arguments_values['string'] == tested_value
