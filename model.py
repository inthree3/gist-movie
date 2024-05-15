# %%
from pymongo import MongoClient
import requests
from itertools import chain

# %%

mongo_path = "mongodb+srv://hwang020612:bC0XJSYYMlIID9Se@cluster-data-engineerin.yo4frmj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-data-engineering" ## copy your path from MongoDB
client = MongoClient(mongo_path)

db=client["movie_db"]
# %%
collection=db["library_movie"]
# %%
import pprint

for item in collection.find():
    print(item)
# # %%
# url=f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=e4bf7c60c4e3f303ffbe874f8d3acb16&movieNm={title}'
# requests.get(url)

# %%
import pandas as pd
cursor=collection.find({})
df=pd.DataFrame(list(cursor))

# print(df)
# %%
data={'파묘': ['미스터리','공포(호러)'],
'범죄도시4': ['액션','범죄'],
'쿵푸팬더4': ['애니메이션','액션','코미디'],
'오멘: 저주의 시작': ['공포(호러)'],
'댓글부대': ['범죄','드라마'],
'남은 인생 10년': ['멜로/로맨스']}
    
# %%
def recommend(preferences):

    mongo_path = "mongodb+srv://hwang020612:bC0XJSYYMlIID9Se@cluster-data-engineerin.yo4frmj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-data-engineering" ## copy your path from MongoDB
    client = MongoClient(mongo_path)

    db=client["movie_db"]

    collection=db["library_movie"]

    cursor=collection.find({})
    df=pd.DataFrame(list(cursor))
    
    genre_preference=set(chain.from_iterable(
        [data[value] for value in preferences]
    ))

    df["score"]=df["장르"].apply(lambda x: sum([1 for genre in x if genre in genre_preference])/(len(x)+0.5) if x is not None and x!="" else 0)
    df=df.sort_values(by=['score'], ascending=False)

    return df.head()

# %%
