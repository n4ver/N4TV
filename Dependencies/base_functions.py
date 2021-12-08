def valid_url(url):
    if url.startswith("https://logs.tf/"):
        return True
    else:
        return False


def extract_log_no(url):
    lst = url.split("/")
    number = lst[-1].split("#")[0]
    try: int(number)
    except:
        return -1
    if int(number) <= 0:
        return -1
    return int(number)


def valid_log(url):
    return (valid_url(url) and extract_log_no(url) != -1)


def special_sort(lst):
    return sorted(lst, key = lambda x: x [1])