import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Webpage title
TITLE = "WhatsApp Chat Analyzer"
# Initial page config
st.set_page_config(
    page_title=TITLE,
    page_icon="",
    # layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Whatsapp Chat Analyzer")
st.subheader("**♟ General Statistics ♟**")
st.write('''* This app is meant to explore the WhatsApp Chats.
    Try it out by `Uploading WITHOUT MEDIA whatsapp chat export` here.''')
st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.markdown('''This application is compatible with both `iOS` and\
    `Android` device exported chat.''')
st.sidebar.markdown('''
**Application Feature:**
- Individual Statistics
- Group Statistics
- Activity Cluster
- Emoji's Analysis
- WordCloud
- Download Results
'''
)
st.sidebar.markdown("`View Code on Github`")

# for storing graphs
pdfFile = PdfPages("output.pdf")

uploaded_file = st.file_uploader("Choose a txt file only")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.selectbox("Show analysis wrt",user_list)


    if st.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("♟Top Statistics♟")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages 📦 📨")
            st.title(num_messages)
        with col2:
            st.header('Total Words ᅠ📑📝')
            st.title(words)
        with col3:
            st.header("Media Shared 🎞️ 📷")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared 🖇️ 🔗")
            st.title(num_links)

        st.header("Chat Analyzed 💬")
        st.dataframe(df)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        plt.title("Monthly Timeline")
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)
        st.pyplot(fig)



        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        plt.title("Daily Timeline")
        st.pyplot(fig)
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)



        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)


        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        plt.title("Most busy day")
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        plt.title("Most busy month")
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)

        # Weekly Activity Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        plt.title("Weekly Activity Map")
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)


        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color= sns.color_palette('pastel'))
                plt.xticks(rotation='vertical')
                plt.title('Most Busy Users')
                fig.tight_layout(pad=1)
                pdfFile.savefig(fig)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        plt.title("Wordcloud")
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)
        plt.title('Most commmon words')
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f",colors = sns.color_palette('pastel'),startangle=90, pctdistance=0.85,shadow=True)
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            st.pyplot(fig)
        plt.title("Emoji Analysis")
        fig.tight_layout(pad=1)
        pdfFile.savefig(fig)

        pdfFile.close()

        with open("output.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Download Results",
                           data=PDFbyte,
                           file_name="output.pdf",
                           mime='application/octet-stream')








