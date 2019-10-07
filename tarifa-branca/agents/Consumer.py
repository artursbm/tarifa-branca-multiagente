import numpy as np
from mesa import Agent

from utils.ConsumerProfile import ConsumerProfile


class Consumer(Agent):
    """
    Consumer represents a customer of the energy system. It will have a flag to tell, at the end of the simulations,
    if the agent has adhered to the Tarifa Branca charging model.

    :ivar subscribe: defines the agent status related to the Tarifa Branca program
    (whether the agent have subscribed or not) after simulation step
    :type subscribe: bool

    :ivar flexibility: defines the agent odds of changing its energy consumption habits, given its current habits and the
    Environment characteristics (its Charging curve, for example).
    :type flexibility: float

    :ivar information: defines the level of information from a consumer, which includes its knowledge on simple finance
    math, so it can conclude the advantages of changing to "Tarifa Branca".
    :type information: float

    :ivar knows_white_tariff: defines if an agent knows that "Tarifa Branca" exists; if it doesn't, consumer won't
    change its subscription.
    :type information: bool

    :ivar consumer_profile: defines consumer profile, including product list in a consumer house, and its use along a day.
    :type consumer_profile: Pandas.DataFrame

    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.subscribe_to_white_tariff = False
        self.flexibility = float(np.random.rand())
        self.information = float(np.random.rand())
        self.knows_white_tariff = np.random.choice([True, False], p=[self.information, (1 - self.information)])
        self.consumer_profile = ConsumerProfile(self.unique_id)

    def step(self):
        self.consumer_profile.plot_consumer_profile()
        self.subscribe_to_white_tariff = self.choose_subscription(self)

        if self.subscribe_to_white_tariff:
            print(f'Cons. {self.unique_id} optou por aderir à Tarifa Branca. '
                  f'\n Flexibilidade: {self.flexibility} '
                  f'\n Informação: {self.information} '
                  f'\n Conhece? {self.knows_white_tariff}')
            print('\n')
            self.consumer_profile.generate_new_consumer_profile()
            self.consumer_profile.plot_consumer_profile()
        else:
            print(f'Cons. {self.unique_id} se manterá na Tarifa Convencional.'
                  f'\n Flexibilidade: {self.flexibility} '
                  f'\n Informação: {self.information} '
                  f'\n Conhece? {self.knows_white_tariff}')
            print('\n')

    @staticmethod
    def choose_subscription(self_):
        """
        this method will randomly choose between
        stick with Tarifa Convencional
        subscribe to Tarifa Branca
        """
        # Retrieving environment agent in consumer agent step
        # environment.characteristic_curve.white_tariff
        envi = self_.model.schedule.agents[0]
        if self_.knows_white_tariff:
            # If agent know about "Tarifa Branca", it will then compare costs from it with the conventional tariff
            wt_daily_cost = envi.characteristic_curve.white_tariff['value'] * self_.consumer_profile.profile['value']
            ct_daily_cost = envi.characteristic_curve.conventional_tariff['value'] * self_.consumer_profile.profile['value']

            wt_total_cost = sum(wt_daily_cost)
            ct_total_cost = sum(ct_daily_cost)

            # if agent sees that white tariff cost is bigger than conventional
            # and its information level is high (>=80%), it will opt out from it.
            if wt_total_cost > ct_total_cost and self_.information >= 0.8:
                return False

            elif wt_total_cost <= ct_total_cost and self_.information >= 0.6:
                randomness = np.random.rand()
                if ((self_.flexibility * 3) + (self_.information * 2) + randomness) / 3 >= 0.5:
                    return True

        return False
