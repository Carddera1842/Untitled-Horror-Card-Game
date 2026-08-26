from card import Card
from enemy import Enemy
from player import Player

print("Welcome to the horror card game!")

player = Player("Survivor", 50, 0)
infected = Enemy("Infected", 100, 6)

print(f"Player: {player.name}")
print(f"Player Health: {player.health}")
print(f"Player Energy: {player.energy}")

print(f"Enemy: {infected.name}")
print(f"Enemy Health: {infected.health}")
print(f"Enemy Attack: {infected.attack}")

handgun = Card("Handgun Shot", 8, 1)

print(handgun.name)
print(f"Damage: {handgun.damage}")
print(f"Cost: {handgun.cost}")

def play_card(card, enemy):
    if player.energy >= card.cost:
        print(f"You played {card.name}!")
        player.energy -= card.cost
        enemy.health -= card.damage
        return True
    else:
        print("Not enough energy to play this card!")
        return False

play_card(handgun, infected)

print(f"Enemy Health: {infected.health}")

print(f"Player Energy: {player.energy}")

