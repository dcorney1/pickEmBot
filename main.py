import os
import re
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from groupme_interface import basic_text_msg
import functions_framework
load_dotenv()

START_URL = os.getenv('START_URL')


def get_winner(result):
    if result['result'] != 'F':
        return None
    if result['score2'] > result['score1']:
        return result['t2'], result['t1']
    if result['score1'] > result['score2']:
        return result['t1'], result['t2']
    return None


def handle_group_me(json_val):
    pass


@functions_framework.http
def main(request):
    json_val = request.get_json()
    if json_val.get("group_id") == '70879853' and json_val.get("sender_type") != 'BOT':
        handle_group_me(json_val)
        return "SETUP TO HANDLE NON BOT MESSAGING"

    message = json_val.get("message")
    if not message or not message.get("attributes"):
        return "THIS IS AN UNHANDLEABLE MESSAGE"

    job = message.get("attributes")
    headers = json.load(open(r'./headers.json'))
    response = requests.request("GET", START_URL, headers=headers, data={})
    picks_dict = json.loads(re.findall(r'(var|let|const)\s+(opmLS)\s*=.*?({.*})', response.text)[0][2])
    teams = picks_dict['teams']
    not_picked = [team['name'] for team in teams if not team.get("picks")]

    if job.get("type") == "PICKS" and not_picked:
        basic_text_msg(f"Can the following players please make their picks: {', '.join(not_picked)}")
        return "PICKS MESSAGE SENT"

    if job.get("type") != "UPDATE":
        return "THERE IS NOTHING TO UPDATE"

    results_list = [
        item.split('|') for item in re.findall(r'NFL_(.*?)\\n', re.findall(r'opmLS.loadState.*?;', response.text)[0])
    ]
    results_list_of_dicts = [
        {
            'game': result[0].split('_')[1],
            't1': result[0].split('_')[1].split('@')[0],
            't2': result[0].split('_')[1].split('@')[1],
            'result': result[1],
            'quarter': int(result[2]),
            'time_left': result[5],
            'date': result[6].split(' ')[0],
            'start_time': result[6].split(' ')[1],
            'score1': int(result[10]),
            'score2': int(result[11])
        } for result in results_list
    ]
    results_df = pd.DataFrame(results_list_of_dicts)
    results_df.set_index('game', inplace=True)
    results_df['winner'] = results_df.apply(get_winner, axis=1)

    data = [{'id': team['id'], 'name': team['name'], 'picks': team['picks']} for team in teams]
    picks_list = []

    for entry in data:
        cbs_id = entry['id']
        name = entry['name']
        picks = entry['picks']
        for game, values in picks.items():
            if type(values) is dict:
                choice = values['winner']
                weight = int(values['weight'])
                picks_list.append(
                    {'cbs_id': cbs_id, 'name': name, 'game': game.split('_')[1], 'choice': choice, 'weight': weight}
                )
    picks_df = pd.DataFrame(picks_list)
    scores_df = picks_df.join(results_df, on='game', how='inner')
    scores_df.to_csv(r'./output.csv', index=False)

    potential_points_df = scores_df[
        (scores_df['winner'] == scores_df['choice']) | pd.isna(scores_df['winner'])
    ].groupby('name')['weight'].sum().reset_index()

    points_scored_df = scores_df[
        (scores_df['winner'] == scores_df['choice'])
    ].groupby('name')['weight'].sum().reset_index()
    highest_scored_points = points_scored_df.weight.max()
    max_potential = potential_points_df.weight.max()
    min_potential = potential_points_df.weight.min()
    highest_scored_names = points_scored_df[points_scored_df.weight == highest_scored_points]['name']
    highest_potential_names = potential_points_df[potential_points_df.weight == max_potential]['name']
    lowest_potential_names = potential_points_df[potential_points_df.weight == min_potential]['name']

    basic_text_msg(
        f"Player(s) with the highest score {highest_scored_points}: {', '.join(highest_scored_names)}!"
    )
    basic_text_msg(
        f"Player(s) with the highest potential at {max_potential}: {', '.join(highest_potential_names)}"
    )
    basic_text_msg(
        f"Player(s) with the lowest potential at {min_potential}: {', '.join(lowest_potential_names)}"
    )
