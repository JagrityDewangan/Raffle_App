from model.pot import Pot

class StartRaffleService:
    # Display the new draw has been started
    def execute(self, raffle_app):
        
        print(f"\nNew Raffle draw has been started. Initial pot size: ${raffle_app.pot.amount:.2f}")
        raffle_app.stateRunning = True
        input("Press any key to return to the main menu ")
