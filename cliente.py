from random import uniform, random


def tiempo(m,e):
    return uniform(m-e,m+e)

def discretizar():
    r = random()
    if r < 0.1:
        return tiempo(4,3)
    elif r >= 0.1 and r < 0.8:
        return tiempo(2,1)
    else:
        return tiempo(3, 2)

print(discretizar())