from classes.Boss import Boss
from classes.Castle import Castle
from classes.Enemy import Enemy
from classes.Player import Player

def choice_action(player):
    choice = 0
    while choice not in ["1", "2"]:
        print("What do you want to do?")
        print("1. Attack")
        print("2. Heal")
        choice = input()
    return int(choice)

def display_ascii_art(file, reduced=False, scale=0.5):
    with open(file, "r") as f:
        print(f.read())


def define_character():
    player = Player("Link", 60, 120, 15)
    enemy = Enemy("Bokoblin", 30, 30, 5)
    boss = Boss("Ganon", 150, 150, 20)
    return player, enemy, boss


def main():
    hyrule = Castle(3)
    boss_level = hyrule.nb_level
    # display_ascii_art("Title.txt")
    player, enemy, boss = define_character()
    for i in range(0, boss_level):
        if i == boss_level:
            enemy = boss
        enemy.reload_health()
        print(f"Level {i + 1}")
        while enemy.health > 0 and player.health > 0:
            print("You encounter an enemy!")
            print(f"{enemy.name} has {enemy.health} health.")
            print(f"{player.name} has {player.health} health.")
            choice = choice_action(player)
            if choice == 1:
                player.attack(enemy)
            else:
                player.self_heal()
            if enemy.health <= 0:
                i += 1
                if i < boss_level:
                    print("You have reached the next level!")
                else:

                    print("You defeated the boss!")
                    display_ascii_art("victory.txt")
                    return
            enemy.attack(player)
            if player.health <= 0:
                display_ascii_art("game_over.txt")
                return
if __name__ == "__main__":
    main()
