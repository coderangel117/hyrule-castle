from base_game.classes.Boss import Boss
from base_game.classes.Castle import Castle
from base_game.classes.Enemy import Enemy
from base_game.classes.Player import Player


def choice_action(player):
    print("What do you want to do?")
    print("1. Attack")
    print("2. Heal")
    choice = input()
    if choice == "1":
        print("You attack!")
    elif choice == "2":
        player.self_heal()
        print("You heal!")
    else:
        print("Invalid choice. Please choose again.")
        choice_action(player)
    return int(choice)

def display_ascii_art(file):
    print("Welcome to the game!")
    with open(file, "r") as f:
        print(f.read())


def define_character():
    player = Player("Link", 60, 60, 15)
    enemy = Enemy("Bokoblin", 30, 30, 5)
    boss = Boss("Ganon", 150, 150, 20)
    return player, enemy, boss


def main():
    hyrule = Castle(10)
    # display_ascii_art("Title.txt")
    player, enemy, boss = define_character()
    for i in range(hyrule.nb_level):
        enemy.reload_health()
        print(f"Level {i + 1}")
        print("You encounter an enemy!")
        print(f"{enemy.name} has {enemy.health} health.")
        print(f"{player.name} has {player.health} health.")
        while enemy.health > 0 and player.health > 0:
            choice =  choice_action(player)
            if choice == 1:
                player.attack(enemy)
            if enemy.health <= 0:
                print(f"{enemy.name} has been defeated!")
                break
            enemy.attack(player)
            if player.health <= 0:
                print(f"{player.name} has been defeated!")
                break
        print(f"{player.name} has {player.health} health.")
        print("You have reached the next level!")


if __name__ == "__main__":
    main()
