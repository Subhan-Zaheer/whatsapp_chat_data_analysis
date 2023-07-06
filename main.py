import os
import re
import emoji
import numpy as np
import pandas as pd
import datetime
import time
import matplotlib as mlt
from matplotlib import pyplot as plt
import seaborn as sns
import sys


def converting_time_in_12hr_format():
    return '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s'


def converting_time_in_12hr_format_for_iphone():
    return '\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[APap][mM]\]'


def converting_time_in_24hr_format_for_iphone():
    return '[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s]'


def date_time_12hr_format_iphone():
    return '%d/%m/%Y, %I:%M:%S %p'


def date_time_24hr_format_iphone():
    return '%d/%m/%Y, %H:%M - '


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
    temp_chats_dataFrame = temp_chats_dataFrame.groupby('User_Name').sum(numeric_only=True).reset_index()
    print(temp_chats_dataFrame.sort_values(by='Message_Count', ascending=False).head(50))
    print(temp_chats_dataFrame.describe())
    return chats_dataFrame


def last_30_days_chat(chats_dataFrame):

    temp_df = chats_dataFrame.copy() # Creating a copy of actual dataset.
    last_index_date = pd.to_datetime(temp_df.iloc[-1]['Date']) # getting date of last index in dataset.
    date_1970 = pd.to_datetime(time.ctime(time.time()-time.time())) # date 1970-01-01
    seconds_of_last_index_date = (last_index_date - date_1970).total_seconds() # Generating seconds of date on last index
    seconds_of_date_of_month_back = time.ctime(seconds_of_last_index_date-2592000) # Generating seconds for month back date.
    date_of_month_back = pd.to_datetime(seconds_of_date_of_month_back).date() # Creating date for above computed seconds.
    # print(f"Date of month back is : {date_of_month_back}")
    # print(f"Today date is : {last_index_date}")
    today_index = temp_df.index[-1]
    # print(f"Index in today_index is : {today_index}")
    # print(f"Date of month back is {date_of_month_back}")
    date_of_month_back_index = temp_df[temp_df['Date']==date_of_month_back].index
    date_of_month_back_index = date_of_month_back_index[len(date_of_month_back_index)-1]
    # print(f"Index in date_of_month_back_index is : {date_of_month_back_index}")
    prev_30_days_chat = temp_df.iloc[date_of_month_back_index:today_index]
    most_active_users(prev_30_days_chat)
    pass


def total_messagelength_of_every_user(chats_dataFrame):
    another_df = chats_dataFrame.copy()
    another_df['Message_Length'] = another_df['Message'].apply(lambda x: len(x))
    print(another_df.groupby('User_Name').sum(numeric_only=True).reset_index().drop(columns='Year').sort_values(by='Message_Length').head(50))
    return another_df
    pass


def message_Count_by_month(chat_dataFrame):
    temp_df = chats_dataFrame.copy()
    temp_df['Message_Count'] = [1] * temp_df.shape[0]
    temp_df = temp_df.groupby('Month').sum(numeric_only=True).reset_index()
    temp_df.drop(columns='Year', inplace=True)
    print(temp_df)


def message_Count_by_days(chats_dataFrame):
    temp_df = chats_dataFrame.copy()
    temp_df['Message_Count'] = [1] * chats_dataFrame.shape[0]
    temp_df = temp_df.groupby('Day').sum(numeric_only=True).reset_index()
    temp_df.drop(columns='Year', inplace=True)
    print("Message count after grouping by days")
    print(temp_df)


def top10_emojis(chats_dataFrame):
   pass



def creating_dateFrame_for_Iphone_chat(file_name):
    """ Converting raw data into presentable data frame"""

    split_formats = {
        '12hr': converting_time_in_12hr_format_for_iphone(),
        '24hr': converting_time_in_24hr_format_for_iphone(),
        'custom': ''
    }
    datetime_formats = {
        '12hr': date_time_12hr_format_iphone(),
        '24hr': date_time_24hr_format_iphone(),
        'custom': ''
    }

    file = open(r"bds_chat_data.txt",
                'r',
                encoding='utf-8')

    raw_string = " ".join(file.read().split('\n'))  # splitting our text by \n.

    # extracting the user messages from given raw string.
    user_messages = re.split(split_formats['12hr'], raw_string)[1:]

    # extracting out the date and time from given raw string.
    date_and_time = re.findall(split_formats['12hr'], raw_string)

    chats_dataFrame = pd.DataFrame({'date_time': date_and_time, 'user_messages': user_messages})

    # Converting date_time to pandas date_time object.

    ls = []
    for i in chats_dataFrame['date_time']:
        ls.append(i[1:-1])
    sr = pd.Series(ls)
    chats_dataFrame['date_time'] = sr
    chats_dataFrame['date_time'] = pd.to_datetime(chats_dataFrame['date_time'], format=datetime_formats['12hr'])

    chats_dataFrame = splitting_user_and_message(chats_dataFrame)

    splitting_date_and_time(chats_dataFrame)
    return adding_helper_columns(chats_dataFrame)


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

    chats_dataFrame = pd.DataFrame({'date_time':date_and_time, 'user_messages':user_messages })


    # Converting date_time to pandas date_time object.
    chats_dataFrame['date_time'] = pd.to_datetime(chats_dataFrame['date_time'], format=datetime_formats['12hr'])


    chats_dataFrame = splitting_user_and_message(chats_dataFrame)

    splitting_date_and_time(chats_dataFrame)
    return adding_helper_columns(chats_dataFrame)


if __name__ == '__main__':
    

    sys.stdout.reconfigure(encoding='utf-8')
    # chat_format = int(input("Enter 1 if whatsapp chat text is from android and 0 if it is from Iphone : "))
    # file_name = input("Enter file name with extension : ")
    # if chat_format == 1:
    #     chats_dataFrame = creating_dataFrame('bds_chat_data.txt')
    # else:
    #     chats_dataFrame = creating_dateFrame_for_Iphone_chat("bds_chat_data.txt")
    chats_dataFrame = creating_dataFrame("bds_chat_data.txt")
    chats_dataFrame = most_active_users(chats_dataFrame)
    last_30_days_chat(chats_dataFrame)
    message_Count_by_days(chats_dataFrame)
    message_Count_by_month(chats_dataFrame)


    pass
