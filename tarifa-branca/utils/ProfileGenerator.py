import random

import pandas as pd


def generate_profile(agent_id):
    print("generating profile for agent " + str(agent_id))
    product_list = open_product_list()
    consumer_products = create_consumer_products()

    for product in product_list.get_values():
        consumer_products.append(map_product_to_consumer(product))

    return consumer_products


def open_product_list():
    return pd.read_csv("./utils/aparelhos_selecionados.csv")


def create_consumer_products():
    # initialize empty consumer product profile with defined columns
    return pd.DataFrame(["Produto", "Quantidade", "Consumo (kWh)", "timeOfUse"])


def map_product_to_consumer(product):
    return {
        "Produto": product["Produto"],
        "Quantidade": random.randrange(product["MaxQuant"]),
        "Consumo (kWh)": product["Consumo (kWh)"],
        "timeOfUse": choose_time_of_use(product["Intervalos de uso"], product["horasDia"])

    }


def choose_time_of_use(time_interval, hours_of_use):
    return [1, 3, 20]
