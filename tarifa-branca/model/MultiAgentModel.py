from mesa import Model
from mesa.time import BaseScheduler

from agents import Consumer, Environment


class MultiAgentModel(Model):
    def __init__(self, N):
        self.n_agents = N
        self.schedule = BaseScheduler(self)

        # Creating the environment and adding it to the scheduler, so I can access it on every agent step
        environment = Environment.Environment(N*2, self, tariff_mode="white-tariff")
        self.schedule.add(environment)

        # Creating agents
        for i in range(self.n_agents):
            agent = Consumer.Consumer(i, self)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
