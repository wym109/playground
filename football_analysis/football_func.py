import pandas as pd
import numpy as np
from scipy.stats import poisson 
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from fuzzywuzzy import process, fuzz
import time
import pickle

def calculate_strength(dict_historical_data, league):
    home = dict_historical_data[league][['HomeTeam', 'HomeGoals', 'AwayGoals']].rename(
        columns={'HomeTeam':'Team', 'HomeGoals':'HomeScored', 'AwayGoals':'HomeConceded'}).groupby(
        ['Team'], as_index=False)[['HomeScored', 'HomeConceded']].mean()
    away = dict_historical_data[league][['AwayTeam', 'HomeGoals', 'AwayGoals']].rename(
        columns={'AwayTeam':'Team', 'HomeGoals':'AwayConceded', 'AwayGoals':'AwayScored'}).groupby(
        ['Team'], as_index=False)[['AwayScored', 'AwayConceded']].mean()

    df_league_strength = pd.merge(home, away, on='Team')
    average_home_scored, average_home_conceded = home['HomeScored'].mean(), home['HomeConceded'].mean()
    average_away_scored, average_away_conceded = away['AwayScored'].mean(), away['AwayConceded'].mean()

    df_league_strength['HomeScored'] /= average_home_scored
    df_league_strength['HomeConceded'] /= average_home_conceded
    df_league_strength['AwayScored'] /= average_away_scored
    df_league_strength['AwayConceded'] /= average_away_conceded

    df_league_strength.set_index('Team', inplace=True)
    return df_league_strength


def predict_points(df_league_strength, home, away):
    if home in df_league_strength.index and away in df_league_strength.index:
        #home_scored * away_conceded
        lamb_home = df_league_strength.at[home,'HomeScored'] * df_league_strength.at[away,'AwayConceded']
        lamb_away = df_league_strength.at[away,'AwayScored'] * df_league_strength.at[home,'HomeConceded']
        prob_home, prob_away, prob_draw = 0, 0, 0
        for x in range(0,11): #number of goals home team
            for y in range(0, 11): #number of goals away team
                p = poisson.pmf(x, lamb_home) * poisson.pmf(y, lamb_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p
        
        points_home = 3 * prob_home + prob_draw
        points_away = 3 * prob_away + prob_draw
        return (points_home, points_away)
    else:
        return (0, 0)