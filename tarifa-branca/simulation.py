from timeit import default_timer as timer

import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

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
flex_wtc = list()
info_wtc = list()
flex_wtc_no_habit = list()
info_wtc_no_habit = list()
flex_ctc = list()
info_ctc = list()

for i in all_agents:
    for j, v in i.consumer_profile.profile.iterrows():
        total_charge_consumption_prior_decision[j] += (v['value'] / n_agents)

    if not i.changed_habits:
        for k, vl in i.consumer_profile.profile.iterrows():
            total_charge_consumption_after_decision[k] += (vl['value'] / n_agents)
    else:
        for k, vl in i.consumer_profile.new_profile.iterrows():
            total_charge_consumption_after_decision[k] += (vl['value'] / n_agents)

    if not i.subscribe_to_white_tariff:
        flex_ctc.append(i.flexibility)
        info_ctc.append(i.information)

    if i.subscribe_to_white_tariff and not i.changed_habits:
        flex_wtc_no_habit.append(i.flexibility)
        info_wtc_no_habit.append(i.information)

    if i.subscribe_to_white_tariff:
        white_tariff_consumers += 1
    if i.changed_habits:
        flex_wtc.append(i.flexibility)
        info_wtc.append(i.information)

        wt_cons_habit_changed += 1
        diff_wtc_costs.append({
            "agent": i,
            "id": i.unique_id,
            "diff": abs(i.ctc - i.wtc)})

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
print('\n')

agent_saving_more['agent'].consumer_profile.plot_profile_comparison()

print(f'O Agente que MENOS economizou foi o {agent_saving_less["id"]};'
      f' Valor TB: {agent_saving_less["agent"].wtc};'
      f' Valor Anterior: {agent_saving_less["agent"].ctc}')
print('\n')

agent_saving_less['agent'].consumer_profile.plot_profile_comparison()

# Análises globais
consumption_prior_decision = pd.DataFrame({"time": daytime, "charge": total_charge_consumption_prior_decision})
consumption_after_decision = pd.DataFrame({"time": daytime, "charge": total_charge_consumption_after_decision})

print(f'\n'
      f'{white_tariff_consumers} consumidores aderiram à tarifa Branca ({100 * white_tariff_consumers / n_agents}%);\n'
      f'{wt_cons_habit_changed} consumidores mudaram seus hábitos ({100 * wt_cons_habit_changed / n_agents}%);')

x = ['Tarifa Branca', 'Tarifa Convencional']
y = [white_tariff_consumers, (n_agents - white_tariff_consumers)]
hover = [f'{100 * white_tariff_consumers / n_agents}%', f'{100 * (n_agents - white_tariff_consumers) / n_agents}%']
figP = go.Figure(data=[go.Bar(x=x, y=y, text=hover, textposition='auto')])
figP.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                   marker_line_width=1.5, opacity=0.6)
figP.update_layout(title_text='Proporção de adesão à Tarifa Branca')
plotly.offline.plot(figP, filename='proporcao_adesao.html')

fig = go.Figure()
fig.add_trace(go.Bar(x=daytime,
                     y=consumption_prior_decision['charge'],
                     name='Antes',
                     marker_color='rgb(55, 83, 109)'
                     ))
fig.add_trace(go.Bar(x=daytime,
                     y=consumption_after_decision['charge'],
                     name='Depois',
                     marker_color='rgb(26, 118, 255)'
                     ))
fig.update_layout(
    title='Comparativo de perfil médio de consumo energético da população',
    xaxis_tickfont_size=12,
    xaxis=dict(
        title='Horário',
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    yaxis=dict(
        title='kWh',
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinate.
)
plotly.offline.plot(fig, filename='population_before_after.html')

fig = px.bar(consumption_prior_decision, x='time', y='charge',
             color='charge',
             labels={'time': 'Horário', 'charge': 'kWh'})
fig.update_layout(
    title_text='Consumo médio da População - ANTES',
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    yaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    )
)
plotly.offline.plot(fig, filename='consumption_prior_decision.html')

fig = px.bar(consumption_after_decision, x='time', y='charge',
             color='charge',
             labels={'time': 'Horário', 'charge': 'kWh'})
fig.update_layout(
    title_text='Consumo médio da População - DEPOIS',
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    yaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    )
)
plotly.offline.plot(fig, filename='consumption_after_decision.html')

fig_flex_info = go.Figure()
x = ['TB COM Mudança de hábito', 'TB SEM Mudança de hábito', 'Tarifa Convencional']
y_flex = [round(np.median(flex_wtc), 4), round(np.median(flex_wtc_no_habit), 4), round(np.median(flex_ctc), 4)]
y_info = [round(np.median(info_wtc), 4), round(np.median(info_wtc_no_habit), 4), round(np.median(info_ctc), 4)]

fig_flex_info.add_trace(go.Bar(x=x,
                               y=y_flex,
                               text=y_flex,
                               textposition='auto',
                               name='Flexibilidade',
                               marker_color='rgb(65, 34, 168)'
                               ))
fig_flex_info.add_trace(go.Bar(x=x,
                               y=y_info,
                               text=y_info,
                               textposition='auto',
                               name='Informação',
                               marker_color='rgb(105, 48, 145)'
                               ))
fig_flex_info.update_layout(
    title='Mediana de flexibilidade e informação dos consumidores de acordo com a modalidade de tarifa',
    xaxis_tickfont_size=12,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinate.
)
plotly.offline.plot(fig_flex_info, filename='flex_info_by_mode.html')

fig = go.Figure()
x = ['Consumidor com maior economia', 'Consumidor com menor economia']
y_flex = [agent_saving_more['agent'].flexibility, agent_saving_less['agent'].flexibility]
y_info = [agent_saving_more['agent'].information, agent_saving_less['agent'].information]
fig.add_trace(go.Bar(x=x,
                     y=y_flex,
                     text=y_flex,
                     textposition='auto',
                     name='Flexibilidade',
                     marker_color='rgb(65, 34, 168)'
                     ))
fig.add_trace(go.Bar(x=x,
                     y=y_info,
                     text=y_info,
                     textposition='auto',
                     name='Informação',
                     marker_color='rgb(105, 48, 145)'
                     ))
fig.update_layout(
    title='Flexibilidade e Nível de Informação dos consumidores mais e menos econômicos da Tarifa Branca',
    xaxis_tickfont_size=12,
    legend=dict(
        x=0.5,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinate.
)
plotly.offline.plot(fig, filename='flex_info_agents_less_more.html')

print(f'\nProgram took {end - start} seconds to run.\n END OF EXECUTION')
