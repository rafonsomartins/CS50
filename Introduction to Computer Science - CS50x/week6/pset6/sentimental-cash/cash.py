# TODO
from cs50 import get_float

while True:
    x = get_float("Change owed: ")
    if x >= 0:
        break
cents = x*100
quarters = cents // 25
cents -= quarters*25
dimes = cents // 10
cents -= dimes*10
nickles = cents // 5
cents -= nickles*5
pennies = cents

coins = int(quarters + dimes + nickles + pennies)

print(f"{coins}")