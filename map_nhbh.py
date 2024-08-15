import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull
import webbrowser

# ConvexHull과 같은 복잡한 처리를 위해 px대신 go사용

# 데이터 로드 및 전처리
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df = df.rename(columns={'Unnamed: 0':'Id'})

def creat_map(color_list, color_list_name):
    # 색상 팔레트 정의
    palette_nhbh = color_list

    # 동네 이름을 정렬
    sorted_neighborhoods = sorted(df['Neighborhood'].unique())

    nhbh_individuals = {i: [] for i in df['Neighborhood']}
    nhbh_color = {nhbh: color for nhbh, color in zip(nhbh_individuals.keys(), palette_nhbh)}

    # 각 동네의 점들 그룹화
    for nhbh, lat, lon in zip(df['Neighborhood'], df['Latitude'], df['Longitude']):
        nhbh_individuals[nhbh].append([lat, lon])

    # Plotly의 기본 객체 생성
    fig = go.Figure()

    # 각 동네에 대해 Convex Hull 계산 및 Polygon 추가
    for nhbh in sorted_neighborhoods:
        points = np.array(nhbh_individuals[nhbh])
        
        if len(points) >= 3:
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
            hull_points = np.vstack([hull_points, hull_points[0]])  # 다각형을 닫기 위해 첫 번째 점을 다시 추가

            fig.add_trace(go.Scattermapbox(
                lat=hull_points[:, 0],
                lon=hull_points[:, 1],
                mode='lines',  # 테두리만 그리기 위해 'lines' 모드 사용
                line=dict(color=nhbh_color[nhbh], width=2),
                hovertext=nhbh,
                hoverinfo='text',
                name=nhbh
            ))
        
        elif len(points) == 2:
            fig.add_trace(go.Scattermapbox(
                lat=points[:, 0],
                lon=points[:, 1],
                mode='lines+markers',
                line=dict(color=nhbh_color[nhbh]),
                hovertext=nhbh,
                hoverinfo='text',
                name=nhbh
            ))

        elif len(points) == 1:
            fig.add_trace(go.Scattermapbox(
                lat=[points[0][0]],
                lon=[points[0][1]],
                mode='markers',
                marker=dict(color=nhbh_color[nhbh]),
                hovertext=nhbh,
                hoverinfo='text',
                name=nhbh
            ))

    # Mapbox 스타일 설정
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            center=go.layout.mapbox.Center(lat=42.034482, lon=-93.642897),
            zoom=12
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            font=dict(
                size=10  # 범례 텍스트 크기를 10으로 설정
            )
        ),
        legend_title=dict(text='Neighborhood',
                          font=dict(
                                size=12,  # 제목의 크기 설정
                                color="black",  # 제목의 색상 설정
                                family="Arial",  # 폰트 설정
                                weight="bold"  # 굵게 표시
        )),
    )
    fig.write_html("map_nhbh_"+color_list_name+".html")
    return webbrowser.open_new("map_nhbh_"+color_list_name+".html")

len(df['Neighborhood'].value_counts())

colorful = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1",
    "#955251", "#B565A7", "#009B77", "#DD4124", "#D65076",
    "#45B8AC", "#EFC050", "#5B5EA6", "#9B2335", "#DFCFBE",
    "#55B4B0", "#E15D44", "#7FCDCD", "#BC243C", "#C3447A",
    "#98B4D4", "#C1C6C8", "#F7786B", "#34B3F1", "#FFD662",
    "#CE3175", "#6C4F3D", "#BDC3C7", "#935116"]

creat_map(colorful,"colorful")

all_gray = ['gray']*28
creat_map(all_gray,"all_gray")


##############
# Exterior 1st와 2nd 개수 비교(5위까지 순위 같음, 1st기준 분석시작)

df.columns
exteriors = set(df['Exterior_1st'].unique()) | set(df['Exterior_2nd'].unique())
len(exteriors)

first = df.groupby(['Exterior_1st'],as_index=False).agg(first = ('Exterior_1st','count'))
second = df.groupby(['Exterior_2nd'],as_index=False).agg(second = ('Exterior_2nd','count'))

Exterior_all = pd.DataFrame()
Exterior_all
Exterior_all['Exterior'] = sorted(list(exteriors))
Exterior_all
# left join 수행
Exterior = pd.merge(Exterior_all, first, on='key', how='left')

# NaN 값을 0으로 채우기
result = result.fillna(0)

print(result)










first
first = first.sort_values('Exterior_1st')
first.reset_index(drop=True, inplace=True)
first.columns = ['Exterior','first']
second.columns = ['Exterior','second']
second
Exterior = pd.merge(first,second,on='Exterior')
Exterior = Exterior.sort_values('first',ascending=False)
Exterior.reset_index(drop=True, inplace=True)
Exterior.sum()

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
                lat=points[:, 0],
                lon=points[:, 1],
                mode='lines+markers',
                line=dict(color=nhbh_color[nhbh]),
                hovertext=nhbh,
                hoverinfo='text',
                name=nhbh
            ))

palette_exterior_top5 = 

Exterior
colors = 


{"VinylSd" : }
[
'#FF6F61',  # VinylSd
'#6F9FD8',  # MetalSd
'#F7C94C',  # HdBoard
'#6DBE45',  # Wd Sdng
'#FF8C00',  # Plywood
'#4DB6AC',  # CemntBd
'#9B59B6',  # BrkFace
] + ['#D3D3D3'] * (len(exterior_distribution['Exterior_1st'].unique()) - 7)  # 나머지 색상은 회색으로 설정







코랄 핑크 (Coral Pink): #FF6F61
페일 옐로우 (Pale Yellow): #FFD662
소프트 블루 (Soft Blue): #92A8D1
민트 그린 (Mint Green): #88B04B
라벤더 퍼플 (Lavender Purple): #B565A