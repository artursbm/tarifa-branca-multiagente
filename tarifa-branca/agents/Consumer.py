import numpy as np
from mesa import Agent


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
        # self.consumption = ConsumptionCurve(obj1, obj2, obj3, obj4...) add this later

    def step(self):
        choice = self.choose_subscription()
        if (self.flexibility + choice) / 2 >= 0.5:
            self.subscribe = True
            print("Cons. {} optou por aderir. Flexibilidade: {}; Método de Escolha: {}".format(self.unique_id,
                                                                                               self.flexibility,
                                                                                               choice))
        else:
            print("Cons. {} NÃO optou por aderir. Flexibilidade: {}; Método de Escolha: {}".format(self.unique_id,
                                                                                                   self.flexibility,
                                                                                                   choice))

    @staticmethod
    def choose_subscription():
        """
        this method will randomly choose between
        0: Tarifa Convencional
        1: Tarifa Branca
        """
        return np.random.choice([0, 0.5])
