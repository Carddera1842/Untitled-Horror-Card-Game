from card import Card
from enemy import Enemy

print("Welcome to the horror card game!")

player_health = 50

infected = Enemy("Infected", 100, 6)

print(f"Player Health: {player_health}")

print(f"Enemy: {infected.name}")
print(f"Enemy Health: {infected.health}")
print(f"Enemy Attack: {infected.attack}")

handgun = Card("Handgun Shot", 8, 1)

print(handgun.name)
print(f"Damage: {handgun.damage}")
print(f"Cost: {handgun.cost}")

def play_card(card, enemy):
    enemy.health -= card.damage
    return enemy.health

enemy_health = play_card(handgun, infected)

print(f"You played {handgun.name}!")

print(f"Enemy Health: {enemy_health}")

