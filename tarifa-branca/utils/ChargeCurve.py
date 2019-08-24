import matplotlib.pyplot as plt
import numpy as np


class ChargeCurve:
    def __init__(self):
        self.white_tariff = np.array([0.51894, 0.51894,
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
                                      0.51894, 0.51894])
        self.conventional_tariff = np.array([0.62833] * 25)

    def plot_charge_cost(self):
        fig = plt.figure()
        s = fig.add_subplot(111)
        s.bar(np.arange(0.5, 24.5, 0.5), self.white_tariff)
        s.plot(np.arange(0, 25, 1), self.conventional_tariff, color='red')
        s.set_xticks(range(0, 25))

        plt.ylabel('R$/kWh')
        plt.xlabel('horário')
        plt.title("Custos de Tarifa Branca vs. Tarifa Convencional")
        plt.show()
