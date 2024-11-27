import os

from classes.Boss import Boss
from classes.Castle import Castle
from classes.Enemy import Enemy
from classes.Player import Player


def choice_action(player):
    choice = 0
    while choice not in ["1", "2"]:
        print("---OPTIONS-----\n"
              "1. Attack    2. Heal")
        choice = input()
    return int(choice)


def display_ascii_art(file, reduced=False, scale=0.5):
    with open(file, "r") as f:
        print(f.read())


def define_character():
    player = Player("Link", 60, 60, 15)
    enemy = Enemy("Bokoblin", 30, 30, 5)
    boss = Boss("Ganon", 150, 150, 20)
    return player, enemy, boss


def main():
    hyrule = Castle(10)
    boss_level = hyrule.nb_level
    # display_ascii_art("Title.txt")
    player = define_character()[0]
    for i in range(1, boss_level + 1):
        enemy = Enemy("Bokoblin", 30, 30, 5)
        if i == boss_level:
            enemy = Boss("Ganon", 150, 150, 20)
            print("You have reached the boss level!")
        print(f"========== FIGHT {i} ==========")
        while enemy.health > 0 and player.health > 0:
            enemy_hp = "I" * int(enemy.health)
            player_hp = "I" * int(player.health)
            print(f"{enemy.name} \n "
                  f"HP: {enemy_hp} {enemy.health}/{enemy.max_health}")
            print(f"{player.name} \n"
                  f"HP: {player_hp} {player.health}/{player.max_health}")
            choice = choice_action(player)
            if choice == 1:
                player.attack(enemy)
            else:
                player.self_heal()
                print(f"{player.name} used heal!")
            if enemy.health <= 0:
                if i < boss_level:
                    print(f"{enemy.name} died!")
                    i += 1
                    input('Press any key to continue...')
                    break
                if i == boss_level:
                    print("You defeated the boss!")
                    os.system("mpg123 /srv/http/hyrule-castle/base_game/victory_8bit.mp3 > /dev/null 2>&1")
                    display_ascii_art("victory.txt")
                    return
            enemy.attack(player)
            if player.health <= 0:
                display_ascii_art("game_over.txt")
                return


if __name__ == "__main__":
    main()
