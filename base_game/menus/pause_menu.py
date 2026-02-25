import curses

from pick import pick


class PauseMenu:
    def show(self, stdscr):
        """Affiche le menu pause."""
        stdscr.clear()
        title = "=== Menu Pause ==="
        options = ["Sauvegarder", "Quitter", "Reprendre le jeu"]
        _, choice = pick(options, title, screen=stdscr)
        stdscr.refresh()
        if choice == 0:
            stdscr.addstr("Sauvegarde en cours...\n")
            stdscr.refresh()
            curses.napms(1000)  # Simule un délai
            return "resume"
        elif choice == 1:
            return "quit"
        elif choice == 2:
            return "resume"
        else:
            return ""
