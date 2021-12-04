from Dependencies.base_functions import extract_log_no, valid_log
import requests
import json

def main():
    url = input("Enter URL of log: ")
    # https://logs.tf/2911626#76561198056629020
    while not valid_log(url.strip()):
        print("URL not valid.")
        url = input("Enter URL of log: ")

    log_no = extract_log_no(url)
    api = "https://logs.tf/api/v1/log/" + str(log_no)
    response = requests.get(api)
    print("STATUS: ", response.status_code)
    with open(f'/../logs/{str(log_no)}.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
    
