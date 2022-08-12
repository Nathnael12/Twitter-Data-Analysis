import streamlit as st
import pandas as pd

add_selectbox = st.sidebar.selectbox(
    "Show data for",
    ("Missing values count", "Most tweeted word", "Most hashtagged words")
)


# df =pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 15, 25, 40]
# }).set_index('first column', inplace=False)
# st.write(df)
# st.line_chart(df)
# st.write("Here's our first attempt at using data to create a table:")
# st.multiselect("my drop",('me','you'))
# st.selectbox("my drop",('me','you'))

import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
if add_selectbox=="Missing values count":
    st.write("Here's Missing columns values table")

    rows = run_query("SELECT * from missing_data;")
    df=pd.DataFrame(rows).iloc[:, 0:2]
    df.rename(columns={0:"missing columns name",1:"count"},inplace=True)
    st.write(df)
elif add_selectbox=="Most hashtagged words":
    st.write("The chart for frequently hashtagged words")

    rows = run_query("SELECT * from freq_hashtags;")
    df=pd.DataFrame(rows).iloc[:, 0:2]
    df.rename(columns={0:"freq_hashtags",1:"count"},inplace=True)

    df =pd.DataFrame({
        'words': list(df["freq_hashtags"]),
        'counts': list(df["count"])
    }).set_index('words', inplace=False)
    st.write(df)
    st.line_chart(df)

else:
    st.write("The chart for frequently tweeted words")

    rows = run_query("SELECT * from freq_words;")
    df=pd.DataFrame(rows).iloc[:, 0:2]
    df.rename(columns={0:"freq_words",1:"count"},inplace=True)

    df =pd.DataFrame({
        'words': list(df["freq_words"]),
        'counts': list(df["count"])
    }).set_index('words', inplace=False)
    st.write(df)
    st.bar_chart(df)
