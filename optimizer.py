from numba import njit, prange
import random
from simulator import State

def dominates(a, b):
    return a[0] >= b[0] and a[1] >= b[1] and a != b

def random_search(n, batch_size = 8):
    random.seed(42)
    def random_config():
        return tuple([(random.randrange(i * 100, (i + 1) * 100), random.randrange(0, 100)) for i in range(5)])
    @njit
    def test(config):
        s = State()
        for i in range(500):
            attack = -1
            for j in range(5):
                t, r = config[j]
                if i == t:
                    attack = r
            s.ticks(attack)
        return s.balance, s.territory

    # @njit(parallel = True)
    # def tests(configs):
    #     n = len(configs)
    #     bal, ter = [0] * n, [0] * n
    #
    #     for j in prange(n):
    #         bal[j], ter[j] = test(configs[j])
    #     return bal, ter

    front_set = {}
    for _ in range(n):
        res = test(cf := random_config())
        to_del = [r for r in front_set if dominates(res, r)]
        for r in to_del: del front_set[r]
        if not any(dominates(r, res) for r in front_set.keys()):
            front_set[res] = cf
    # for _ in range(n // batch_size):
        # bal, ter = tests(cf := [random_config() for _ in range(batch_size)])
        # result = list(zip(bal, ter))
        # to_del = [r for r in front_set if any(dominates(res, r) for res in result)]
        # for r in to_del: del front_set[r]
        # for res, config in zip(result, cf):
        #     if not any(dominates(r, res) for r in front_set.keys()):
        #         front_set[res] = config

    return front_set
