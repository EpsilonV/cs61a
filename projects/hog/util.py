__author__ = 'john'

from math import sqrt

def is_prime(num):
    """
    :param num: the test num
    :return: True if num is a prime number or False
    """
    if num <= 1:
        return False
    for i in range(2,int(sqrt(num))+1):
        if num % i == 0:
            return  False

    return True

def next_prime(num):
    while True:
        num += 1
        if is_prime(num):
            return num