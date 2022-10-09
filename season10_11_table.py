import pandas as pd
import numpy as np

epl = pd.read_csv('input_data/df_full_premierleague.csv', index_col=0)

epl.head()
epl.shape
# The table contains 36 columns and 4070 rows with data.

# Sorting the data by date
sorted_epl = epl.sort_values(by=['date', 'home_team'], ascending=True)
sorted_epl = sorted_epl.reset_index(drop=True)
sorted_epl.index += 1
sorted_epl.index

# Season 2010/2011:
season10_11 = sorted_epl.loc[sorted_epl['season'] == '10/11']
season10_11

# Team names:
teams_names = season10_11['home_team'].unique()
teams_names

# Results from 380 this season games:
season10_11_results = season10_11.loc[:, [
    'home_team', 'away_team', 'result_full']]

sr = season10_11_results

# Assigning new columns with the goals and points for each game:
new_columns = ['home_team_goals', 'away_team_goals',
               'home_team_points', 'away_team_points']
home_team_goals_list, away_team_goals_list, home_team_points_list, away_team_points_list = [], [], [], []
list_of_stats = [home_team_goals_list, away_team_goals_list,
                 home_team_points_list, away_team_points_list]

for row in sr.itertuples(index=False):
    home_team_goals = int(row[2].split('-')[0])
    away_team_goals = int(row[2].split('-')[1])
    if home_team_goals > away_team_goals:
        home_team_points = 3
        away_team_points = 0
    elif home_team_goals < away_team_goals:
        home_team_points = 0
        away_team_points = 3
    else:
        home_team_points = 1
        away_team_points = 1
    home_team_goals_list.append(home_team_goals)
    away_team_goals_list.append(away_team_goals)
    home_team_points_list.append(home_team_points)
    away_team_points_list.append(away_team_points)

i = 0
for column in new_columns:
    sr[column] = list_of_stats[i]
    i += 1

# Creating the league table:
league_table = pd.DataFrame(columns=['Team', 'Games Played', 'Wins', 'Draws',
                            'Loses', 'GS', 'GC', 'GD', 'Points'])

# Creating dictionaries with team stats:
team_stats = dict()

# Creating stats for each team:
for team in teams_names:
    team_points = sr.loc[sr['home_team'] == team, 'home_team_points'].sum(
    ) + sr.loc[sr['away_team'] == team, 'away_team_points'].sum()
    team_goals_scored = sr.loc[sr['home_team'] == team, 'home_team_goals'].sum(
    ) + sr.loc[sr['away_team'] == team, 'away_team_goals'].sum()
    team_goals_conceded = sr.loc[sr['home_team'] == team, 'away_team_goals'].sum(
    ) + sr.loc[sr['away_team'] == team, 'home_team_goals'].sum()

    team_goal_difference = team_goals_scored - team_goals_conceded

    team_wins = ((sr['home_team'] == team) & (sr['home_team_points'] == 3)).values.sum(
    ) + ((sr['away_team'] == team) & (sr['away_team_points'] == 3)).values.sum()
    team_loses = ((sr['home_team'] == team) & (sr['home_team_points'] == 0)).values.sum(
    ) + ((sr['away_team'] == team) & (sr['away_team_points'] == 0)).values.sum()
    team_draws = ((sr['home_team'] == team) & (sr['home_team_points'] == 1)).values.sum(
    ) + ((sr['away_team'] == team) & (sr['away_team_points'] == 1)).values.sum()
    team_games = team_wins + team_draws + team_loses

    # Creating dictionary with team stats:
    team_stats[team] = {'Team': team,
                        'Games Played': team_games,
                        'Wins': team_wins,
                        'Draws': team_draws,
                        'Loses': team_loses,
                        'GS': team_goals_scored,
                        'GC': team_goals_conceded,
                        'GD': team_goal_difference,
                        'Points': team_points}

    team_stats

    # Appending the team stats into the league table:
    league_table = league_table.append(team_stats[team], ignore_index=True)
league_table

end_league_table = league_table.sort_values(
    by=['Points', 'GD'], ascending=False)
end_league_table = end_league_table.reset_index(drop=True)
end_league_table.index += 1
end_league_table

print(end_league_table.to_string())
end_league_table.to_csv(r'output_data.csv', header=True, index=True, sep=',')