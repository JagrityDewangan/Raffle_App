import pytest
from unittest.mock import MagicMock, patch
from io import StringIO
from model.ticket import Ticket
from model.user import User
from raffle_app import RaffleApp
from service.run_raffle_service import RunRaffleService

def test_run_raffle_generate_winning_ticket_and_calculate_rewards():
    raffle_app = RaffleApp()

    with patch('builtins.input', return_value='3'), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        # Set up the test with necessary data
        user1 = raffle_app.users.append(User("User1", [Ticket([1, 2, 3, 4, 5])]))
        user2 = raffle_app.users.append(User("User2", [Ticket([6, 7, 8, 9, 10])]))

        # Mock RunRaffleService to generate a specific winning ticket for testing
        with patch.object(RunRaffleService(), 'winning_ticket', return_value=MagicMock(numbers=[1, 2, 3, 4, 5])):
            raffle_app.display_menu()

        output = mock_stdout.getvalue().strip()

        # Add your assertions based on the expected behavior
        assert "Running Raffle" in output
        assert "Winning Ticket is 1 2 3 4 5" in output
        assert "Group 2 Winners:" in output
        assert "Group 3 Winners:" in output
        assert "Group 4 Winners:" in output
        assert "Group 5 Winners:" in output
        assert "Press any key to return to the main menu" in output

        # You can add more specific assertions based on your application's behavior

if __name__ == '__main__':
    pytest.main()
