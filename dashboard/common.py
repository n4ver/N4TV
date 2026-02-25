def extract_log_no(url):
    lst = url.split("/")
    number = lst[-1].split("#")[0]
    try: int(number)
    except: return -1
    if int(number) <= 0: return -1
    return int(number)


def special_sort(lst):
    return sorted(lst, key = lambda x: x [1])