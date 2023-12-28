import random
from util.calculations_util import CalculationsUtil
from model.pot import Pot
from constants.constants import ValidationMessages
from model.ticket import Ticket

class RunRaffleService:
    
    # Run the raffle, find winners, claculate rewards and display result
    def execute(self, raffle_app):
        print("\nRunning Raffle..")

        # Generating the winning ticket
        winning_ticket = Ticket.generate_random_ticket()
        print(f"Winning Ticket is {' '.join(map(str, winning_ticket.numbers))}\n")
        # Find winners and count user ticket
        winners, user_ticket_count = self.find_winners(raffle_app.users, winning_ticket)

        # Calculating rewards and displaying winners
        total_reward = 0
        
        for group, group_winners in winners.items():
            reward_percentage = CalculationsUtil.GROUP_PERCENTAGES[int(group.split()[1])]
            if group_winners:
                total_reward += self.calculate_and_display_rewards(
                    group, group_winners, user_ticket_count, reward_percentage, raffle_app.pot
                )
            else:
                print(f"{group} Winners: Nil\n")

        # Rollover remaining money to the next draw
        raffle_app.pot.amount -= total_reward

        # reset users and draw state
        raffle_app.users = []
        raffle_app.stateRunning = False
        print(f"\n"+ ValidationMessages.DEFAULT_MENU)
    # find winners
    def find_winners(self, users, winning_ticket):
        winners = {'Group 2': [], 'Group 3': [], 'Group 4': [], 'Group 5': []}
        user_ticket_count = {}

        for user in users:
            for user_ticket in user.tickets:
                matching_numbers = len(set(winning_ticket.numbers) & set(user_ticket.numbers))

                if matching_numbers >= 2:
                    winners[f'Group {matching_numbers}'].append((user, user_ticket))
                    user_key = f"{user.name}_{matching_numbers}"
                    user_ticket_count[user_key] = user_ticket_count.get(user_key, 0) + 1

        return winners, user_ticket_count
    # Calculate and display rewards for each winner in a group
    def calculate_and_display_rewards(self, group, group_winners, user_ticket_count, reward_percentage, pot):
        total_reward_group = 0
        printed_users = set()
        print(f"{group} Winners:")
        for winner, winning_ticket in group_winners:
            user_key = f"{winner.name}_{int(group.split()[1])}"
            ticket_count = user_ticket_count.get(user_key, 0)

            if winner.name not in printed_users:
                reward = CalculationsUtil.calculate_reward(reward_percentage, pot, group_winners)
                reward = reward * ticket_count 
                print(f"{winner.name} with {ticket_count} winning ticket(s)- ${reward:.2f}\n")
                total_reward_group += reward

                # Mark the user as printed
                printed_users.add(winner.name)

        return total_reward_group
