import asyncio
import os
import numpy as np
import pandas as pd
import matplotlib as mlt
from matplotlib import pyplot as plt


def read_data(file_name):
    # print(os.getcwd())
    # os.chdir(r"C:\Users\Khan Mob s  Comp\Desktop")
    # print(os.getcwd())
    file = open(r"bds_chat_data.txt", 'r', encoding='utf-8')
    # print(file)
    raw_string = "\n".join(file.read().split('\n'))
    print(raw_string)
    # line = file.readlines()
    # print(line.__sizeof__())
    # splitting = line[0].split(',')
    # print(line)
    # print(splitting)
    # while True:
    #     (yield)

    # specific_line = np.array(line[8:12])
    # print(specific_line)

    pass


if __name__ == '__main__':
    file_name = input("Enter file name with extension : ")
    read_data(file_name)
    print("\n-------------*********************------------------\n")
    read_data(file_name)
    pass
