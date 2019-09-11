def DATA(value):
    return value


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
    value = value.replace('(', '')
    value = value.replace(')', '')
    value = value.replace('-', '')

    return value


def EMAIL(value):
    if len(value.split(';')) == 1:
        value += ';'

    return value
