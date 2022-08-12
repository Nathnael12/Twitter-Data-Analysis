import streamlit as st
import pandas as pd

st.write("Here's Missing columns values table")
# df =pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 15, 25, 40]
# }).set_index('first column', inplace=False)
# st.write(df)
# st.line_chart(df)
# st.write("Here's our first attempt at using data to create a table:")
# st.multiselect("my drop",('me','you'))
# st.selectbox("my drop",('me','you'))

import streamlit as st
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

rows = run_query("SELECT * from missing_data;")
df=pd.DataFrame(rows).iloc[:, 0:2]
df.rename(columns={0:"missing columns name",1:"count"},inplace=True)
st.write(df)

# Print results.
# for row in rows:
    # st.write(f"{row[0]} has a :{row[1]}:")