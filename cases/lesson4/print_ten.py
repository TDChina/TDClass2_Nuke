import time

test_list = [i for i in range(20)]


def print_list():
    for i in test_list:
        print i
        time.sleep(1)


print_list()
