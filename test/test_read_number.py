import pytest
import sys
import os

from add_path import add_path_f
add_path_f()

from main import read_number 

@pytest.fixture
def mocked_input(monkeypatch):
    """Фикстура для перехвата input."""
    def fake_input(prompt):
        return fake_input.values.pop(0)
    fake_input.values = []
    monkeypatch.setattr('builtins.input', fake_input)
    return fake_input

@pytest.mark.parametrize(
    "user_inputs, expected_result",
    [
        (["100"], "-"),
        (["900"], "-"),
        (["+7900"], "-"),
        (["8900"], "-"),
        (["123 112 90 90"], "-"), 
        ([""], "-"), 
        (["1231232323"], "-"),
        (["900123231"], "-"),
        (["109009001212"], "-"),
        (["10 900 900 12 12"], "-"),
        (["+"], "-"), 
        (["."], "-"), 
        (["Привет мир!"], "-"),
        (["+79091238989"], "+79091238989"),
        (["89091238989"], "+79091238989"),
        (["+7 909 123 89 89"], "+79091238989"),
        (["+790912   38989"], "+79091238989"), 
        (["9091238989"], "+79091238989"), 
        (["79091238989"], "+79091238989"), 
    ],
)
    
def test_read_number(mocked_input, user_inputs, expected_result):
    """Тестирует my_function с разными входами."""
    mocked_input.values = user_inputs
    assert read_number("Test") == expected_result





