
import pandas as pd
import plotly.express as px
import branca.colormap as cm
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df['Neighborhood'].unique()
exterior_distribution = df.groupby(['Year_Built', 'Exterior_1st']).size().reset_index(name='Count')
exterior_distribution
df['Exterior_1st'].value_counts()
num_exterior = df.groupby('Exterior_1st',as_index=False).agg(n=('Exterior_1st','count')).sort_values('n',ascending=False)

desc_order = [i for i in num_exterior['Exterior_1st']] 
fig = px.histogram(df, x='Year_Built', color='Exterior_1st',
                   title="연도별 외강재 소재 분포",
                   labels={"Exterior_1st":"외강재 소재"},
                   category_orders={"Exterior_1st": desc_order},
                   barmode='stack')
fig.update_xaxes(dtick=1)


color_map = {ext: 'gray' if ext in desc_order[7:] else px.colors.qualitative.Plotly[i] for i, ext in enumerate(desc_order)}

df['color'] = df['Exterior_1st'].apply(lambda x: color_map.get(x))

fig = px.histogram(df, x='Year_Built', color='Exterior_1st',
                   title="연도별 전체 TOP7",
                   labels={"Exterior_1st":"외장재 소재"},
                   category_orders={"Exterior_1st": desc_order},
                   barmode='stack',
                   color_discrete_map=color_map)

fig.update_xaxes(dtick=1)

import branca.colormap as cm
import webbrowser
from folium.features import DivIcon

map_house = folium.Map(location=[42.034482,-93.642897],zoom_start=13,tiles='cartodbpositron')

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

colormap = cm.StepColormap(
    colors=list(color_map.values()),
    caption="Color Legend"
)
colormap.add_to(map_house)
map_house.save('map_house.html')



# 10년 단위로 데이터 그룹화
df['Decade'] = (df['Year_Built'] // 10) * 10
decade_grouped = df.groupby(['Decade', 'Exterior_1st']).size().reset_index(name='count')

# 바 플롯 생성
fig = px.bar(decade_grouped, x='Decade', y='count', color='Exterior_1st',
             title="10년 단위 TOP 외장재",
             labels={"Exterior_1st": "외장재 소재"},
             category_orders={"Exterior_1st": desc_order},
             color_discrete_map=color_map)
fig.show()

## 1990년대, 2000년대 지도 시각화


df2 = df.query("Decade in [1990]")
df2 = df2.reset_index(drop=True)
import folium
map_house2 = folium.Map(location=[42.034482,-93.642897],zoom_start=13,tiles='cartodbpositron')

for i in range(len(df2['Longitude'])):
    folium.CircleMarker(
        [df2['Latitude'][i], df2['Longitude'][i]],
        popup=f"위도: {df2['Latitude'][i]}, 경도: {df2['Longitude'][i]}, Price: ${df2['Sale_Price'][i]}",
        radius=df2['Sale_Price'][i]/100000,
        color=df2['color'][i],
        fill=True,
        fill_color=df2['color'][i],
        fill_opacity=0.7
    ).add_to(map_house2)

colormap = cm.StepColormap(
    colors=list(color_map.values()),
    caption="Color Legend"
)
colormap.add_to(map_house2)
map_house2.save('1990.html')



df3 = df.query("Decade in [2000]")
df3 = df3.reset_index(drop=True)
import folium
map_house3 = folium.Map(location=[42.034482,-93.642897],zoom_start=13,tiles='cartodbpositron')

for i in range(len(df3['Longitude'])):
    folium.CircleMarker(
        [df3['Latitude'][i], df3['Longitude'][i]],
        popup=f"위도: {df3['Latitude'][i]}, 경도: {df3['Longitude'][i]}, Price: ${df2['Sale_Price'][i]}",
        radius=df2['Sale_Price'][i]/100000,
        color=df2['color'][i],
        fill=True,
        fill_color=df3['color'][i],
        fill_opacity=0.7
    ).add_to(map_house3)

colormap = cm.StepColormap(
    colors=list(color_map.values()),
    caption="Color Legend"
)
colormap.add_to(map_house3)
map_house3.save('2000.html')

import webbrowser

webbrowser.open_new('map_house.html')
webbrowser.open_new('1990.html')
webbrowser.open_new('2000.html')