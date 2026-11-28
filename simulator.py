from numba import njit, uint8, int8, uint16, uint32, int32
from numba.experimental import jitclass

@njit
def get_territory(depth):
    return (depth + 1) * depth * 2

@njit
def get_perimeter(depth):
    return 4 * depth + 4

spec = [
    ('depth', uint16),
    ('territory', uint32),
    ('perimeter', uint16),
    ('dispatched', int32),
    ('tick', uint16),
    ('balance', int32),
    ('attack_wait', int8),
    ('tick10', uint8),
    ('tick100', uint8)
]

@jitclass(spec=spec)
class State:
    def __init__(self):
        self.balance = 512
        self.depth = 2
        self.territory = get_territory(self.depth)
        self.perimeter = get_perimeter(self.depth)
        self.dispatched = 0
        self.tick = 0
        self.attack_wait = -1
        self.tick10 = 0
        self.tick100 = 0

    def ticks(self, attack = -1):
        if attack != -1:
            self.dispatched = self.balance * attack // 100
            self.attack_wait = 0
        if self.attack_wait != -1:
            if self.attack_wait == 0:
                self.dispatched -= 2 * self.perimeter
                self.balance -= 2 * self.perimeter
                self.depth += 1
                self.perimeter = get_perimeter(self.depth)
                self.territory = get_territory(self.depth)
                self.attack_wait = 4 if self.territory < 1000 else 3
            else:
                self.attack_wait -= 1
        if self.dispatched < 0:
            self.dispatched = 0
            self.attack_wait = -1
        if self.tick10 == 10:
            available = self.balance - self.dispatched
            base = 0.07 - self.tick * 0.00003125
            if available > self.territory * 150:
                interest = 0
            elif available > self.territory * 100:
                interest = base * (1.5 - 0.05 * available / self.territory)
            else:
                interest = base
            self.balance += int(interest * available)
            self.tick10 = 0
            if self.tick100 == 100:
                self.balance += self.territory
                self.tick100 = 0
        self.tick += 1
        self.tick10 += 1
        self.tick100 += 1
