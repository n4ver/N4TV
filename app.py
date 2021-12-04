from flask import Flask, render_template, request
from Dependencies.base_functions import extract_log_no, special_sort
import requests
import json
import time
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)


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
        data = data_handler(real_aliases, bigdict)
        
        return render_template('handle_logs.html', data=data)
    elif request.method == "GET":
        log_url = request.args.get('log', None)
        log_no = extract_log_no(log_url)

        api = "https://logs.tf/api/v1/log/" + str(log_no)
        response = requests.get(api)
        while response.status_code == 429:
            time.sleep(10) # Wait before next call
            print("STATUS: 429, Sent too many requests")
            response = requests.get(api)

        real_aliases = load_json()

        bigdict = response.json()
        data = data_handler(real_aliases, bigdict)

        #return render_template('index.html')
        return render_template('handle_logs.html', data=data)


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

    red_team = special_sort(red_team, order)
    blu_team = special_sort(blu_team, order)
    total_red = [0, 0, 0, 0]
    total_blu = [0, 0, 0, 0]
    #row_format = " {:^6} {:^6} {:^6} {:^6} {:^6} {:^6} "
    data = [[],[],[],[]]
    
    for j in red_team:
        i = j[0]
        lst = [data1[i]["kills"], data1[i]["deaths"], data1[i]["dmg"], data1[i]["hr"], real_aliases[i], data1[i]["class_stats"][0]["type"]]
        #print(row_format.format(*lst))
        data[1] += [lst]
        for k in range(len(lst)-2):
            total_blu[k] += lst[k]
    
    for j in blu_team:
        i = j[0]
        lst = [data1[i]["class_stats"][0]["type"], real_aliases[i], data1[i]["kills"], data1[i]["deaths"], data1[i]["dmg"], data1[i]["hr"]]
        #print(row_format.format(*lst))
        data[0] += [lst]
        for k in range(2, len(lst)):
            total_red[k-2] += lst[k]

    data[2] = total_blu
    data[3] = total_red
    
    return data


def load_json():
    f = open('real_aliases.json')
    data = json.load(f)
    return data


if __name__ == "__main__":
    app.run(debug=True, port=5000)
