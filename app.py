import streamlit as st
import preprocess, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess.preprocess(data)
    st.header("Coverted DataFrame")
    st.dataframe(df)

    userlist = df['user'].unique().tolist()
    userlist.remove('group_notification')
    userlist.sort()
    userlist.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox(
        'Select User in chat Group',
        userlist)

    if st.sidebar.button("Show Analysis"):
        num_messages, total_words, total_media, total_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("Media Shared")
            st.title(total_media)
        with col4:
            st.header("Links Shared")
            st.title(total_links)

        # timeline plots
        st.title("Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['timeline'], timeline['messages'], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #daily timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        col1,col2 = st.columns(2)
        with col1:
            # active days
            st.title("Busiest Days")
            active_days = helper.active_days(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_days['index'], active_days['day_name'], color='orange', width=0.4)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            #acitve months
            st.title("Busiest Months")
            active_month = helper.active_months(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_month['index'], active_month['month'], color='red', width=0.4)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Heat Map")
        heat_df = helper.heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heat_df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0))
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)



        if selected_user == "Overall":
            st.title("Most Busy Users")
            top_busy, busy_df = helper.fetch_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(top_busy.index, top_busy.values, color='maroon', width=0.4)
                plt.xticks(rotation=30)
                plt.xlabel("Top Users")
                plt.ylabel("No. of messages")
                st.pyplot(fig)
            with col2:
                st.dataframe(busy_df)

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Used Words")
        df_most = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        col1, col2 = st.columns(2)
        with col1:
            ax.barh(df_most['Words'].tolist()[0:10], df_most['Frequency'].tolist()[0:10], color='green')
            plt.xticks(rotation='vertical')
            plt.xlabel("Top Words")
            plt.ylabel("Frequency")
            st.pyplot(fig)
        with col2:
            # pass
            st.dataframe(df_most)

        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        emoji_df = helper.most_common_emojis(selected_user, df)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.pie(emoji_df[1][0:8], labels=emoji_df[0][0:8], autopct='%1.1f%%', shadow=False)
            st.pyplot(fig)
