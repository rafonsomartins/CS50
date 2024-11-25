# TODO
from cs50 import get_int
while True:
    x = get_int("heigth: ")
    if x < 9 and x > 0:
        break
for i in range(1, x + 1):
    for n in range(x - i):
        print(" ", end="")
    for m in range(i):
        print("#", end="")
    print("")