# %%
import streamlit as st
import requests
from pymongo import MongoClient
import json
# %%
mongo_path = "mongodb+srv://hwang020612:bC0XJSYYMlIID9Se@cluster-data-engineerin.yo4frmj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-data-engineering" ## copy your path from MongoDB
client = MongoClient(mongo_path)

db=client["movie_db"]
collection=db["library_movie"]
# %%
# collection.update_many({}, {"$unset": {"번호": ""}})

# %%
import os
from dotenv import load_dotenv
load_dotenv(override=True)

SEARCH_API_KEY=os.getenv("SEARCH_API_KEY")
SEARCH_ENGINE_ID=os.getenv("SEARCH_ENGINE_ID")
# %%
for item in collection.find():
    if "썸네일" not in item or item["썸네일"]=="https://adventure.co.kr/wp-content/uploads/2020/09/no-image.jpg":
        print(item)
# %%
import requests
for item in collection.find():
    if "썸네일" not in item or item["썸네일"]=="https://adventure.co.kr/wp-content/uploads/2020/09/no-image.jpg":
        movie_title=item["제목"].split("=")[0].split("[")[0].rstrip()
        movie_thumbnail=requests.get(f"https://www.googleapis.com/customsearch/v1?key={SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&num=1&q=영화 {movie_title} 예스24")
        try:
            # img_link=json.loads(movie_thumbnail.content.decode())["items"][0]["pagemap"]["metatags"][0]["og:image"]
            img_link=json.loads(movie_thumbnail.content.decode())["items"][0]["pagemap"]["cse_image"][0]["src"]
        except:
            img_link="https://adventure.co.kr/wp-content/uploads/2020/09/no-image.jpg"
            print("missing image")
            print(movie_thumbnail.content.decode())
            

        query={"제목": item["제목"]}
        new_value={"$set": {"썸네일": img_link}}
        collection.update_one(query, new_value)
        print(item["제목"])

# %%
print(json.loads(movie_thumbnail.content.decode())["items"][0]["pagemap"]["cse_image"][0]["src"])
# %%
import json
movie_thumbnail=requests.get(f"https://www.googleapis.com/customsearch/v1?key={SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&num=1&q=케이블 가이 poster 예스24")
json.loads(movie_thumbnail.content.decode())
# %%
import pprint
import json

for item in collection.find():
    if "장르" not in item.keys():
        title_origin=item["제목"]
        title=title_origin.split('=')[0].split('[')[0]

        url=f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=e4bf7c60c4e3f303ffbe874f8d3acb16&movieNm={title}'
        response=requests.get(url)
        response_json=json.loads(response.content.decode())
        if response_json["movieListResult"]["totCnt"]>0:
            type=response_json["movieListResult"]["movieList"][0]["typeNm"]
            genre=response_json["movieListResult"]["movieList"][0]["genreAlt"].split(',')

            query={"제목": title_origin}
            new_values={"$set": {"유형": type, "장르": genre}}
            
        else:
            print(f"{title}에 대한 api 검색 결과가 없습니다.")
            query={"제목": title_origin}
            new_values={"$set": {"유형": None, "장르": None}}
        
        collection.update_one(query, new_values)

# %%
for item in collection.find():
    title_origin=item["제목"]
    query={"제목": title_origin}

    if item["장르"]=='' or item["장르"]==[]:
        new_values={"$set": {"장르": [""]}}
        collection.update_one(query, new_values)

# %%
#type, genre
print(response_json["movieListResult"]["movieList"][0]["typeNm"])
print(response_json["movieListResult"]["movieList"][0]["genreAlt"])

# %%
selections=["파묘", "범죄도시4", "쿵푸팬더4", "오멘: 저주의 시작", "댓글부대", "남은 인생 10년"]
for selection in selections:
    url=f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=e4bf7c60c4e3f303ffbe874f8d3acb16&movieNm={selection}'
    response=requests.get(url)
    response_json=json.loads(response.content.decode())
    print(f'{{{selection}: [{response_json["movieListResult"]["movieList"][0]["genreAlt"]}]}}')
# %%

