import matplotlib.pyplot as plt


class ChargeCurve:
    def __init__(self, tariff_mode):
        self.tariff_mode = tariff_mode
        self.charge_cost = [0.51894, 0.51894, 0.51894, 0.51894, 0.51894, 0.51894, 0.51894, 0.51894, 0.51894, 0.51894,
                            0.51894, 0.51894, 0.51894, 0.51894, 0.51894,
                            0.51894, 0.76971, 1.19806, 1.19806, 1.19806,
                            0.76971, 0.51894, 0.51894, 0.51894]

    def plot_charge_cost(self):
        plt.bar(list(range(0,len(self.charge_cost))), self.charge_cost)
        plt.ylabel('R$/kWh')
        plt.xlabel('horário')
        plt.title(self.tariff_mode)
        plt.show()

