from timeit import default_timer as timer

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model.MultiAgentModel import MultiAgentModel

# Start of simulation: will make 10 iterations of it with 5 agents

n_agents = 10000

start = timer()
sim_model_white_tariff = MultiAgentModel(n_agents)
end = timer()

sim_model_white_tariff.step()

all_agents = sim_model_white_tariff.schedule.agents[1:n_agents + 1]
daytime = np.arange(0, 24, 0.5)
total_charge_consumption_prior_decision = np.zeros(len(daytime))
total_charge_consumption_after_decision = np.zeros(len(daytime))

white_tariff_consumers = 0
wt_cons_habit_changed = 0
diff_wtc_costs = list()

for i in all_agents:
    for j, v in i.consumer_profile.profile.iterrows():
        total_charge_consumption_prior_decision[j] += (v['value'] / n_agents)

    if not i.changed_habits:
        for k, vl in i.consumer_profile.profile.iterrows():
            total_charge_consumption_after_decision[k] += (vl['value'] / n_agents)
    else:
        for k, vl in i.consumer_profile.new_profile.iterrows():
            total_charge_consumption_after_decision[k] += (vl['value'] / n_agents)

    if i.subscribe_to_white_tariff:
        white_tariff_consumers += 1
    if i.changed_habits:
        wt_cons_habit_changed += 1
        diff_wtc_costs.append({"agent": i, "id": i.unique_id, "diff": abs(i.ctc - i.wtc)})

# Análises locais
diff_wtc_costs = sorted(diff_wtc_costs, key=lambda l: l['diff'])
agent_saving_more = diff_wtc_costs[len(diff_wtc_costs) - 1]
agent_saving_less = diff_wtc_costs[0]
agent_saving_less['agent'].consumer_profile.products.to_csv(
    r'/Users/artursbm/Git/tarifa-branca-multiagente/agent_saving_less.csv')
agent_saving_more['agent'].consumer_profile.products.to_csv(
    r'/Users/artursbm/Git/tarifa-branca-multiagente/agent_saving_more.csv')

print(f'O Agente que MAIS economizou foi o {agent_saving_more["id"]};'
      f' Valor TB: {agent_saving_more["agent"].wtc}; '
      f' Valor Anterior: {agent_saving_more["agent"].ctc}')

agent_saving_more['agent'].consumer_profile.plot_profile_comparison()

print(f'O Agente que MENOS economizou foi o {agent_saving_less["id"]};'
      f' Valor TB: {agent_saving_less["agent"].wtc};'
      f' Valor Anterior: {agent_saving_less["agent"].ctc}')

agent_saving_less['agent'].consumer_profile.plot_profile_comparison()

# Análises globais
consumption_prior_decision = pd.DataFrame({"time": daytime, "charge": total_charge_consumption_prior_decision})
consumption_after_decision = pd.DataFrame({"time": daytime, "charge": total_charge_consumption_after_decision})

print(f'\n'
      f'{white_tariff_consumers} consumidores aderiram à tarifa Branca ({100 * white_tariff_consumers / n_agents}%);\n'
      f'{wt_cons_habit_changed} consumidores mudaram seus hábitos ({100 * wt_cons_habit_changed / n_agents}%);')

fig = plt.figure()
s = fig.add_subplot(111)
s.set_xticks(range(0, 25))
s.set_yticks(np.arange(0, 21, 0.75))
s.bar(consumption_prior_decision['time'], consumption_prior_decision['charge'],
      align='edge',
      color='red',
      label='Consumo horário')
s.legend()
plt.ylabel('kWh')
plt.xlabel('Horário')
plt.title(f"Perfil de consumo energético da população")
plt.show()

fig2 = plt.figure()
s2 = fig2.add_subplot(111)
s2.set_xticks(range(0, 25))
s2.set_yticks(np.arange(0, 21, 0.75))
s2.bar(consumption_prior_decision['time'], consumption_after_decision['charge'],
       align='edge',
       color='blue',
       label='Consumo horário')
s2.legend()
plt.ylabel('kWh')
plt.xlabel('Horário')
plt.title(f"Perfil de consumo energético da população após decisões")
plt.show()

# TODO: plot graphics for some agents that changed habits
# self.consumer_profile.plot_profile_comparison()

print(f'\nProgram took {end - start} seconds to run.\n END OF EXECUTION')
