from multiprocessing import cpu_count
from os import environ

def get_workers():
    return cpu_count()

bind = '0.0.0.0:' + 