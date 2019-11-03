import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        fig = make_subplots(rows=2, cols=1, subplot_titles=("Consumo antes", "Consumo depois"))
        fig.add_trace(
            go.Bar(
                x=self.profile['time'],
                y=self.profile['value'],
            ),
            row=1,
            col=1
        )
        fig.add_trace(
            go.Bar(
                x=self.new_profile['time'],
                y=self.new_profile['value'],
            ),
            row=2,
            col=1
        )
        fig.update_xaxes(title_text='Horário', tick0=0, dtick=1, row=1, col=1)
        fig.update_xaxes(title_text='Horário', tick0=0, dtick=1, row=2, col=1)
        fig.update_yaxes(title_text='kWh', range=[0, 30], row=2, col=1)
        fig.update_yaxes(title_text='kWh', range=[0, 30], row=2, col=1)
        fig.update_layout(showlegend=False,
                          title_text=f'Comparativo de Perfil de consumo - Agente {self.idx}',
                          )
        plotly.offline.plot(fig, filename=f'agent_{self.idx}.html')

    def generate_new_consumer_profile(self, envi, flexibility):
        conventional_tariff_cost = envi.characteristic_curve.conventional_tariff['value'] * self.profile[
            'value']

        self.new_profile = pg.regenerate_profile(self.products, envi.characteristic_curve.white_tariff['value'],
                                                 sum(conventional_tariff_cost), flexibility)

    def copy_profile(self):
        self.new_profile = self.profile.copy(deep=True)
