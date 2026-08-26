from card import Card

print("Welcome to the horror card game!")

player_health = 50
enemy_health = 100

print(f"Player Health: {player_health}")
print(f"Enemy Health: {enemy_health}")

handgun = Card("Handgun Shot", 8, 1)

print(handgun.name)
print(f"Damage: {handgun.damage}")
print(f"Cost: {handgun.cost}")

