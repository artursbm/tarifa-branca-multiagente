import numpy as np
from mesa import Agent

from utils.ConsumerProfile import ConsumerProfile


class Consumer(Agent):
    """
    Consumer represents a customer of the energy system. It will have a flag to tell, at the end of the simulations,
    if the agent has adhered to the Tarifa Branca charging model.

    :ivar subscribe: defines the agent status related to the Tarifa Branca program
    (whether the agent have subscribed or not) after simulation step
    :type subscribe: bool

    :ivar flexibility: defines the agent odds of changing its energy consumption habits, given its current habits and the
    Environment characteristics (its Charging curve, for example).
    :type flexibility: float

    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.subscribe = False
        self.flexibility = np.random.rand()
        self.consumer_profile = ConsumerProfile(self.unique_id)

    def step(self):
        self.consumer_profile.plot_consumer_profile()
        choice = self.choose_subscription()
        if (self.flexibility + choice) / 2 >= 0.5:
            self.subscribe = True
            print(f'Cons. {self.unique_id} optou por aderir à Tarifa Branca. Flexibilidade: {self.flexibility}')
        else:
            print(f'Cons. {self.unique_id} se manterá na Tarifa Convencional. Flexibilidade: {self.flexibility}')

    @staticmethod
    def choose_subscription():
        """
        this method will randomly choose between
        0: Tarifa Convencional
        1: Tarifa Branca
        """
        return np.random.choice([0, 1])

    @staticmethod
    def tariff_mode(choice):
        return "Tarifa Convencional" if choice == 0 else "Tarifa Branca"
