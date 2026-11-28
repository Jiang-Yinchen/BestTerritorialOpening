class State:
    @staticmethod
    def get_territory(depth):
        return (depth + 1) * depth * 2

    @staticmethod
    def get_perimeter(depth):
        return 4 * depth + 4

    def __init__(self):
        self.balance = 512
        self.depth = 2
        self.territory = State.get_territory(self.depth)
        self.perimeter = State.get_perimeter(self.depth)
        self.dispatched = 0
        self.tick = 1
        self.attack_wait = -1
        self.interest = 0

    def ticks(self, attack = -1):
        if attack != -1:
            self.dispatched = self.balance * attack // 100
            self.attack_wait = 0
        if self.attack_wait != -1:
            if self.attack_wait == 0:
                self.dispatched -= 2 * self.perimeter
                self.balance -= 2 * self.perimeter
                self.depth += 1
                self.perimeter = State.get_perimeter(self.depth)
                self.territory = State.get_territory(self.depth)
                self.attack_wait = 4 if self.territory < 1000 else 3
            else:
                self.attack_wait -= 1
        if self.dispatched < 0:
            self.dispatched = 0
            self.attack_wait = -1
        if self.tick % 10 == 0:
            available = self.balance - self.dispatched
            base = 0.07 - self.tick * 0.00003125
            if available > self.territory * 150:
                self.interest = 0
            elif available > self.territory * 100:
                self.interest = base * (1.5 - 0.05 * available / self.territory)
            else:
                self.interest = base
            self.balance += int(self.interest * available)
        if self.tick % 100 == 0:
            self.balance += self.territory
        self.tick += 1
