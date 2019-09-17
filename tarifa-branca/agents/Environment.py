from mesa import Agent
from utils.ChargeCurve import ChargeCurve


class Environment(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.characteristic_curve = ChargeCurve()

    def step(self):
        self.characteristic_curve.plot_charge_cost()

