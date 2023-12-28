class CalculationsUtil:
    GROUP_PERCENTAGES = {2: 0.1, 3: 0.15, 4: 0.25, 5: 0.5}
    @staticmethod
    # Calculate the reward 
    def calculate_reward(reward_percentage, pot, winners):
        return reward_percentage * pot.amount / len(winners)