class View:
    # Display main menu and taking choice 1, 2, and 3 as a input
    def show_menu(self, raffle_app):
        print('\n---------------------------------------------------------------------')
        print("\nWelcome to My Raffle App")

        if not raffle_app.stateRunning:
            print(f"Status: Draw has not started.")
            
        else:
            print(f"Status: Draw is ongoing. Raffle pot size is $"+str(raffle_app.pot.amount))

        print("\n[1] Start a New Draw")
        print("[2] Buy Tickets")
        print("[3] Run Raffle")

        choice = input("\nEnter your choice (1, 2, or 3): ")

        return choice
