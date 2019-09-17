import random

import numpy as np
import pandas as pd


def generate_product_list(agent_id):
    print(f"generating profile for agent {agent_id}")
    product_list = open_product_list()
    consumer_products = pd.DataFrame(columns=["Produto", "Consumo (kWh)", "timeOfUse"])

    for index, product in product_list.iterrows():
        # This is to guarantee that at least one of each product will be present in the consumer's list
        quant = np.random.choice(np.arange(1, product["MaxQuant"] + 1)) if product["MaxQuant"] > 1 else 1
        for q in np.arange(quant):
            consumer_products = consumer_products.append({
                "Produto": product.get_values()[0] + f' {q}',
                "Consumo (kWh)": product["Consumo (kWh)"],
                "timeOfUse": choose_time_of_use(product["horasDia"], product["useRange"])
            }, ignore_index=True)

    return consumer_products


def generate_profile(products):
    products_time_of_use = products["timeOfUse"]
    products_consumption = products["Consumo (kWh)"]
    daytime = np.arange(0, 24, 0.5)
    day_consumption_profile = np.zeros(len(daytime))
    j = 0
    for tou in products_time_of_use:
        for i in daytime:
            if i in tou:
                day_consumption_profile[np.where(daytime == i)] += products_consumption[j]
        j += 1

    return pd.DataFrame({"time": daytime, "value": day_consumption_profile})


def open_product_list():
    return pd.read_csv("./utils/aparelhos_selecionados.csv")


def choose_time_of_use(hours_of_use, time_range):
    if time_range == '[[0,24]]' and hours_of_use == 24:
        return np.arange(0, 24.5, 0.5)
    time_arr = time_range.strip('[[').strip(']]').split('],[')
    # case where the array of times of use is bigger than 1
    if len(time_arr) == 1:
        time_arr = time_arr[0].split(',')
        time_arr = [int(t) for t in time_arr]
        if time_arr[0] > time_arr[1]:
            h = time_arr[1] + 25
            tou = random.sample(range(time_arr[0], h), hours_of_use)
            tou = [t - 24 if t >= 24 else t for t in tou]
            return np.array(generate_time_of_use_range(tou))
        else:
            return generate_time_of_use_range(random.sample(range(time_arr[0], time_arr[1] + 1), hours_of_use))

    else:
        final_time_range = list()

        for tm in time_arr:
            time = tm.split(',')
            time = [int(t) for t in time]
            res = np.array(random.sample(range(time[0], time[1] + 1), hours_of_use))
            final_time_range.extend(res)

        tou = np.array(random.sample(final_time_range, hours_of_use))
        return generate_time_of_use_range(tou.tolist())


def generate_time_of_use_range(time_of_use):
    tou = time_of_use
    time_of_use.extend([r - 0.5 for r in tou if r > 0])
    time_of_use.extend([r + 0.5 for r in tou if r + 0.5 not in time_of_use])
    time_of_use.sort()
    return np.array(time_of_use)
