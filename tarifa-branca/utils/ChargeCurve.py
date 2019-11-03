import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go


class ChargeCurve:
    def __init__(self):
        self.white_tariff = pd.DataFrame({"time": np.arange(0, 24, 0.5),
                                          "value": np.array([0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.76971, 0.76971,
                                                             1.19806, 1.19806,
                                                             1.19806, 1.19806,
                                                             1.19806, 1.19806,
                                                             0.76971, 0.76971,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894,
                                                             0.51894, 0.51894])})

        self.conventional_tariff = pd.DataFrame({"time": np.arange(0, 24, 0.5),
                                                 "value": np.array([0.62833] * 48)})

    def plot_charge_cost(self):
        colors = ['rgb(17,103,96)', ] * 48
        for i in range(32, 34):
            colors[i] = 'rgb(201,150,69)'
        for i in range(34, 40):
            colors[i] = 'rgb(215,87,32)'
        for i in range(40, 42):
            colors[i] = 'rgb(201,150,69)'

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=self.white_tariff['time'],
                y=self.white_tariff['value'],
                marker_color=colors,
                name='Tarifa Branca'))
        fig.add_trace(
            go.Scatter(x=self.conventional_tariff['time'],
                       y=self.conventional_tariff['value'],
                       mode='lines',
                       line_color='rgb(226,39,28)',
                       name='Tarifa Convencional'))
        fig.update_layout(
            title_text='Tarifas Branca e Convencional',
            xaxis_title='Horário',
            yaxis_title='R$/kWh',
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            yaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=0.25
            )
        )
        plotly.offline.plot(fig, filename='environment.html')
