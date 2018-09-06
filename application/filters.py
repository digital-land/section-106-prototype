
def readable_number_filter(number):
    return "{:,}".format(number)

def monetary_filter(number):
    readable_number = readable_number_filter(number)
    return "£{}".format(readable_number)