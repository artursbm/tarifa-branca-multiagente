from model.MultiAgentModel import MultiAgentModel

# Start of simulation: will make 10 iterations of it with 5 agents

# for i in range(10):
sim_model = MultiAgentModel(5)
sim_model.step()
print('\n')

