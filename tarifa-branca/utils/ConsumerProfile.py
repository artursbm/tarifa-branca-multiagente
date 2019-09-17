import matplotlib.pyplot as plt

import utils.ProfileGenerator as pg


class ConsumerProfile:
    def __init__(self, agent_id):
        self.idx = agent_id
        self.products = pg.generate_product_list(self.idx)
        self.profile = pg.generate_profile(self.products)

    def plot_consumer_profile(self):
        print(self.profile)
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
        plt.title(f"Perfil de consumo energético do agente {self.idx}")
        plt.show()
        # fig = plt.figure()
        # s = fig.add_subplot(111)
        # s.bar(np.arange(0.5, 24.5, 1), self.profile)
        # s.plot(np.arange(0, 25, 1), self.conventional_tariff, color='red')
        # s.set_xticks(range(0, 25))
        #
        # plt.ylabel('R$/kWh')
        # plt.xlabel('horário')
        # plt.title("Custos de Tarifa Branca vs. Tarifa Convencional")
        # plt.show()
