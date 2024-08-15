import pandas as pd
import folium
import webbrowser

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

from sklearn.linear_model import LinearRegression

# 데이터 파일 불러오기
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df.columns
df['Neighborhood'].value_counts()

ex= df.groupby('Exterior_1st',as_index=False).agg(n=('Exterior_1st','count')).sort_values('n', ascending=False)
df.groupby(['Exterior_1st', 'Year_Built'],as_index=False).agg(n=('Exterior_1st','count')).sort_values('n', ascending=False)
ex
["VinylSd","MetalSd","HdBoard","Wd Sdng","Plywood","CemntBd","BrkFace"]




[i for i in ex['Exterior_1st']]
rank = {
    "Excellent" : 5,
    "Good":4,
    "Typical":3,
    "Fair":2,
    "Poor":1
}
df['rank_Exter_Cond'] = [rank[key] for key in df['Exter_Cond']]
df['Exterior_1st'].value_counts().sort_values(ascending=False)
ex = df.groupby(['Exterior_1st','Neighborhood'],as_index=False).agg(n=('Neighborhood','count'))
df['Exterior_1st'].unique(|)
ex['VinylSd']
ex.value_counts()
fig = px.scatter(
    df,
    x="Mas_Vnr_Area",
    y="Sale_Price",
    color="Exterior_1st",
).show()

fig = px.scatter(
    df,
    x="Gr_Liv_Area",
    y="Sale_Price",
    color="Exterior_1st",
).show()


fig = px.bar(
    df,
    x="Sale_Price",
    y="Neighborhood",
    color="Exterior_1st",
    orientation='h'
).show()



df.columns




#fig.update_yaxes(range=[0, 700000])
fig.show()
df.columns
df.groupby('Neighborhood').agg(n=('Mas_Vnr_Area','count')).sort_values('n', ascending=False)


df.shape
df.columns
fig = px.histogram(df, x="Exterior_1st")
fig.show()
map_house = folium.Map(location=[42.034482,-93.642897 ],
                       zoom_start=13,
                       tiles='cartodbpositron')
N_array = df['Exterior_1st'].unique()
palette = sns.color_palette("viridis", len(N_array)).as_hex()
N_dict = { N:color for N,color in zip(N_array, palette)}


for i in range(len(df['Longitude'])):
    folium.CircleMarker([df['Latitude'][i], df['Longitude'][i]],
                        popup=f"위도: {df['Latitude'][i]}, 경도: {df['Longitude'][i]}, Price: ${df['Sale_Price'][i]}",
                        radius=df['Sale_Price'][i]/100000,
                        color=N_dict.get(df['Exterior_1st'][i]),
                        fill = True,
                        fill_color= N_dict.get(df['Exterior_1st'][i]),
                        fill_opacity=0.7
                        ).add_to(map_house)
import branca.colormap as cm
colormap = cm.LinearColormap(palette , vmin=0, vmax=len(N_array)-1, caption="Color Legend")
colormap.add_to(map_house)


map_house.save('map_house.html')
webbrowser.open_new('map_house.html')

# 데이터 나누기(랜덤으로 train 80%, test20%)
# np.random.seed(20240805) # 팀 결성일
# index_train = sorted(np.random.choice(df.shape[0], int(df.shape[0]*0.8), replace=False))
# train = df.iloc[index_train,:]
# test = df.drop(index_train, axis=0)
# 검산 my_list = sorted(list(test.index) + list(train.index))
# 검산 my_list == list(df.index)

## <데이터 살펴보기>
# train.shape
# train.info()
df.columns

fig = go.Figure()
fig.add_trace(go.Histogram(x=df["Year_Built"]))
fig.add_trace(go.Histogram(x=df["Year_Remod_Add"]))
fig.update_layout(
    title = dict({
        "text" : "연도별 건축수",
        "font_size": 15,
    })
)

df["Year_Built"].value_counts(ascending=False).tail(10)
df["Year_Remod_Add"].value_counts(ascending=False).tail(10)
df["Year_Built"].describe()
df["Year_Remod_Add"].describe()
df['Year_Sold'].describe()
df['Sale_Type'].value_counts()
df['Sale_Type']

import pandas as pd
import folium
import webbrowser
import branca.colormap as cm
import json

# 데이터 파일 불러오기
df = pd.read_csv('data/houseprice-with-lonlat.csv')

# 외장재 별로 색상을 지정합니다
color_mapping = {
    "VinylSd": "skyblue",  # 하늘색
    "HdBoard": "green",    # 초록색
    "Plywood": "purple",   # 보라색
    "MetalSd": "orange",   # 주황색
    "BrkFace": "red"       # 빨간색
}

# 나머지 색상을 회색으로 설정
df['color'] = df['Exterior_1st'].apply(lambda x: color_mapping.get(x, "gray"))

# 지도 생성
map_house = folium.Map(location=[42.034482,-93.642897],
                       zoom_start=13,
                       tiles='cartodbpositron')

# 마커 추가
for i in range(len(df['Longitude'])):
    folium.CircleMarker(
        [df['Latitude'][i], df['Longitude'][i]],
        popup=f"위도: {df['Latitude'][i]}, 경도: {df['Longitude'][i]}, Price: ${df['Sale_Price'][i]}",
        radius=df['Sale_Price'][i]/100000,
        color=df['color'][i],
        fill=True,
        fill_color=df['color'][i],
        fill_opacity=0.7
    ).add_to(map_house)

# 고지대/저지대 GeoJSON 파일 불러오기
with open('ames_elevation.geojson') as f:
    geojson_data = json.load(f)

# GeoJSON 데이터를 지도에 추가
folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        'fillColor': 'blue' if feature['properties']['name'] == 'High Elevation Area' else 'yellow',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.3,
    }
).add_to(map_house)

# 범례 추가
colormap = cm.StepColormap(
    colors=list(color_mapping.values()) + ["gray"],
    index=[0, 1, 2, 3, 4, 5],
    vmin=0,
    vmax=5,
    caption="Color Legend"
)
colormap.add_to(map_house)

# 지도 저장 및 열기
map_house.save('map_house.html')
webbrowser.open_new('map_house.html')


#########################
import pandas as pd

ames = pd.read_csv('Ames_HousePrice_nbhd.csv')
ames

import folium
import webbrowser

nbhd = folium.Map(location=[42.034482,-93.642897 ],
                       zoom_start=13,
                       tiles='cartodbpositron')

for i in range(len(ames['Longitude'])):
    folium.CircleMarker([ames['Latitude'][i], ames['Longitude'][i]],
                        popup=f"위도: {ames['Latitude'][i]}, 경도: {ames['Longitude'][i]}, 동네: ${ames['Neighborhood'][i]}",
                        radius=ames['Radius'][i]
                        ).add_to(nbhd)
                        

nbhd.save('nbhd.html')
webbrowser.open_new('nbhd.html')


###

import json

geo = json.load(open("data/city.geojson", encoding="UTF-8"))
geo
# 데이터 탐색
type(geo_seoul)
len(geo_seoul)
geo_seoul.keys()
geo_seoul["features"][0]
len(geo_seoul["features"])
len(geo_seoul["features"][0])
geo_seoul["features"][0].keys()