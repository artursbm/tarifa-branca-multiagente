from mesa import Agent
from utils.ChargeCurve import ChargeCurve


class Environment(Agent):

    def __init__(self, unique_id, model, tariff_mode):
        super().__init__(unique_id, model)
        self.characteristic_curve = ChargeCurve(tariff_mode=tariff_mode)

    def step(self):
        self.characteristic_curve.plot_charge_cost()

