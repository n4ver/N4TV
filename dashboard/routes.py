from flask import render_template, request, redirect, url_for
from flask import current_app as app

from .common import extract_log_no, special_sort

import requests
import json
import time

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        log_url = request.form['logsurl']
        log_no = extract_log_no(log_url)
        
        api = "https://logs.tf/api/v1/log/" + str(log_no)
        response = requests.get(api)

        real_aliases = load_json()
        
        bigdict = response.json()
        data, map_played, score = data_handler(real_aliases, bigdict)
        
    elif request.method == "GET":
        log_url = request.args.get('l', None)
        log_no = extract_log_no(log_url)

        api = "https://logs.tf/api/v1/log/" + str(log_no)
        response = requests.get(api)
        while response.status_code == 429:
            time.sleep(10) # Wait before next call
            print("429 | Sent too many requests, waiting 10 seconds...")
            response = requests.get(api)

        real_aliases = load_json()

        bigdict = response.json()
        data, map_played, score = data_handler(real_aliases, bigdict)

    sharelink = f"{request.base_url}?l={log_url}"
    return render_template('handle_logs.html', data=data, sharelink=sharelink, map_played=map_played, score=score)


def data_handler(real_aliases, resp):
    aliases = resp["names"]
    data1 = resp["players"]

    classorder = ['scout','soldier','pyro','demoman','heavyweapons','engineer','medic','sniper','spy']
    order = {key:i for i, key in enumerate(classorder)}

    red_team = []
    blu_team = []
    for i in aliases:
        if i not in real_aliases:
            real_aliases[i] = aliases[i]
        classinfo = data1[i]["class_stats"][0]["type"]
        if data1[i]["team"] == "Blue":
            blu_team += [[i, order[classinfo]]]
        elif data1[i]["team"] == "Red":
            red_team += [[i, order[classinfo]]]

    red_team = special_sort(red_team)
    blu_team = special_sort(blu_team)
    total_red = [0, 0, 0, 0]
    total_blu = [0, 0, 0, 0]
    #row_format = " {:^6} {:^6} {:^6} {:^6} {:^6} {:^6} "
    data = [[],[],[],[]]
    map_played = resp["info"]["map"]
    score = [resp["teams"]["Blue"]["score"], resp["teams"]["Red"]["score"]]
    
    for j in red_team:
        i = j[0]
        lst = [data1[i]["kills"], data1[i]["deaths"], data1[i]["dapm"], data1[i]["hr"], real_aliases[i], data1[i]["class_stats"][0]["type"]]
        #print(row_format.format(*lst))
        data[1] += [lst]
        for k in range(len(lst)-2):
            if k != 2:
                total_blu[k] += lst[k]
            else:
                total_blu[k] += data1[i]['dmg']
    
    for j in blu_team:
        i = j[0]
        lst = [data1[i]["class_stats"][0]["type"], real_aliases[i], data1[i]["kills"], data1[i]["deaths"], data1[i]["dapm"], data1[i]["hr"]]
        #print(row_format.format(*lst))
        data[0] += [lst]
        for k in range(2, len(lst)):
            if k != 4:
                total_red[k-2] += lst[k]
            else:
                total_red[k-2] += data1[i]['dmg']

    data[2] = total_blu
    data[3] = total_red
    
    return data, map_played, score


def load_json():
    try:
        f = open('real_aliases.json')
        data = json.load(f)
        return data
    except FileNotFoundError:
        return {}