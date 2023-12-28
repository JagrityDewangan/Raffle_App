from view.view import View
from service.start_raffle_service import StartRaffleService
from service.sell_ticket_service import SellTicketsService
from service.run_raffle_service import RunRaffleService
from constants.constants import ValidationMessages

class Controller:
    # Initializing controller with RaffleApp, View, services
    def __init__(self, raffle_app):
        self.raffle_app = raffle_app
        self.view = View()
        self.start_raffle_service = StartRaffleService()
        self.sell_tickets_service = SellTicketsService()
        self.run_raffle_service = RunRaffleService()
        self.state = "not_running"
        self.ticket_purchase_completed = False
        self.is_running = True
    def run(self):
        # Display menu control based on draw state
        while True:
            # If draw is not running, request the user to start a new draw or display error for wrong choice
            if self.state == "not_running":
                choice = self.view.show_menu(self.raffle_app)
                if choice == '1':
                    self.start_raffle_service.execute(self.raffle_app)
                    self.state = "running"
                else:
                    print(ValidationMessages.INVALID_CHOICE1)
                    self.is_running = False
            # If the draw is running, handle options for buying ticket and running raffle
            elif self.state == "running":
                choice = self.view.show_menu(self.raffle_app)
                if choice == '2':
                    self.sell_tickets_service.execute(self.raffle_app)
                    self.ticket_purchase_completed = True
                elif choice == '3'and not self.ticket_purchase_completed:
                    print(ValidationMessages.INVALID_CHOICE2)
                    self.is_running = False
                elif choice == '3':
                    self.run_raffle_service.execute(self.raffle_app)
                    self.state = "ended"
                else:
                    print(ValidationMessages.INVALID_CHOICE2)
                    self.is_running = False
            # If draw is ended, request the user to starta new draw
            elif self.state == "ended":
                choice = self.view.show_menu(self.raffle_app)
                if choice == '1':
                    self.start_raffle_service.execute(self.raffle_app)
                    self.state = "running"
                    self.ticket_purchase_completed = False
                else:
                    print(ValidationMessages.INVALID_CHOICE1)
                    self.is_running = False