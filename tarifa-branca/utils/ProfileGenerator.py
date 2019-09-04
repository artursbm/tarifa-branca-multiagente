import pandas as pd
import numpy as np


def generate_profile(agent_id):
    print(f"generating profile for agent {agent_id}")
    product_list = open_product_list()
    consumer_products = pd.DataFrame(columns=["Produto", "Consumo (kWh)", "timeOfUse"])

    for index, product in product_list.iterrows():
        # This is to guarantee that at least one of each product will be present in the consumer's list
        quant = np.random.choice(np.arange(1, product["MaxQuant"]+1)) if product["MaxQuant"] > 1 else 1
        for q in np.arange(quant):
            consumer_products = consumer_products.append({
                "Produto": product.get_values()[0],
                "Consumo (kWh)": product["Consumo (kWh)"],
                "timeOfUse": choose_time_of_use(product["horasDia"], product["useRange"])
            }, ignore_index=True)

    return consumer_products


def open_product_list():
    return pd.read_csv("./utils/aparelhos_selecionados.csv")


def choose_time_of_use(hours_of_use, time_range):
    return [1, 3, 20]

