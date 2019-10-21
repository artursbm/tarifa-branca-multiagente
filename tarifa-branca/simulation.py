from model.MultiAgentModel import MultiAgentModel

# Start of simulation: will make 10 iterations of it with 5 agents

# for i in range(10):
sim_model_white_tariff = MultiAgentModel(1000)

sim_model_white_tariff.step()

a = sim_model_white_tariff.schedule.agents[1:1000]
b = 0
c = 0
for i in a:
    if i.subscribe_to_white_tariff:
        b += 1
    if i.changed_habits:
        c += 1

print(f'{b} consumidores aderiram à tarifa Branca \n e {c} consumidores mudaram seus hábitos')
