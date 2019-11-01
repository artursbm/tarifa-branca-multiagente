import matplotlib.pyplot as plt
import numpy as np

import utils.ProfileGenerator as pg


class ConsumerProfile:
    def __init__(self, agent_id):
        self.idx = agent_id
        self.products = pg.generate_product_list(self.idx)
        self.profile = pg.generate_profile(self.products)
        self.new_profile = None

    def plot_consumer_profile(self):
        fig = plt.figure()
        s = fig.add_subplot(111)
        s.set_xticks(range(0, 25))
        s.bar(self.profile['time'], self.profile['value'],
              align='edge',
              color='blue',
              label='Perfil de consumo')
        s.legend()
        plt.ylabel('kWh')
        plt.xlabel('Horário')
        plt.title(f"Perfil de consumo energético do usuário {self.idx}")
        plt.show()

    def plot_consumer_new_profile(self):
        fig = plt.figure()
        s = fig.add_subplot(111)
        s.set_xticks(range(0, 25))
        s.bar(self.new_profile['time'], self.new_profile['value'],
              align='edge',
              color='blue',
              label='Novo Perfil de consumo')
        s.legend()
        plt.ylabel('kWh')
        plt.xlabel('Horário')
        plt.title(f"Novo Perfil de consumo energético do usuário {self.idx}")
        plt.show()

    def plot_profile_comparison(self):
        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle(x=0.5, y=1.0, t=f'Comparativo de Perfil de consumo - Agente {self.idx}')
        ax1.bar(self.profile['time'], self.profile['value'],
                align='edge',
                color='blue',
                label='Perfil de consumo antes')

        ax2.bar(self.new_profile['time'], self.new_profile['value'],
                align='edge',
                color='blue',
                label='Perfil de consumo depois')

        ax1.set_xticks(range(0, 25))
        ax1.set_yticks(np.arange(0, 35, 0.75))

        ax2.set_xticks(range(0, 25))
        ax2.set_xticks(np.arange(0, 35, 0.75))

        ax1.set_xlabel(xlabel="Horário")
        ax1.set_ylabel(ylabel="kWh")

        ax2.set_xlabel(xlabel="Horário")
        ax2.set_ylabel(ylabel="kWh")

        plt.show()

    def generate_new_consumer_profile(self, envi, flexibility):
        conventional_tariff_cost = envi.characteristic_curve.conventional_tariff['value'] * self.profile[
            'value']

        self.new_profile = pg.regenerate_profile(self.products, envi.characteristic_curve.white_tariff['value'],
                                                 sum(conventional_tariff_cost), flexibility)

    def copy_profile(self):
        self.new_profile = self.profile.copy(deep=True)
