import random
class Ticket:
    # Initialize the ticket
    def __init__(self, numbers):
        self.numbers = numbers

    @classmethod
    # Generate random ticket with 5 unique numbers in range 1 to 15
    def generate_random_ticket(cls):
        numbers = random.sample(range(1, 16), 5)
        return cls(numbers)