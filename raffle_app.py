from controller.controller import Controller
from model.pot import Pot

class RaffleApp:
    # Initialize the RaffleApp with an initial pot size of $100, an empty list of users, and draw state is not running
    def __init__(self):
        self.pot = Pot(100.0)
        self.users = []
        self.stateRunning = False
    # Display menu by initializing controller and running it
    def display_menu(self):
        controller = Controller(self)
        controller.run()

if __name__ == "__main__":
    raffle_app = RaffleApp()
    raffle_app.display_menu()
