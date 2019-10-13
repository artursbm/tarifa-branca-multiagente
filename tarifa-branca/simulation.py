from model.MultiAgentModel import MultiAgentModel

# Start of simulation: will make 10 iterations of it with 5 agents

# for i in range(10):
sim_model_white_tariff = MultiAgentModel(1)

sim_model_white_tariff.step()

# a = sim_model_white_tariff.schedule.agents[1:100]
# b = 0
# for i in a:
#     if i.subscribe_to_white_tariff:
#         b += 1
#
# print(f'{b} consumidores aderiram à tarifa Branca')
