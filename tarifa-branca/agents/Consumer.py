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
        self.changed_habits = False

    def step(self):
        # Retrieving environment agent in consumer agent step
        # environment.characteristic_curve.white_tariff
        envi = self.model.schedule.agents[0]
        wtc = envi.characteristic_curve.white_tariff['value'] * self.consumer_profile.profile['value']
        ctc = envi.characteristic_curve.conventional_tariff['value'] * self.consumer_profile.profile[
            'value']

        self.consumer_profile.plot_consumer_profile()
        self.subscribe_to_white_tariff = self.choose_subscription(self.information, self.flexibility,
                                                                  self.knows_white_tariff, wtc, ctc)

        if self.subscribe_to_white_tariff:
            print(f'Cons. {self.unique_id} optou por aderir à Tarifa Branca. '
                  f'\n Flexibilidade: {self.flexibility} '
                  f'\n Informação: {self.information} '
                  f'\n Conhece? {self.knows_white_tariff}'
                  f'\n Valor Tarifa Convencional: {sum(ctc)}'
                  f'\n Valor da Tarifa Branca: {sum(wtc)}')
            if sum(wtc) >= sum(ctc):
                # if cost of white tariff is already lower than conventional, user will stick with its habits.
                self.consumer_profile.generate_new_consumer_profile(envi, self.flexibility)
                new_wtc = envi.characteristic_curve.white_tariff['value'] * self.consumer_profile.new_profile['value']
                self.changed_habits = True
                print(f'Valor da Tarifa Branca: {sum(new_wtc)}')
            else:
                self.consumer_profile.copy_profile()

            self.consumer_profile.plot_consumer_new_profile()

        else:
            print(f'Cons. {self.unique_id} se manterá na Tarifa Convencional.'
                  f'\n Flexibilidade: {self.flexibility} '
                  f'\n Informação: {self.information} '
                  f'\n Conhece? {self.knows_white_tariff}'
                  f'\n Valor da Tarifa Convencional: {sum(ctc)}'
                  f'\n Valor da Tarifa Branca: {sum(wtc)}')
            print('\n')

    @staticmethod
    def choose_subscription(info, flex, knows_wt, wtc, ctc):
        """
        this method will randomly decide between
        stick with Tarifa Convencional
        subscribe to Tarifa Branca
        """

        if knows_wt:
            # If agent know about "Tarifa Branca", it will then compare costs from it with the conventional tariff
            wt_total_cost = sum(wtc)
            ct_total_cost = sum(ctc)

            # if agent sees that white tariff cost is bigger than conventional
            # and its information level is high (>=80%), it will opt out from it.
            if wt_total_cost > ct_total_cost and flex <= 0.4 and info >= 0.8:
                return False

            elif wt_total_cost <= ct_total_cost or info >= 0.6:
                randomness = np.random.rand()
                if ((flex * 3) + (info * 2) + randomness) / 2 >= 0.5:
                    return True

        return False
