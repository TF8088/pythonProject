import os


class Menu:
    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle
        self.options = []

    @staticmethod
    def clear_screen():
        """
        Clears the console screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def wait_for_input():
        """
        Waits for user input, typically used to pause the program execution.
        """
        input("Press Enter to continue...")

    @staticmethod
    def quit_program():
        """
        Exits the program.
        """
        print("Exiting...")
        quit()

    def add_option(self, op_text, op_func, *args):
        """
        Adds an option to the menu.

        Args:
            `opText (str)`: The text describing the option.
            `opFunc (function)`: The function to be called when the option is selected.
            `*args`: Optional arguments to be passed to the function.
        """
        self.options.append((op_text, op_func, args))

    def add_submenu(self, op_text, submenu):
        """
        Adds a submenu option to the menu.

        Args:
            op_text (str): The text describing the submenu option.
            submenu (Menu): The submenu to be added.
        """
        self.add_option(op_text, submenu.show)

    def show(self):
        """
        Displays the menu and handles user input.
        """

        max_option_length = 52
        max_option_length += 4

        while True:
            self.clear_screen()
            print("╔" + "═" * max_option_length + "╗")
            print("║" + f"{self.title:^{max_option_length}}" + "║")
            print("║" + f"{self.subtitle:^{max_option_length}}" + "║")
            print("╠" + "═" * max_option_length + "╣")

            for i, (op_text, _, _) in enumerate(self.options, start=1):
                print(f"║ {i}. {op_text:<{max_option_length - 5}} ║")

            print("║ 0." + f" {'Exit':<{max_option_length - 5}} ║")
            print("╚" + "═" * max_option_length + "╝")

            choice = input("Enter the number of your choice: ")

            self.clear_screen()

            try:
                choice = int(choice)
                if 0 <= choice <= len(self.options):
                    if choice == 0:
                        return
                    else:
                        op_text, op_func, args = self.options[choice - 1]
                        if args:
                            op_func(*args)
                            self.wait_for_input()
                        else:
                            op_func()
                            self.wait_for_input()
                else:
                    print("Invalid choice")
            except ValueError as e:
                print("Invalid input:", e)


class Submenu(Menu):
    def __init__(self, title, subtitle):
        """
        Initialize the Submenu with a title and subtitle.

        Args:
            `title (str)`: The title of the submenu.
            `subtitle (str)`: The subtitle of the submenu.
        """
        super().__init__(title, subtitle)
