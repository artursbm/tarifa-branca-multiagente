from model.MultiAgentModel import MultiAgentModel

# Start of simulation: will make 10 iterations of it with 5 agents

n_agents = 100

sim_model_white_tariff = MultiAgentModel(n_agents)

sim_model_white_tariff.step()

a = sim_model_white_tariff.schedule.agents[1:n_agents+1]
white_tariff_consumers = 0
wt_cons_habit_changed = 0
for i in a:
    if i.subscribe_to_white_tariff:
        white_tariff_consumers += 1
    if i.changed_habits:
        wt_cons_habit_changed += 1


print(f'{white_tariff_consumers} consumidores aderiram à tarifa Branca ({100*white_tariff_consumers/n_agents}%) \n '
      f'e {wt_cons_habit_changed} consumidores mudaram seus hábitos ({100*wt_cons_habit_changed/n_agents}%)')

