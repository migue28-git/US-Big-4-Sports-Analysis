import pandas as pd
import scipy.stats as stats
import numpy as np
import re

nhl_df = pd.read_csv("assets/nhl.csv")
nba_df = pd.read_csv("assets/nba.csv")
nfl_df = pd.read_csv("assets/nfl.csv")
mlb_df = pd.read_csv("assets/mlb.csv")
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]


def nhl_correlation():
    nhl_df = pd.read_csv("assets/nhl.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

    nhl_df = nhl_df.iloc[[bool(re.match('\d*', x).group()) for x in nhl_df['W']]]
    nhl_df = nhl_df.set_index('team')
    nhl_df = nhl_df[['W', 'L', 'year']]
    nhl_df = nhl_df.astype(int)
    nhl_df = nhl_df[nhl_df['year'] == 2018]
    nhl_df['W Ratio'] = nhl_df['W'] / (nhl_df['W'] + nhl_df['L'])
    cities = cities.set_index('Metropolitan area')
    cities['NHL'] = [re.sub("[\(\[].*?[\)\]]", "", x) for x in cities['NHL']]
    W_R = []
    for teams in cities['NHL']:
        l = re.findall('[A-Z][a-z]*\ [A-Z][a-z]*|[A-Z][a-z]*', teams)
        ratio = []
        for team in l:
            for i in nhl_df.index:
                if bool(re.search('%s' % team, i)):
                    ratio.append(nhl_df['W Ratio'][i])
                    break
        if len(ratio) == 0:
            W_R.append(0)
        else:
            W_R.append(np.mean(ratio))
    cities['Win Ratio'] = W_R
    cities = cities[['Population (2016 est.)[8]', 'NHL', 'Win Ratio']]
    cities = cities[cities['Win Ratio'] != 0]
    population_by_region = cities['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    population_by_region = population_by_region.astype(int)
    win_loss_by_region = cities['Win Ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


def nba_correlation():
    nba_df = pd.read_csv("assets/nba.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

    nba_df = nba_df.set_index('team')
    nba_df = nba_df[['W', 'L', 'year', 'W/L%']]
    nba_df = nba_df[nba_df['year'] == 2018]
    nba_df = nba_df.astype(float)
    nba_df['W Ratio'] = nba_df['W'] / (nba_df['W'] + nba_df['L'])
    cities = cities.set_index('Metropolitan area')
    cities['NBA'] = [re.sub("[\(\[].*?[\)\]]", "", x) for x in cities['NBA']]
    W_R = []
    for teams in cities['NBA']:
        l = re.findall('[A-Z][a-z]*\ [A-Z][a-z]*|[A-Z][a-z]*|76ers', teams)
        ratio = []
        for team in l:
            for i in nba_df.index:
                if (bool(re.search('%s' % team, i))):
                    ratio.append(nba_df['W Ratio'][i])
                    break
        if (len(ratio) == 0):
            W_R.append(0)
        else:
            W_R.append(np.mean(ratio))
    cities['Win Ratio'] = W_R
    cities = cities[['Population (2016 est.)[8]', 'NBA', 'Win Ratio']]
    cities = cities[cities['Win Ratio'] != 0]
    population_by_region = cities['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    population_by_region = population_by_region.astype(int)
    win_loss_by_region = cities[
        'Win Ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


def mlb_correlation():
    mlb_df = pd.read_csv("assets/mlb.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

    mlb_df = mlb_df.set_index('team')
    mlb_df = mlb_df[['W', 'L', 'year', 'W-L%']]
    mlb_df = mlb_df[mlb_df['year'] == 2018]
    mlb_df = mlb_df.astype(float)
    mlb_df['W Ratio'] = mlb_df['W'] / (mlb_df['W'] + mlb_df['L'])
    cities = cities.set_index('Metropolitan area')
    cities['MLB'] = [re.sub("[\(\[].*?[\)\]]", "", x) for x in cities['MLB']]
    W_R = []
    for teams in cities['MLB']:
        l = re.findall('[A-Z][a-z]*\ [A-Z][a-z]*|[A-Z][a-z]*', teams)
        ratio = []
        for team in l:
            for i in mlb_df.index:
                if (bool(re.search('%s' % team, i))):
                    ratio.append(mlb_df['W Ratio'][i])
                    break
        if (len(ratio) == 0):
            W_R.append(0)
        else:
            W_R.append(np.mean(ratio))
    cities['Win Ratio'] = W_R
    cities = cities[['Population (2016 est.)[8]', 'MLB', 'Win Ratio']]
    cities = cities[cities['Win Ratio'] != 0]
    population_by_region = cities['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    population_by_region = population_by_region.astype(int)
    win_loss_by_region = cities[
        'Win Ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


def nfl_correlation():

    nfl_df = pd.read_csv("assets/nfl.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

    nfl_df = nfl_df.set_index('team')
    nfl_df = nfl_df[['W', 'L', 'year', 'W-L%']]
    nfl_df = nfl_df[nfl_df['year'] == 2018]
    nfl_df = nfl_df.iloc[[bool(re.match('\d*', x).group()) for x in nfl_df['W']]]
    nfl_df = nfl_df.astype(float)
    nfl_df['W Ratio'] = nfl_df['W'] / (nfl_df['W'] + nfl_df['L'])
    cities = cities.set_index('Metropolitan area')
    cities['NFL'] = [re.sub("[\(\[].*?[\)\]]", "", x) for x in cities['NFL']]
    W_R = []
    for teams in cities['NFL']:
        l = re.findall('[A-Z][a-z]*\ [A-Z][a-z]*|[A-Z][a-z]*', teams)
        ratio = []
        for team in l:
            for i in nfl_df.index:
                if (bool(re.search('%s' % team, i))):
                    ratio.append(nfl_df['W Ratio'][i])
                    break
        if (len(ratio) == 0):
            W_R.append(0)
        else:
            W_R.append(np.mean(ratio))
    cities['Win Ratio'] = W_R
    cities = cities[['Population (2016 est.)[8]', 'NFL', 'Win Ratio']]
    cities = cities[cities['Win Ratio'] != 0]
    population_by_region = cities['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    population_by_region = population_by_region.astype(int)
    win_loss_by_region = cities[
        'Win Ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


def sports_team_performance():
    nhl_df = pd.read_csv("assets/nhl.csv")
    nba_df = pd.read_csv("assets/nba.csv")
    nfl_df = pd.read_csv("assets/nfl.csv")
    mlb_df = pd.read_csv("assets/mlb.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
    ######################## NHL ########################################
    nhl_df = nhl_df.iloc[[bool(re.match('\d*', x).group()) for x in nhl_df['W']]]
    nhl_df = nhl_df.set_index('team')
    nhl_df = nhl_df[['W', 'L', 'year']]
    nhl_df = nhl_df.astype(int)
    nhl_df = nhl_df[nhl_df['year'] == 2018]
    nhl_df['W Ratio'] = nhl_df['W'] / (nhl_df['W'] + nhl_df['L'])
    ######################################################################

    ######################## NBA ########################################
    nba_df = nba_df.set_index('team')
    nba_df = nba_df[['W', 'L', 'year', 'W/L%']]
    nba_df = nba_df[nba_df['year'] == 2018]
    nba_df = nba_df.astype(float)
    nba_df['W Ratio'] = nba_df['W'] / (nba_df['W'] + nba_df['L'])
    ######################################################################

    ######################## NFL ########################################
    nfl_df = nfl_df.set_index('team')
    nfl_df = nfl_df[['W', 'L', 'year', 'W-L%']]
    nfl_df = nfl_df[nfl_df['year'] == 2018]
    nfl_df = nfl_df.iloc[[bool(re.match('\d*', x).group()) for x in nfl_df['W']]]
    nfl_df = nfl_df.astype(float)
    nfl_df['W Ratio'] = nfl_df['W'] / (nfl_df['W'] + nfl_df['L'])
    ######################################################################

    ######################## MLB ########################################
    mlb_df = mlb_df.set_index('team')
    mlb_df = mlb_df[['W', 'L', 'year', 'W-L%']]
    mlb_df = mlb_df[mlb_df['year'] == 2018]
    mlb_df = mlb_df.astype(float)
    mlb_df['W Ratio'] = mlb_df['W'] / (mlb_df['W'] + mlb_df['L'])
    ######################################################################

    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    dfs = {'NFL':nfl_df, 'NBA':nba_df, 'NHL':nhl_df, 'MLB':mlb_df}
    for i in cities:
        cities[i] = [re.sub("[\(\[].*?[\)\]]", "", x) for x in cities[i]]
    cities.set_index('Metropolitan area',inplace=True)

    for i in sports:
        W_R = []
        for teams in cities[i]:
            l = re.findall('[A-Z][a-z]*\ [A-Z][a-z]*|[A-Z][a-z]*|76ers', teams)
            ratio = []
            for team in l:
                for w in dfs[i].index:
                    if bool(re.search('%s' % team, w)):
                        ratio.append(dfs[i]['W Ratio'][w])
                        break
            if len(ratio) == 0:
                W_R.append(0)
            else:
                W_R.append(np.mean(ratio))

        cities[i + ' Win Ratio'] = W_R

    cities = cities[cities.columns[-4:]]
    p_values = pd.DataFrame(index=sports)
    for i in sports:
        c = cities
        p_v = []
        for x in sports:
            c = c[(c[i + ' Win Ratio'] != 0) & (c[x + ' Win Ratio'] != 0)]
            p_v.append(stats.ttest_rel(c[i + ' Win Ratio'],c[x + ' Win Ratio'])[1])
        p_values[i] = p_v
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values


