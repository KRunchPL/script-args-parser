from enum import auto, Enum
from typing import ClassVar, Iterator


class State(Enum):
    """
    String parsing states.
    """

    #: start state for general character handling
    GENERAL = auto()
    #: when double quote has started
    DOUBLE_QUOTE = auto()
    #: when single quote has started
    SINGLE_QUOTE = auto()


class CharBasedStateMachine:
    """
    State machine that performs transitions based on a single character.

    For each transition it returns a boolean value indicating whether the character was a token separator.
    """

    #: state transitions for each states
    #: { State: { <character encountered>: (<is char a token separator>, <state after transition>)} }
    #: default transition is: (False, <current state>)
    _TRANSITIONS: ClassVar[dict[State, dict[str, tuple[bool, State]]]] = {
        State.GENERAL: {
            ';': (True, State.GENERAL),
            '"': (False, State.DOUBLE_QUOTE),
            "'": (False, State.SINGLE_QUOTE),
        },
        State.DOUBLE_QUOTE: {
            '"': (False, State.GENERAL),
        },
        State.SINGLE_QUOTE: {
            "'": (False, State.GENERAL),
        },
    }

    def __init__(self) -> None:
        self._state = State.GENERAL

    def transition(self, char: str) -> bool:
        """
        Perform state transition based on provided character.

        :param char: character that triggered transition
        :return: whether character is a token separator
        """
        assert len(char) == 1
        is_token_separator, self._state = self._TRANSITIONS[self._state].get(char, (False, self._state))
        return is_token_separator


class StringIterator:
    """
    Iterator of string that provides additional index property.
    """

    def __init__(self, value: str) -> None:
        self._value = value
        self._reset()

    def __iter__(self) -> Iterator[str]:
        """
        Reset self to the begining of the string.

        :return: self
        """
        self._reset()
        return self

    def __next__(self) -> str:
        """
        Return next character from the string.

        :return: next character from the string
        """
        self._index += 1
        return next(self._chars)

    @property
    def index(self) -> int:
        """
        Index of last returned character.

        :return: index of last returned character
        """
        return self._index

    def _reset(self) -> None:
        self._chars = iter(self._value)
        self._index = -1


def split_string_by_semicolon(argument_value: str) -> list[str]:
    """
    Split given string by semicolon.

    :param argument_value: value to be split
    :return: split result
    """
    values = []
    state_machine = CharBasedStateMachine()
    token_start = 0
    chars = StringIterator(argument_value)
    for char in chars:
        if char == '\\':
            next(chars)  # skip next character
            continue
        if state_machine.transition(char):
            values.append(argument_value[token_start:chars.index])
            token_start = chars.index + 1
            continue
    values.append(argument_value[token_start:])
    return values
