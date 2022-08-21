import re
import regex
import pandas as pd
from datetime import datetime
from pandas.errors import EmptyDataError

def preprocessor(data):

    pattern = '\d+/\d+/\d+, \d+:\d+\d+ [aA-zZ]* - '

    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_message': messages,'message_date': dates})

    # SAMSUNG Export time format

    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format="%Y/%m/%d, %I:%M %p - ")
    except Exception as diag:
        print(diag)

    # IOS Export time format

        try:
            # Drop date enclosures from date column
            df['message_date'] = df['message_date'].map(lambda x: x.lstrip('[').rstrip(']'))
            df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M:%S %p - ")
        except Exception as diag:
            print(diag)

        # OppO Export time format
            try:
                df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M %p - ")
            except Exception as diag:
                print(diag)

            # Android Export time format
                try:
                    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %I:%M %p - ")
                except Exception as diag:
                    print(diag)

                    try:
                        df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p - ")
                    except EmptyDataError as diag:
                        raise diag



    df['message_date'] = pd.to_datetime(df['message_date'])

    # convert message_date type

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # seperate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []

    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df