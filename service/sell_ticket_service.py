from constants.constants import ValidationMessages
from model.user import User
from model.ticket import Ticket

class SellTicketsService:
    # Run to take input for user name and number of tickets
    def execute(self, raffle_app):
        user_input = input("Enter your name, number of tickets to purchase (e.g., James,1): ")

        # Splitting user input into name and number of tickets
        input_parts = [part.strip() for part in user_input.split(',')]
        name = input_parts[0]
        number_of_tickets = int(input_parts[1])
        
        # Validating if both name and number of tickets are provided
        if len(input_parts) != 2 or not input_parts[0] or not input_parts[1].isdigit():
            print(ValidationMessages.INVALID_TICKET)
            return
        
        name, num_tickets = input_parts
        if not name.strip().isalpha():
            print(ValidationMessages.INVALID_USER)
            return

        num_tickets = int(num_tickets)

        # Checking for unique user not purchasing more than 5 tickets
        total_tickets_for_user = sum(1 for user in raffle_app.users if user.name == name)
        if total_tickets_for_user + num_tickets > 5:
            print(ValidationMessages.INVALID_TICKET_COUNT.format(name=name))
            return

        existing_user = next((user for user in raffle_app.users if user.name == name), None)
        if existing_user:
            if len(existing_user.tickets) + num_tickets > 5:
                print(ValidationMessages.INVALID_TICKET_COUNT.format(name=name))
                return

            new_tickets = [Ticket.generate_random_ticket() for _ in range(num_tickets)]
            existing_user.tickets.extend(new_tickets)
            purchased_tickets = new_tickets
        else:
            purchased_tickets = [Ticket.generate_random_ticket() for _ in range(num_tickets)]
            user = User(name, purchased_tickets)
            raffle_app.users.append(user)

        print(f"\nHi {name}, you have purchased {num_tickets} ticket(s):")
        for ticket_index, ticket in enumerate(purchased_tickets):
            print(f"Ticket {ticket_index + 1}: {' '.join(map(str, ticket.numbers))}")
        # Calculating the pot size based on user ticket count
        raffle_app.pot.amount += num_tickets * 5
        print(f"\n"+ ValidationMessages.DEFAULT_MENU)
