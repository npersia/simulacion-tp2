
import random

import simpy
import numpy

import pandas as pd

RANDOM_SEED = 42
NUM_ATM = 1         # Number of clients in the atm
ATM_TIME = 5        # Minutes it takes to user a atm
SIM_TIME = 540     # Simulation time in minutes

global df
df = pd.DataFrame(columns=["client", "arrive", "enter", "waits","leaves"])

global waiting_people
waiting_people = pd.DataFrame(columns=["clients"])


def use_time():
    return numpy.random.choice(
        [random.uniform(4-3,4+3),
         random.uniform(2-1,2+1),
         random.uniform(3-2,3+2)]
        ,p=[0.1,0.7,0.2])


def mean_time(now):
    if now <= 120:
        return 4
    elif now > 120 and now <= 300:
        return 2
    else:
        return 6


class Atm(object):

    def __init__(self, env, NUM_ATM):
        self.env = env
        self.atm = simpy.Resource(env, NUM_ATM)

    def use(self):
        yield self.env.timeout(use_time())


def client(env, name, atm):
    arrives = env.now
    print('%s arrives at the ATM at %.2f.' % (name, arrives))
    with atm.atm.request() as request:
        yield request

        enters = env.now
        print('%s enters the ATM at %.2f.' % (name, enters))
        yield env.process(atm.use())
        waits = enters-arrives
        print('%s waits time %.2f.' % (name, waits))

        print('%s leaves the ATM at %.2f.' % (name, env.now))
        print('Clients in the queue %d'% (len(atm.atm.queue)))
        wp = pd.DataFrame({"clients": [len(atm.atm.queue)]})

        global waiting_people
        waiting_people = waiting_people.append(wp,ignore_index = True)


        d2 = {"client": [name], "arrive": [arrives], "enter": [enters],"waits": [waits], "leaves": [env.now]}
        df2 = pd.DataFrame(data=d2)


        global df
        df = df.append(df2,ignore_index = True)


def setup(env, NUM_ATM):
    atm = Atm(env, NUM_ATM)
    i=0
    while True:
        t_inter = mean_time(env.now)
        yield env.timeout(random.expovariate(1/t_inter))
        i += 1
        env.process(client(env, 'Client %d' % i, atm))


# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_ATM))

# Execute!
env.run(until=SIM_TIME)


print(df)
print(waiting_people)