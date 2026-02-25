import curses

from pick import pick


class OptionsMenu:
    def show(self, stdscr):
        stdscr.clear()
        options = ["Changer la difficulté", "Retourner au menu principal"]
        _, choice = pick(options, screen=stdscr)
        stdscr.refresh()
        if choice == 0:
            stdscr.clear()
            title = "Choisissez la difficulté"
            options = ["Facile", "Normal", "Difficile", "legendaire"]
            level, choice = pick(options, title, screen=stdscr)
            stdscr.refresh()
            stdscr.addstr("Vous jouez maintenant en difficulté {}".format(level))
            stdscr.refresh()
            curses.napms(1000)
            stdscr.clear()
        return "back"