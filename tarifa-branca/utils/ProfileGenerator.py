import numpy as np
import pandas as pd
import random


def generate_profile(agent_id):
    print(f"generating profile for agent {agent_id}")
    product_list = open_product_list()
    consumer_products = pd.DataFrame(columns=["Produto", "Consumo (kWh)", "timeOfUse"])

    for index, product in product_list.iterrows():
        # This is to guarantee that at least one of each product will be present in the consumer's list
        quant = np.random.choice(np.arange(1, product["MaxQuant"] + 1)) if product["MaxQuant"] > 1 else 1
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
    if time_range == '[[0,24]]' and hours_of_use == 24:
        return np.arange(0, 25)
    time_arr = time_range.strip('[[').strip(']]').split('],[')
    # case where the array of times of use is bigger than 1
    if len(time_arr) == 1:
        time_arr = time_arr[0].split(',')
        time_arr = [int(t) for t in time_arr]
        if time_arr[0] > time_arr[1]:
            h = time_arr[1] + 25
            time_of_use = random.sample(range(time_arr[0], h), hours_of_use)
            time_of_use = [t-24 if t >= 24 else t for t in time_of_use]
            return np.array(time_of_use, )
        else:
            return np.array(random.sample(range(time_arr[0], time_arr[1]), hours_of_use))
    else:
        return np.arange(16, 21)
