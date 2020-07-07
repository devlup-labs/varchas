import random
import string

def random_string_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_referral_code():
    return "RG{rand_letters}{rand_digits}".format(rand_letters=random_string_generator(3, string.ascii_uppercase),
                                                  rand_digits=random.randint(10, 99))
