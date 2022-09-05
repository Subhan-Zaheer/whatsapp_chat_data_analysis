import os
import re

import numpy as np
import pandas as pd
import datetime
import time
import matplotlib as mlt
from matplotlib import pyplot as plt
import seaborn as sns


def converting_time_in_12hr_format():
    return '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s'


def converting_time_in_24hr_format():
    return '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'


def date_time_12hr_format():
    return '%d/%m/%Y, %I:%M %p - '


def date_time_24hr_format():
    return '%d/%m/%Y, %H:%M - '


def splitting_user_and_message(chats_dataFrame):
    user_name = []
    message = []

    for i in chats_dataFrame['user_messages']:

        a = re.split('([\w\W]+?):\s', i)
        if (a[1:]):
            # creating two different lists of usernames and messages from user_message column
            # if a row is a valid message than it will store message in message list and
            # user_name in user_name list
            user_name.append(a[1])
            message.append(a[2])
        else:
            # if it is not a valid message than it would be a group notification
            # we will also store it in list accordingly.
            user_name.append("Group Notification")
            message.append(a[0])

    chats_dataFrame['User_Name'] = user_name
    chats_dataFrame['Message'] = message
    chats_dataFrame.drop('user_messages', inplace=True, axis=1)
    return chats_dataFrame


def re_for_date_and_time():
    return '\d{2,4}\-\d{2}\-\d{2}'


def splitting_date_and_time(chats_dataFrame):

    chats_dataFrame['Date'] = pd.to_datetime(chats_dataFrame['date_time']).dt.date
    chats_dataFrame['Time'] = pd.to_datetime(chats_dataFrame['date_time']).dt.time

    # chats_dataFrame.drop(chats_dataFrame['date_time'], inplace=True)
    print(chats_dataFrame)
    print(chats_dataFrame.columns)
    print(type(chats_dataFrame['Time'][0]))

    pass


def adding_helper_columns(chats_dataFrame):
    chats_dataFrame['Day'] = pd.to_datetime(chats_dataFrame['date_time']).dt.strftime('%a')
    chats_dataFrame['Year'] = pd.to_datetime(chats_dataFrame['date_time']).apply(lambda x: x.year)
    chats_dataFrame['Month'] = pd.to_datetime(chats_dataFrame['date_time']).apply(lambda x: x.strftime('%b'))
    return chats_dataFrame
    pass


def most_active_users(chats_dataFrame):
    temp_chats_dataFrame = chats_dataFrame.copy()
    temp_chats_dataFrame['Message_Count'] = [1] * chats_dataFrame.shape[0]
    temp_chats_dataFrame.drop(columns='Year', inplace=True)
    temp_chats_dataFrame = temp_chats_dataFrame.groupby('User_Name').sum().reset_index()
    print(temp_chats_dataFrame.sort_values(by='Message_Count', ascending=False).head(50))
    print(temp_chats_dataFrame.describe())
    return chats_dataFrame


def last_30_days_chat(chats_dataFrame):
    date = chats_dataFrame.iloc[-1]['Date']
    time.ctime()
    pass


def creating_dataFrame(file_name):

    """ Converting raw data into presentable data frame"""

    split_formats = {
        '12hr': converting_time_in_12hr_format() ,
        '24hr': converting_time_in_24hr_format(),
        'custom': ''
    }
    datetime_formats = {
        '12hr': date_time_12hr_format(),
        '24hr': date_time_24hr_format(),
        'custom': ''
    }

    file = open(r"bds_chat_data.txt", 'r', encoding='utf-8')

    raw_string = " ".join(file.read().split('\n'))   # splitting our text by \n.

    # extracting the user messages from given raw string.
    user_messages = re.split(split_formats['12hr'], raw_string)[1:]

    # extracting out the date and time from given raw string.
    date_and_time = re.findall(split_formats['12hr'], raw_string)
    # print(date_and_time)
    chats_dataFrame = pd.DataFrame({'date_time':date_and_time, 'user_messages':user_messages })
    # print(chats_dataFrame)

    # Converting date_time to pandas date_time object.
    chats_dataFrame['date_time'] = pd.to_datetime(chats_dataFrame['date_time'], format=datetime_formats['12hr'])

    # print(chats_dataFrame)

    chats_dataFrame = splitting_user_and_message(chats_dataFrame)
    # print(chats_dataFrame)
    splitting_date_and_time(chats_dataFrame)
    return adding_helper_columns(chats_dataFrame)


if __name__ == '__main__':
    file_name = input("Enter file name with extension : ")
    chats_dataFrame = creating_dataFrame(file_name)
    chats_dataFrame = most_active_users(chats_dataFrame)
    # print(chats_dataFrame)


    pass
