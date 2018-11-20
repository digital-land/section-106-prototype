import json


def readable_number_filter(number):
    return "{:,}".format(number)


def monetary_filter(number):
    readable_number = readable_number_filter(number)
    return "£{}".format(readable_number)


def pretty_json(value):
    return json.dumps(value, sort_keys=True, indent=4, separators=(',', ': '))