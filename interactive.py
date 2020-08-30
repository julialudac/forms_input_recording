from action_menu import FillFormMenu, ReadFormMenu, ReadFormsMenu


def get_welcome_message(xml_root):
    title_element = list(xml_root)[0]
    return "Welcome to the " + title_element.text + " system!"


def main():
    print("Welcome to form input recording program.")
    option = ""
    while option not in ["1", "2", "3"]:
        option = input(
            "What would you like to do?\n1. Fill a form\n2. Read form\n3. Read several forms at once from the same template\n")
        if option == "1":
            FillFormMenu()
        elif option == "2":
            ReadFormMenu()
        elif option == "3":
            ReadFormsMenu()


if __name__ == "__main__":
    main()
