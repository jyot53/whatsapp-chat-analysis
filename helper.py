from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import matplotlib.pyplot as plt


def fetch_stats(user, df):
    # dfcontact = pd.DataFrame({'users': df['user'].value_counts().index.tolist(),
    #                           'message_count': df['user'].value_counts().tolist()})
    extractor = URLExtract()

    if (user == "Overall"):
        num_messages = df.shape[0]
        total_media = df[df['messages'].str.contains("<Media omitted>")].shape[0]
        total_words = df['messages'].str.split().str.len().sum()
        links = []
        for message in df['messages']:
            links.extend(extractor.find_urls(message))
        total_links = len(links)
        return num_messages, total_words, total_media, total_links
    else:
        total_media = df[(df['messages'].str.contains("<Media omitted>")) & (df['user'] == user)].shape[0]
        num_messages = df[df['user'] == user].shape[0]
        total_words = df[df['user'] == user]['messages'].str.split().str.len().sum()
        links = []
        for message in df[df['user'] == user]['messages']:
            links.extend(extractor.find_urls(message))
        total_links = len(links)
        return num_messages, total_words, total_media, total_links


def fetch_busy_users(df):
    busy = df[df['user'] != 'group_notification']['user'].value_counts().head()
    busy_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return busy, busy_df


def create_wordcloud(selected_user, df):
    df = df[df['user'] != 'group_notification']
    df = df[df['messages'] != '<Media omitted>\n']
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=400, height=200, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    if selected_user != 'Overall':
        temp = temp[temp['user'] == selected_user]

    words = []
    for message in temp['messages']:
        words.extend(message.split())

    common_words = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0: 'Words', 1: 'Frequency'})
    return common_words


def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['timeline'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline


def active_days(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['day_name'] = df['date'].dt.day_name()
    active_day = df['day_name'].value_counts().reset_index()
    return active_day


def active_months(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    active_month = df['month'].value_counts().reset_index()
    return active_month


def heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
