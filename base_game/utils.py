import re
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_special_characters(userinput: str):
    """
    Check if user's input is only an integer
    :param userinput:
    :return: bool
    """
    regex = re.compile("[@.€ç_!#$%^&*()<>' '?\"/\\|}{~:A-z]")
    if regex.search(userinput) is not None:
        print("Only number please")
        return False
    elif userinput == "":
        print("Type something ....")
        return False
    else:
        return True


def display_ascii_art(file):
    """Display ASCII art from a file."""
    abs_path = os.path.join(BASE_DIR, file)

    with open(abs_path, "r") as f:
        print(f.read())


def typewriter_effect(text):
    """Write text with a typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)  # Pause entre chaque lettre
    print()

def handle_exit():
    print("\nSaving your progress...")
    # @TODO: Ajouter une logique de sauvegarde
    print("Progress saved.")
    print("Goodbye, adventurer!")


def clear_screen(stdscr):
    """Clear the screen."""
    stdscr.move(2, 0)
    stdscr.clrtoeol()
    stdscr.move(3, 0)
    stdscr.clrtoeol()
    stdscr.move(6, 0)
    stdscr.clrtoeol()
    stdscr.move(7, 0)
    stdscr.clrtoeol()
    stdscr.move(8, 0)
    stdscr.clrtoeol()
    stdscr.move(9, 0)
    stdscr.clrtoeol()
