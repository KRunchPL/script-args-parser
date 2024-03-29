import os
from dataclasses import asdict
from tempfile import NamedTemporaryFile
from typing import Any

import pytest
import toml

from script_args_parser import ArgumentsParser


def assert_argument_values(name: str, mapping_dict: dict[str, Any], argument_dict: dict[str, Any]) -> None:
    assert name == argument_dict['name']
    for k, v in mapping_dict.items():
        assert argument_dict[k] == v


def test_single_arg():
    mappings = {
        'first_arg': {
            'type': 'str',
            'description': 'Some fancy description',
            'cli_arg': '--cli-option-name',
            'env_var': 'ENV_VAR_NAME',
            'default_value': 'first_default',
            'required': True,
        }
    }
    toml_file = NamedTemporaryFile(mode='w', delete=False)
    try:
        toml.dump(mappings, toml_file)
        toml_file.close()
        parser = ArgumentsParser.from_files(toml_file.name, [])
        assert_argument_values('first_arg', mappings['first_arg'], asdict(parser.arguments[0]))
    finally:
        os.unlink(toml_file.name)


def test_multiple_args():
    mappings = {
        'first_arg': {
            'type': 'str',
            'description': 'Some fancy description',
            'cli_arg': '--cli-option-name',
            'env_var': 'ENV_VAR_NAME',
            'default_value': 'first_default',
            'required': True,
        },
        'second_arg': {
            'type': 'tuple[int, bool, path]',
            'description': 'Some fancy description',
            'cli_arg': '--cli-option-name-for-tuple',
            'env_var': 'ENV_VAR_NAME_TUPLE',
            'default_value': '10 True .',
            'required': False,
        }
    }
    toml_file = NamedTemporaryFile(mode='w', delete=False)
    try:
        toml.dump(mappings, toml_file)
        toml_file.close()
        parser = ArgumentsParser.from_files(toml_file.name, [])
        for i, mapping in enumerate(mappings.items()):
            name, mapp = mapping
            assert_argument_values(name, mapp, asdict(parser.arguments[i]))
    finally:
        os.unlink(toml_file.name)


def test_default_required():
    mappings: dict[str, Any] = {
        'first_arg': {
            'type': 'str',
            'description': 'Some fancy description',
            'cli_arg': '--cli-option-name',
            'env_var': 'ENV_VAR_NAME',
            'default_value': 'first_default',
        }
    }
    toml_file = NamedTemporaryFile(mode='w', delete=False)
    try:
        toml.dump(mappings, toml_file)
        toml_file.close()
        parser = ArgumentsParser.from_files(toml_file.name, [])
        mappings['first_arg']['required'] = False
        assert_argument_values('first_arg', mappings['first_arg'], asdict(parser.arguments[0]))
    finally:
        os.unlink(toml_file.name)


@pytest.mark.parametrize('given_value, expected_value', [
    ('nO', False),
    ('FaLSe', False),
    ('0', False),
    ('yEs', True),
    ('TruE', True),
    ('1', True),
])
def test_string_required(given_value, expected_value):
    mappings = {
        'first_arg': {
            'type': 'str',
            'description': 'Some fancy description',
            'cli_arg': '--cli-option-name',
            'env_var': 'ENV_VAR_NAME',
            'default_value': 'first_default',
            'required': given_value,
        }
    }
    toml_file = NamedTemporaryFile(mode='w', delete=False)
    try:
        toml.dump(mappings, toml_file)
        toml_file.close()
        parser = ArgumentsParser.from_files(toml_file.name, [])
        mappings['first_arg']['required'] = expected_value
        assert_argument_values('first_arg', mappings['first_arg'], asdict(parser.arguments[0]))
    finally:
        os.unlink(toml_file.name)
