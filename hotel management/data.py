admin_data = {"user": "sravani", "pwd": "sravani1510"}


all_rooms = {
"single": [101,102,103,104,105],
"double": [201,202,203,204,205],
"suite": [301,302,303,304,305]
}

prices = {
    "single": 800,
    "double": 1200,
    "suite": 2000
}

# just marking busy rooms
busy_list = set()


def busy(num): # mark busy
    busy_list.add(num)


def free(num, ok=False): # check or free
    if ok:
        busy_list.discard(num)
        return
    return num not in busy_list


# storing guest info
# {name, phone, room, type, in, out, status}
guests = []