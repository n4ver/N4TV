from Dependencies.base_functions import valid_log, extract_log_no
from app import data_handler
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
    results = data_handler(real_aliases, bigdict)

    table1, table2 = init_table()

    for i in results[0]:
        table1.add_row(i)
    for i in results[1]:
        table2.add_row(i)

    table1.add_row(["", "Total"] + results[3])
    table2.add_row(results[2] + ["Total", ""])
    print(table1)
    print(table2)

    
if __name__ == "__main__":
    main()
