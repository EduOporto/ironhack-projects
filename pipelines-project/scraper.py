from bs4 import BeautifulSoup
from bs2json import bs2json
from selenium import webdriver
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def fplayer_scrap(player_id, data_rq, df_to_fill):
    # Key = table, V = columns I need to take from the table 
    tables_cols = {'shooting_df': ["shots_on_target_pct", "goals", "shots_on_target", "shots_total", "shots_total_per90", "shots_on_target_per90", "goals_per_shot", "goals_per_shot_on_target", "average_shot_distance", "shots_free_kicks", "pens_made", "pens_att"],
                   'passing_df': ["passes_pct", "passes_completed", "passes_total_distance", "passes_progressive_distance", "passes_pct_short", "passes_pct_medium", "passes_pct_long" ,"assists", "assisted_shots", "passes_into_final_third", "passes_into_penalty_area", "crosses_into_penalty_area", "progressive_passes"],
                   'defending_df': ["tackles", "tackles_won", "dribble_tackles_pct", "pressure_regain_pct", "blocks", "interceptions", "clearances", "errors"],
                   'dribbling_df': ["dribbles_completed_pct", "players_dribbled_past", "carries", "carry_distance", "carry_progressive_distance", "miscontrols", "dispossessed"],
                   'others_df': ["points_per_match", "plus_minus", "plus_minus_wowy"],
                   'miscel_df': ["cards_yellow", "cards_red", "cards_yellow_red", "fouls", "fouled", "offsides", "crosses", "pens_won", "pens_conceded", "own_goals", "ball_recoveries", "aerials_won_pct"]}

    tab_index = {'shooting_df': 1, 'passing_df': 2, 'defending_df': 5, 'dribbling_df': 6, 'others_df': 7, 'miscel_df': 8}
    index = tab_index[df_to_fill]

    player = BeautifulSoup(data_rq.text, 'html.parser')
    # All tables
    tables = player.find_all('div', {'class': 'section_wrapper'})
    # Convert the table to a json
    converter = bs2json()
    
        # Select the table from the json
    table_s = converter.convert(tables[index])
        # Table as html again
    table = BeautifulSoup(table_s['div']['text'], 'html.parser')
        # Select the table in mode 'Club Collapsed'
    t_collapsed = table.find_all('div', {'class': 'table_wrapper'})[1]
        # Empty list for placing the values to append to the dataframe
    
    values = [player_id]

    for col in tables_cols[df_to_fill]:
            # Select the season 
        row_tag = [season_row for season_row in t_collapsed.find('tbody').find_all('tr') if season_row.find('th', {'data-stat': 'season'}).text == '2018-2019'][0]
        try:
            values.append(float(row_tag.find('td', {'data-stat': col}).text))
        except:
            values.append(0.0)

        # Return list with values
    return values

def gkeeper_scrap(player_id, data_rq, df_to_fill):
    # Key = table, V = columns I need to take from the table 
    tab_equiv = {'goalkeeping_df': 'stats_keeper_ks_collapsed', 'adv_gkeeping_df': 'stats_keeper_adv_ks_collapsed', 
                 'passing_df': 'all_stats_passing_ks_collapsed', 'goal_shoot_c_df': 'stats_gca_ks_collapsed', 
                 'defensive_df': 'stats_defense_ks_collapsed', 'posession_df': 'stats_possession_ks_collapsed', 
                 'playtime_df': 'stats_playing_time_ks_collapsed', 'misc_df': 'stats_misc_ks_collapsed'}
    
    tables_cols = {'stats_keeper_ks_collapsed': ["save_pct", "clean_sheets_pct", "pens_att_gk", "pens_saved"],
                   'stats_keeper_adv_ks_collapsed': ["goals_against_gk", "pens_allowed", "free_kick_goals_against_gk", "corner_kick_goals_against_gk", "own_goals_against_gk", "passes_pct_launched_gk", "pct_passes_launched_gk", "passes_length_avg_gk", "pct_goal_kicks_launched", "goal_kick_length_avg", "crosses_stopped_pct_gk", "def_actions_outside_pen_area_gk", "def_actions_outside_pen_area_per90_gk", "avg_distance_def_actions_gk"], 
                   'all_stats_passing_ks_collapsed': ["passes_pct", "passes_total_distance", "passes_progressive_distance", "passes_pct_short", "passes_pct_medium", "passes_pct_long", "assists", "assisted_shots", "passes_into_final_third"],
                   'stats_gca_ks_collapsed': ["sca", "sca_passes_live", "sca_passes_dead", "gca", "gca_passes_live", "gca_passes_dead"],
                   'stats_defense_ks_collapsed': ["tackles", "tackles_won", "dribble_tackles_pct", "pressure_regain_pct", "blocks", "blocked_shots", "blocked_shots_saves", "blocked_passes", "interceptions", "tackles_interceptions", "clearances", "errors"],
                   'stats_possession_ks_collapsed': ["touches", "touches_live_ball", "dribbles_completed_pct", "carries", "carry_distance", "passes_received_pct", "miscontrols", "dispossessed"],
                   'stats_playing_time_ks_collapsed': ["points_per_match", "plus_minus"],
                   'stats_misc_ks_collapsed': ["cards_yellow", "cards_red", "cards_yellow_red", "fouls", "fouled", "pens_conceded", "own_goals", "ball_recoveries", "aerials_won_pct"]}
    
    df_equiv = tab_equiv[df_to_fill]

    # Searching the soup
    table = data_rq.find_element_by_id(df_equiv)
    selector = data_rq.execute_script("return arguments[0].innerHTML;", table)
    link = BeautifulSoup(selector, 'html.parser')
        
    # Empty list for placing the values to append to the dataframe
    values = [player_id]

    for col in tables_cols[df_equiv]:
        # Select the season 
        row_tag = [row for row in link.find_all('tr') if row.find('th', {'data-stat': 'season'}) != None and row.find('th', {'data-stat': 'season'}).text == '2018-2019'][0]
        try:
            values.append(float(row_tag.find('td', {'data-stat': col}).text))
        except:
            values.append(0.0)
    
    return values

def just_mean(right_df, left_df, name):
    general_df = pd.merge(right_df, left_df, on='sofifa_id')
    general_df[f'mean_{name}'] = (round(general_df.iloc[:,1:].mean(axis=1)*2)*10)
    general_rat = general_df.iloc[:,[0,-1]]
    return general_rat

def bar_plot(dataframe, height_l, height_r):
    f, ax = plt.subplots(1, 2, figsize=(24, 8), sharex=True)
    font = {'weight': 'bold', 'size': 22}
    ax[0].set_title(height_l, **font)
    ax[0].bar(dataframe['short_name'], height=dataframe[height_l])

    ax[1].set_title(height_r, **font)
    ax[1].bar(dataframe['short_name'], height=dataframe[height_r])

    return ax

def scatter_plot(dataframe, x, y, hue=False):
    f, ax = plt.subplots(1, 1, figsize=(12, 9), sharex=True)
    ax.set_xlabel(x, fontsize=18, weight='bold')
    ax.set_ylabel(y, fontsize=15, weight='bold')
    if hue != False:
        sns.scatterplot(data=dataframe, x=x, y=y, hue=hue)
        return ax
    if hue == False: 
        sns.scatterplot(data=dataframe, x=x, y=y)
        return ax

def player_plot(dataframe, player):
    f, ax = plt.subplots(1, 1, figsize=(15, 12), sharex=True)
    font = {'weight': 'bold', 'size': 22}
    ax.set_title(dataframe.iloc[1,player], **font)
    ax.set_xlabel('Specifications', fontsize=18, weight='bold')
    ax.set_ylabel('Rating', fontsize=15, weight='bold')
    
    sns.barplot(x=dataframe.index[5:15], y=dataframe.iloc[5:15,player], palette=['seagreen' if ind%2 == 0 else 'navajowhite' for ind, x in enumerate(list(dataframe.index[5:15]))])

    return ax