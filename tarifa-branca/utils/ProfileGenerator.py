import random

import numpy as np
import pandas as pd


def generate_product_list(agent_id):
    print(f"Generating profile for agent {agent_id}")
    product_list = open_product_list()
    consumer_products = pd.DataFrame(columns=["idProduto", "Produto", "Consumo (kWh)", "timeOfUse"])

    for index, product in product_list.iterrows():
        # This is to guarantee that at least one of each product will be present in the consumer's list
        quant = np.random.choice(np.arange(1, product["MaxQuant"] + 1)) if product["MaxQuant"] > 1 else 1
        for q in np.arange(quant):
            consumer_products = consumer_products.append({
                "idProduto": product["idProduto"],
                "Produto": product.get_values()[1] + f' {q}',
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
            if hours_of_use > len(range(time[0], time[1] + 1)):
                hours_of_use = random.randint(0, len(range(time[0], time[1] + 1)))
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


def regenerate_profile(products, wt_values, ct_total_cost, flexibility):
    # Must first organize products shuffling the ones used during highest cost tariff, then will redistribute them
    # until the total cost gets lower than the threshold
    products_to_rearrange = pd.DataFrame(columns=["idProduto", "Produto", "Consumo (kWh)", "timeOfUse"])
    products_aux = products.copy(deep=True)
    for i, p in products.iterrows():
        is_peak_time = np.in1d(np.arange(17, 20, 0.5), p["timeOfUse"])
        is_not_all_day = p["timeOfUse"] != np.arange(0, 24.5, 0.5)

        if np.sum(is_not_all_day) != 0 and np.sum(is_peak_time) >= 2:
            products_to_rearrange = products_to_rearrange.append(p)
            products_aux.drop(products_aux[products_aux["Produto"] == p["Produto"]].index, inplace=True)

    products_to_rearrange = products_to_rearrange.sample(frac=1).reset_index(drop=True)

    # while the cost is bigger than conventional tariff or is simply bigger,
    # set new time of use for that product.
    products_to_compare = products.copy()
    iter_ = 0
    wtc = sum(wt_values * generate_profile(products_to_compare)['value'])
    while wtc >= ct_total_cost and iter_ < 2:
        for i, prod in products_to_rearrange.iterrows():
            products_aux = products_aux.append(rearrange_times(prod, flexibility))
            products_to_compare = products_aux.copy()
            products_to_compare = products_to_compare.reset_index()

        iter_ += 1
        wtc = sum(wt_values * generate_profile(products_to_compare)['value'])
        print(f'[Iteration {iter_}] wtc = {wtc}')

    return generate_profile(products_aux.reset_index())


def rearrange_times(product, flexibility):
    product_list = open_product_list()
    prod_ref = product_list.loc[product["idProduto"], :]
    use_range = prod_ref["useRange"].split('],[')
    if len(use_range) == 2:
        # just need the second interval, since it's the only one that contains peak charge time
        range_ = [int(i) for i in use_range[1].strip('[[').strip(']]').split(',')]
    else:
        range_ = [int(i) for i in use_range[0].strip('[[').strip(']]').split(',')]

    range_array = np.arange(range_[0], range_[1] + 0.5, 0.5)
    is_peak_in_range_idx = np.where(np.in1d(range_array, get_peak_range()) == True)[0]
    new_range_array = np.delete(range_array, is_peak_in_range_idx)

    prod_tou = product["timeOfUse"]
    is_peak_in_tou_idx = np.where(np.in1d(prod_tou, get_peak_range()) == True)[0]
    np.random.shuffle(is_peak_in_tou_idx)
    # flexibility % of the time of use will be changed
    number_of_removed_ranges = round(flexibility * len(is_peak_in_tou_idx))
    new_prod_tou = np.delete(prod_tou, is_peak_in_tou_idx[0:number_of_removed_ranges])

    new_choosable_times_idx = np.where(np.in1d(new_range_array, new_prod_tou) == True)[0]
    new_choosable_times = np.delete(new_range_array, new_choosable_times_idx)
    if number_of_removed_ranges < len(new_choosable_times):
        final_prod_tou = np.append(new_prod_tou,
                                   np.array(random.sample(new_choosable_times.tolist(), number_of_removed_ranges)))
        new_prod_tou = final_prod_tou

    new_prod_tou.sort()

    product["timeOfUse"] = new_prod_tou
    return product


def get_peak_range():
    return np.arange(17, 20, 0.5)


def open_product_list():
    return pd.read_csv("./utils/aparelhos_selecionados.csv")
