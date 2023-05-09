import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extract = URLExtract()
def fetch_stats(selected_user, df):

    if selected_user != "overall":
        df = df[df['user'] == selected_user]
    # Number of message
    num_message = df.shape[0]
    # Number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Number of shared media
    media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Number of shared links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_message, len(words), media_msg, len(links)


def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(
     columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_word(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_word)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_word(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))

    return return_df

def emoji_helper(selected_user, df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return timeline

def weekly_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    return df['days_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='days_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap



