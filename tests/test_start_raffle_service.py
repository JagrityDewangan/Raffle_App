from unittest.mock import patch
import pytest
from io import StringIO
from raffle_app import RaffleApp
from service.start_raffle_service import StartRaffleService

@pytest.mark.parametrize("input_value, expected_output", [
    ([''], 'New Raffle draw has been started. Initial pot size: $100.00'),
    # Add more test cases if needed
])
def test_execute(input_value, expected_output, capsys):
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
