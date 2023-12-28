# tests/test_view.py

import pytest
from view.view import View
from model.pot import Pot
from raffle_app import RaffleApp

@pytest.fixture
def view():
    return View()

@pytest.fixture
def raffle_app():
    return RaffleApp()

def test_show_menu_option_1(capfd, monkeypatch, view, raffle_app):
    # Mock user input to simulate selecting option 1
    monkeypatch.setattr('builtins.input', lambda _: '1')

    # Call the show_menu method
    choice = view.show_menu(raffle_app)

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert that the menu output contains the expected string
    assert 'Welcome to My Raffle App' in captured.out
    assert 'Status: Draw has not started.' in captured.out
    assert '[1] Start a New Draw' in captured.out
    assert '[2] Buy Tickets' in captured.out
    assert '[3] Run Raffle' in captured.out
    assert choice == '1'  # Ensure that the user input is captured correctly

def test_show_menu_option_3(capfd, monkeypatch, view, raffle_app):
    # Set the stateRunning to True to simulate an ongoing draw
    raffle_app.stateRunning = True

    # Mock user input to simulate selecting option 3
    monkeypatch.setattr('builtins.input', lambda _: '3')

    # Ensure that stateRunning is set before calling show_menu
    assert raffle_app.stateRunning is True

    # Call the show_menu method
    choice = view.show_menu(raffle_app)

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert that the menu output contains the expected string
    assert 'Welcome to My Raffle App' in captured.out
    assert f'Status: Draw is ongoing. Raffle pot size is ${raffle_app.pot.amount}' in captured.out
    assert '[1] Start a New Draw' in captured.out
    assert '[2] Buy Tickets' in captured.out
    assert '[3] Run Raffle' in captured.out
    assert choice == '3'  # Ensure that the user input is captured correctly

if __name__ == "__main__":
    pytest.main()
