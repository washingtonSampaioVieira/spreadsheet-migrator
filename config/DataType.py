import re

import pandas


def DATA(value):
    return value.date()


def INT(value):
    try:
        return int(value)
    except ValueError:
        return 0


def STR(value):
    try:
        return str(value)
    except ValueError:
        return ''


def PHONE(value):
    if value is not None and type(value) != float:
        value = re.sub(r'[\(\)\-" "]', '', value)

    return value


def EMAIL(value):
    # Coletando apenas o primeiro email
    if type(value) != float and value is not None:
        return value.split(';')[0]
    else:
        return ''
