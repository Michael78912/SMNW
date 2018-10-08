import random


def closest(me, others):
    possible_destinations = others
    possible_destinations = [
        abs(me - destination) for destination in possible_destinations
    ]
    destination = min(possible_destinations)

    return others[possible_destinations.index(destination)]


print(
    closest(
        int(input('number: ')),
        eval(input('enter numbers to be closest to seperated by ,: '))))
