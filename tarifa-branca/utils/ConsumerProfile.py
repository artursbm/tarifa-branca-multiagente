import utils.ProfileGenerator as pg


class ConsumerProfile:
    def __init__(self, agent_id):
        self.idx = agent_id
        self.profile = pg.generate_profile(self.idx)

    def plot_consumer_profile(self):
        print(self.profile.head())
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
