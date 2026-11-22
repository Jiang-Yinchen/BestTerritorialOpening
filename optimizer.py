import random
from simulator import State

def dominates(a, b):
    return a[0] >= b[0] and a[1] >= b[1] and a != b

def random_search(n):
    random.seed(42)
    def random_config():
        return [(random.randrange(i * 100, (i + 1) * 100), random.randrange(0, 100)) for i in range(5)]
    def test(config):
        s = State()
        for i in range(500):
            attack = -1
            for t, r in config:
                if i == t:
                    attack = r
            s.ticks(attack)
        return s.balance, s.territory

    front_set = {}
    for _ in range(n):
        res = test(cf := random_config())
        front_set = {r: c for r, c in front_set.items() if not dominates(res, r)}
        if not any(dominates(r, res) for r in front_set.keys()):
            front_set[res] = cf

    return front_set
