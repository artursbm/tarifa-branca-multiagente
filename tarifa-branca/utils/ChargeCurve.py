import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
        fig = plt.figure()
        s = fig.add_subplot(111)
        s.set_xticks(range(0, 25))
        s.bar(self.white_tariff['time'], self.white_tariff['value'],
              align='edge',
              color='green',
              label='Tarifa Branca')
        s.plot(self.conventional_tariff['time'], self.conventional_tariff['value'],
               color='red',
               label='Tarifa Convencional')

        s.legend()
        plt.ylabel('R$/kWh')
        plt.xlabel('Horário')
        plt.title("Custos de Tarifa Branca vs. Tarifa Convencional")
        plt.show()
