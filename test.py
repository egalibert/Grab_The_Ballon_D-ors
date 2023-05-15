counter = 90
multiplier = 0.2
level = 10
velocity = 2

while level < counter:
    velocity += 2 * multiplier
    level += 10
    print(velocity)