import time

import simpy


def falso_random(env):
    a = [1,2,3,4,5,6,7]
    i = 0
    for x in range(10):
        yield env.timeout(a[i])
        print(a[i])
        i+=1
        if i == len(a):
            i = 0

def example(env):
    value = yield env.timeout(1, value=42)
    print('now=%d, value=%d' % (env.now, value))

"""
env = simpy.Environment()
p = env.process(example(env))
env.run()
"""

env = simpy.Environment()
p = env.process(falso_random(env))
env.run()