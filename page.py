import streamlit as st
from pymongo import MongoClient
import pandas as pd
from model import recommend

mongo_path = "mongodb+srv://hwang020612:bC0XJSYYMlIID9Se@cluster-data-engineerin.yo4frmj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-data-engineering" ## copy your path from MongoDB
client = MongoClient(mongo_path)

db=client["movie_db"]
collection=db["library_movie"]

st.title('GIST Movie Recommender')
st.subheader(f'More than {len(list(collection.find({})))} movies are available in GIST! 📹')

st.write("1. Choose your favorite movies up to three")
preference=st.multiselect(
    'select you top three favorite movies', 
    options=["파묘", "범죄도시4", "쿵푸팬더4", "오멘: 저주의 시작", "댓글부대", "남은 인생 10년"], 
    max_selections=3)

st.divider()
st.write("2. We recommend the movies which are available in GIST library based on the movie similarity")
cursor=collection.find({})
df=pd.DataFrame(list(cursor))
df_recommend=recommend(preferences=preference)

cols=st.columns(2)
i=0
for index, row in df_recommend.iterrows():
    with cols[i%2]:
        tile=cols[i%2].container(height=700)
        with tile:
            st.subheader(row["제목"])
            st.image(row["썸네일"], use_column_width=True)
            st.write(f'감독: {row["저자명"]}')
            st.write(f'유형: {row["유형"]}')
            st.write(f'장르: {row["장르"]}')
    i+=1