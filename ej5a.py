
import random

import simpy
import numpy

import pandas as pd

RANDOM_SEED = 42
NUM_SERVER = 1         # Number of clients in the Server
Server_TIME = 5        # Minutes it takes to user a Server
SIM_TIME = 50000     # Simulation time in minutes

global df
df = pd.DataFrame(columns=["Server","req", "arrive", "enter", "waits","leaves"])

global waiting_req
waiting_req = pd.DataFrame(columns=["Server","req"])


def use_time():
    return numpy.random.choice(
        [random.uniform(120-60,120+60),
         random.uniform(240-120,240+120),
         random.uniform(500-300,500+300)]
        ,p=[0.7,0.2,0.1])


class Server(object):

    def __init__(self, env, NUM_SERVER):
        self.env = env
        self.server = simpy.Resource(env, NUM_SERVER)

    def use(self):
        yield self.env.timeout(use_time())


def req(env, name,nServer, server):
    arrives = env.now
    print('%s arrives at the Server at %.2f.' % (name, arrives))

    print('Clients in the queue %d' % (len(server.server.queue)))
    wr = pd.DataFrame({"Server":[nServer],"req": [len(server.server.queue)]})
    global waiting_req
    waiting_req = waiting_req.append(wr, ignore_index=True)

    with server.server.request() as request:
        yield request

        enters = env.now
        print('%s enters the Server at %.2f.' % (name, enters))
        yield env.process(server.use())
        waits = enters-arrives
        print('%s waits time %.2f.' % (name, waits))

        print('%s leaves the Server at %.2f.' % (name, env.now))


        d2 = {"Server":[nServer],"req": [name], "arrive": [arrives], "enter": [enters],"waits": [waits], "leaves": [env.now]}
        df2 = pd.DataFrame(data=d2)


        global df
        df = df.append(df2,ignore_index = True)


def setup(env, NUM_SERVER):
    servers = [Server(env, NUM_SERVER),Server(env, NUM_SERVER),Server(env, NUM_SERVER),Server(env, NUM_SERVER),Server(env, NUM_SERVER)]
    i=0
    while True:
        t_inter = 45
        yield env.timeout(random.expovariate(1/t_inter))
        i += 1
        min_ocup = None
        min_server = None
        for j in range(len(servers)):
            if servers[j].server.users == 0:
                min_server = j
                break
            else:
                if min_ocup == None:
                    min_ocup = len(servers[j].server.queue)
                    min_server = j
                else:
                    if len(servers[j].server.queue) < min_ocup:
                        min_ocup = len(servers[j].server.queue)
                        min_server = j
        server = servers[min_server]





        env.process(req(env, 'Client %d' % i, 'Server %d' % min_server, server))


# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SERVER))

# Execute!
env.run(until=SIM_TIME)


print(df)
print(waiting_req)