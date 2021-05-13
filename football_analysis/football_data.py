import pandas as pd
import numpy as np
from scipy.stats import poisson 
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from fuzzywuzzy import process, fuzz
import time
import pickle

from football_func import *

# downloading series script
# dict_historical_data = pickle.load(open('dict_historical_data','rb'))
# dict_matches_left = pickle.load(open('dict_matches_left','rb'))
dict_matches_left = {}
dict_table = {}

dict_matches_left['E0'] = pd.read_csv('premier_league_matches_left.csv')
dict_table['E0'] = pd.read_csv('premier_league_table.csv')
# dict_table = pickle.load(open('dict_table','rb'))

leagues_short = ['SP1', 'D1', 'E0', 'I1'] #spanish league, bundesliga, premier league, 
dict_historical_data = {}

for league in leagues_short:
    frames = []
    for i in range(15, 21):
        df = pd.read_csv("http://www.football-data.co.uk/mmz4281/"+str(i)+str(i+1)+"/"+league+".csv")
        df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
        df = df.rename(columns={'FTHG': 'HomeGoals', 'FTAG': 'AwayGoals'})
        df = df.assign(Season=i)
        frames.append(df)
    df_historical_data = pd.concat(frames)
    df_historical_data['Date'] = pd.to_datetime(df_historical_data['Date'])
    dict_historical_data[league] = df_historical_data


for i in dict_historical_data:
    dict_historical_data[i]['TotalGoals'] = dict_historical_data[i]['HomeGoals'] + dict_historical_data[i]['AwayGoals']

for i in dict_historical_data:
    print(i)
    print(dict_historical_data[i]['TotalGoals'].mean())

for i in dict_historical_data:
    dict_historical_data[i] = dict_historical_data[i].loc[dict_historical_data[i]['Season'] >= 15]


#  Simulate the matches to predict final standings
league = 'E0' #'la_liga', 'premier_league', 'bundesliga', 'serie_a'
df_league_strength = calculate_strength(dict_historical_data, league)

list_points_home = []
list_points_away = []
for index, row in dict_matches_left[league].iterrows():
    home, away = row['HomeTeam'], row['AwayTeam']
    points_home, points_away = predict_points(df_league_strength, home, away)
    dict_table[league].loc[dict_table[league]['Team'] == home, 'Points'] += points_home
    dict_table[league].loc[dict_table[league]['Team'] == away, 'Points'] += points_away
    #storing every match result
    list_points_home.append(round(points_home, 1))
    list_points_away.append(round(points_away, 1))
    
dict_table[league] = dict_table[league].sort_values('Points', ascending=False).reset_index()
dict_table[league] = dict_table[league][['Team', 'Points']]
dict_table[league].round(0)

print(dict_table[league])

# fig, ax = plt.subplots(nrows=2, ncols=2)
# i=0
# for row in ax:
#     for col in row:
#         dict_plot = {0:'SP1', 1:'D1', 2:'E0', 3:'I1'}
#         dict_colors = {0:'skyblue', 1:'#3D195B', 2:'lightcoral', 3:'lightgreen'}
#         data = dict_historical_data[dict_plot[i]]['TotalGoals']
#         # the bins should be of integer width (poisson is an integer distribution)
#         bins = np.arange(11) - 0.5
#         entries, bin_edges, patches = col.hist(data, bins=bins, density=True, label=dict_plot[i], color=dict_colors[i])
#         bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])

#         #curve
#         def fit_function(x, lamb):
#             """Poisson function.Lamb is the fit parameter"""
#             return poisson.pmf(x, lamb)
#         parameters, cov_matrix = curve_fit(fit_function, bin_middles, entries) #optimal parameters
#         x_plot = np.arange(0, 11)
#         col.plot(x_plot, fit_function(x_plot, *parameters),marker='o', linestyle='--',
#                  label='Fit result',)
#         col.legend()
#         i+=1

# fig.set_size_inches(20, 10.5)
# fig.text(0.5, 0.005, 'Total Goals', ha='center', size=20)
# fig.text(0.005, 0.5, 'Density', va='center', rotation='vertical', size=20)
# fig.tight_layout()
# fig.show()
# fig.savefig('histogram.png')

