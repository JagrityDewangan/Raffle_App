from unittest.mock import patch
import pytest
from io import StringIO
from model.ticket import Ticket
from model.user import User
from raffle_app import RaffleApp
from service.run_raffle_service import RunRaffleService
from service.sell_ticket_service import SellTicketsService
from service.start_raffle_service import StartRaffleService

@pytest.mark.parametrize("input_value, expected_output", [
    ([''], 'New Raffle draw has been started. Initial pot size: $100.00'), ])
def test_start_raffle_service(input_value, expected_output, capsys):
    # Create an instance of RaffleApp and StartRaffleService
    raffle_app = RaffleApp()
    start_raffle_service = StartRaffleService()

    # Patch the input function to return the provided input_value
    with patch('builtins.input', side_effect=input_value):
        # Call the execute method
        start_raffle_service.execute(raffle_app)

    # Capture the standard output
    captured = capsys.readouterr()

    # Assert that the captured output matches the expected output
    assert captured.out.strip() == expected_output

# Function to set up a test RaffleApp instance with users and state
def setup_test_raffle_app():
    raffle_app = RaffleApp()
    user1 = User("John", [Ticket([1, 2, 3, 4, 5])])
    user2 = User("Jane", [Ticket([6, 7, 8, 9, 10])])
    raffle_app.users = [user1, user2]
    raffle_app.stateRunning = True
    return raffle_app

# Test for SellTicketService
def test_execute_sell_tickets_service():
    # Patch input functions to assume user input
    with patch('builtins.input', side_effect=['John,2']):
        raffle_app = setup_test_raffle_app()
        initial_pot_amount = raffle_app.pot.amount
        
        sell_tickets_service = SellTicketsService()
        sell_tickets_service.execute(raffle_app)
        # Assert that the state has changes as expected
        assert len(raffle_app.users) == 2
        assert raffle_app.users[0].name == 'John'
        assert len(raffle_app.users[0].tickets) == 3
        assert raffle_app.pot.amount == initial_pot_amount + 2 * 5

# Test for RunRaffleService
def test_execute_run_raffle_service():
    raffle_app = setup_test_raffle_app()
    raffle_app.pot.amount = 100.0

    run_raffle_service = RunRaffleService()
    run_raffle_service.execute(raffle_app)
    # Assert that the state has changes as expected
    assert raffle_app.stateRunning is False
    assert not raffle_app.users
    assert raffle_app.pot.amount <= 100.0

# Test for finding winners in the raffle draw
def test_find_winners():
    raffle_app = setup_test_raffle_app()
    winning_ticket = Ticket([1, 2, 3, 4, 5])

    run_raffle_service = RunRaffleService()
    winners, user_ticket_count = run_raffle_service.find_winners(raffle_app.users, winning_ticket)

    assert len(winners) == len({'Group 2', 'Group 3', 'Group 4', 'Group 5'})
    assert all(group in winners for group in {'Group 2', 'Group 3', 'Group 4', 'Group 5'})

# Test for calculating and displaying reward
def test_calculate_and_display_rewards():
    raffle_app = setup_test_raffle_app()
    group = 'Group 2'
    group_winners = [(raffle_app.users[0], [1, 2, 3, 4, 5])]

    user_ticket_count = {'John_2': 1}
    reward_percentage = 0.1
    pot = raffle_app.pot

    run_raffle_service = RunRaffleService()
    total_reward_group = run_raffle_service.calculate_and_display_rewards(
        group, group_winners, user_ticket_count, reward_percentage, pot
    )

    assert total_reward_group == 0.1 * pot.amount
