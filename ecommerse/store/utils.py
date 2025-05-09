import random
import string

def generate_discount_code():
    return "DISCOUNT_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

