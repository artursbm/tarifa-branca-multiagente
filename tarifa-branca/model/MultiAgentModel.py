from mesa import Model
from mesa.time import BaseScheduler

from agents import Consumer


class MultiAgentModel(Model):
    def __init__(self, N):
        self.n_agents = N
        self.schedule = BaseScheduler(self)
        # Creating agents
        for i in range(self.n_agents):
            agent = Consumer.Consumer(i, self)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
