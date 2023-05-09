import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)


# fetch unique user

user_list = df['user'].unique().tolist()
user_list.remove('group notification')
user_list.sort()
user_list.insert(0, "overall")

selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)


if st.sidebar.button("Show Analysis"):
    num_message, words, media_msg, num_links = helper.fetch_stats(selected_user, df)
    st.title("Top Analysis")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("Total message")
        st.title(num_message)

    with col2:
        st.header("Total Words")
        st.title(words)

    with col3:
        st.header("Media Shared")
        st.title(media_msg)

    with col4:
        st.header("Links Shared")
        st.title(num_links)

    # Monthly timeline
    st.title('Monthly Timeline')
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Daily_timeline
    st.title('Daily Timeline')
    timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['only_date'], timeline['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Activity map
    st.title('Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        st.header('Busy day')
        busy_day = helper.weekly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(busy_day.index, busy_day.values)
        st.pyplot(fig)

    with col2:
        st.header('Busy Month')
        busy_month = helper.monthly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(busy_month.index, busy_month.values, color='orange')
        st.pyplot(fig)

    # activity heatmap
    st.title('Weekly Activity Map')
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    # finding busiest user

    if selected_user == 'overall':
        st.title('Most Busy User')
        x, new_df = helper.most_busy_user(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

    # Wordcloud
    st.title('WordCloud')
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # Most common words

    most_common_df = helper.most_common_word(selected_user, df)
    fix, ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title('Most Common Words')
    st.pyplot(fix)
    # st.dataframe(most_common_df)

    # emoji analysis

    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)


