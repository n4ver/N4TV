from Dependencies.base_functions import valid_log, extract_log_no, special_sort
import prettytable
import requests
import json


def load_json():
    f = open("real_aliases.json",)
    real_aliases = json.load(f)
    f.close()
    return real_aliases


def init_table():
    table1 = prettytable.PrettyTable(header=True, vrules=prettytable.FRAME)
    table2 = prettytable.PrettyTable(header=True, vrules=prettytable.FRAME)
    table1.field_names = ["Class", "Name", "K", "D", "DMG", "HR"]
    table2.field_names = ["K", "D", "DMG", "HR", "Name", "Class"]
    table1.align = "l"
    table2.align = "r"

    return table1, table2


def main():
    real_aliases = load_json()
    
    url = input("Enter URL of log: ")
    # https://logs.tf/2911626#76561198056629020
    while not valid_log(url.strip()):
        print("URL not valid.")
        url = input("Enter URL of log: ")

    log_no = extract_log_no(url)
    api = "https://logs.tf/api/v1/log/" + str(log_no)
    response = requests.get(api)
    print("STATUS: ", response.status_code)


    bigdict = response.json()
    aliases = bigdict["names"]
    data = bigdict["players"]


    table1, table2 = init_table()

    classorder = ['scout','soldier','pyro','demoman','heavyweapons','engineer','medic','sniper','spy']
    order = {key:i for i, key in enumerate(classorder)}
    red_team = []
    blu_team = []
    for i in aliases:
        if i not in real_aliases:
            real_aliases[i] = aliases[i]
        classinfo = data[i]["class_stats"][0]["type"]
        if data[i]["team"] == "Blue":
            blu_team += [[i, order[classinfo]]]
        elif data[i]["team"] == "Red":
            red_team += [[i, order[classinfo]]]
    #print(order)
    #print(red_team)
    red_team = special_sort(red_team, order)
    blu_team = special_sort(blu_team, order)
    total_red = [0, 0, 0, 0]
    total_blu = [0, 0, 0, 0]
    for j in red_team:
        i = j[0]
        lst = [data[i]["class_stats"][0]["type"], real_aliases[i], data[i]["kills"], data[i]["deaths"], data[i]["dmg"], data[i]["hr"]]
        #print(row_format.format(aliases[i], data[i]["kills"], data[i]["deaths"], data[i]["dmg"], data[i]["hr"]))
        table1.add_row(lst)
        for k in range(2, len(lst)):
            total_red[k-2] += lst[k]
    table1.add_row(["", "Total"] + total_red)

    for j in blu_team:
        i = j[0]
        lst = [data[i]["kills"], data[i]["deaths"], data[i]["dmg"], data[i]["hr"], real_aliases[i], data[i]["class_stats"][0]["type"]]
        #print(row_format.format(aliases[i], data[i]["kills"], data[i]["deaths"], data[i]["dmg"], data[i]["hr"]))
        table2.add_row(lst)
        for k in range(len(lst)-2):
            total_blu[k] += lst[k]
    table2.add_row(total_blu + ["Total", ""])
    
    print(table1)
    print(table2)

    
if __name__ == "__main__":
    main()
