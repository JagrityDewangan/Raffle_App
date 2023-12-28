# tests/test_raffle_app.py

import pytest
from service.sell_ticket_service import SellTicketsService
from model.pot import Pot
from raffle_app import RaffleApp

@pytest.fixture
def sell_tickets_service():
    return SellTicketsService()

@pytest.fixture
def raffle_app():
    return RaffleApp()

def test_choice_2_buy_tickets(capfd, monkeypatch, sell_tickets_service, raffle_app):
    # Mock user input to simulate choosing option 2
    monkeypatch.setattr('builtins.input', lambda _: '2')

    # Call the display_menu method to reach the buy tickets scenario
    raffle_app.display_menu()

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert that the menu output contains the expected string
    assert 'Welcome to My Raffle App' in captured.out
    assert 'Status: Draw has not started.' in captured.out
    assert '[1] Start a New Draw' in captured.out
    assert '[2] Buy Tickets' in captured.out
    assert '[3] Run Raffle' in captured.out

    # Mock user input to simulate buying tickets
    monkeypatch.setattr('builtins.input', lambda _: 'John,2')

    # Call the execute method of SellTicketsService
    sell_tickets_service.execute(raffle_app)

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert that the expected output is present in the captured output
    assert 'Hi John, you have purchased 2 ticket(s):' in captured.out
    assert 'Press any key to return to the main menu' in captured.out

    # Assert that the user has been added with purchased tickets
    assert len(raffle_app.users) == 1
    assert raffle_app.users[0].name == 'John'
    assert len(raffle_app.users[0].tickets) == 2

    # Assert that the pot amount has been updated
    assert raffle_app.pot.amount == 110.0  # Assuming each ticket costs $5

if __name__ == "__main__":
    pytest.main()
