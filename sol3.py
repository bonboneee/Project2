import pandas as pd
import numpy as np
import folium
import webbrowser
from scipy.spatial import ConvexHull

df = pd.read_csv('data/houseprice-with-lonlat.csv')
df = df.rename(columns={'Unnamed: 0':'Id'})

df.groupby('Neighborhood').agg(n=('Neighborhood','count')).sort_values('n')


nhbh_individuals={i :[]for i in df['Neighborhood']}
len(nhbh_individuals.keys())

for nhbh,lat,long in zip(df['Neighborhood'],df['Latitude'], df['Longitude']):
    nhbh_individuals[nhbh].append([lat,long])
nhbh_individuals

test1 = folium.Map(location=[42.034482,-93.642897 ],
                       zoom_start=13,
                       tiles='cartodbpositron')
                       
palette_28 = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1",
    "#955251", "#B565A7", "#009B77", "#DD4124", "#D65076",
    "#45B8AC", "#EFC050", "#5B5EA6", "#9B2335", "#DFCFBE",
    "#55B4B0", "#E15D44", "#7FCDCD", "#BC243C", "#C3447A",
    "#98B4D4", "#C1C6C8", "#F7786B", "#34B3F1", "#FFD662",
    "#CE3175", "#6C4F3D", "#BDC3C7", "#935116"]

nhbh_color = { nhbh:color for nhbh,color in zip(nhbh_individuals.keys(), palette_28)}

for i in range(len(df['Longitude'])):
    folium.CircleMarker([df['Latitude'][i], df['Longitude'][i]],
                        popup=df['Neighborhood'][i],
                        radius=3,
                        color=nhbh_color.get(df['Neighborhood'][i]),
                        ).add_to(test1)


# CSS 스타일 정의: 배경색은 검은색(#000000), 글자색은 노란색(#FFFF00)
custom_tooltip_style = """
    <style>
        .custom-tooltip {
            background-color: #000000;  /* 배경색: 검은색 */
            color: #FFFF00;  /* 글자색: 노란색 */
            padding: 5px;
            border-radius: 5px;
        }
    </style>
"""

# Folium 지도 생성 및 각 동네에 대한 Polygon 추가
for nhbh in nhbh_individuals.keys():
    points = np.array(nhbh_individuals[nhbh])  # points를 NumPy 배열로 변환
    
    # HTML + CSS로 툴팁 설정
    tooltip_html = f"""
    {custom_tooltip_style}
    <div class='custom-tooltip'>{nhbh}</div>
    """
    
    if len(points) >= 3:
        hull = ConvexHull(points)
        hull_points = points[hull.vertices].tolist()  # NumPy 배열을 리스트로 변환하여 folium에 전달
        folium.Polygon(locations=hull_points, color=nhbh_color.get(nhbh), tooltip=tooltip_html).add_to(test1)
    elif len(points) == 2:
        folium.PolyLine(locations=points.tolist(), color=nhbh_color.get(nhbh), tooltip=tooltip_html).add_to(test1)
    elif len(points) == 1:
        folium.CircleMarker(location=points[0], radius=3, color=nhbh_color.get(nhbh), tooltip=tooltip_html).add_to(test1)

# 결과물 저장 및 표시
test1.save('test1.html')
webbrowser.open_new('test1.html')





##########################
import pandas as pd
import plotly.express as px

# 데이터 로드 및 전처리
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df = df.rename(columns={'Unnamed: 0':'Id'})

# Plotly로 지도 시각화
fig = px.scatter_mapbox(df, 
                        lat="Latitude", 
                        lon="Longitude", 
                        color="Neighborhood",  # 범례를 Neighborhood로 설정
                        hover_name="Neighborhood",  # 마우스 오버 시 동네 이름 표시
                        zoom=13,
                        height=600,
                        color_discrete_sequence=palette_28)  # 정의된 색상 팔레트 사용

# Mapbox 스타일 설정 (OpenStreetMap 스타일 사용)
fig.update_layout(mapbox_style="carto-positron")

# 레이아웃 업데이트 (기타 설정)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# 결과물 표시
fig.show()

##################################



import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull

# 데이터 로드 및 전처리
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df = df.rename(columns={'Unnamed: 0':'Id'})

# 색상 팔레트 정의
palette_28 = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1",
    "#955251", "#B565A7", "#009B77", "#DD4124", "#D65076",
    "#45B8AC", "#EFC050", "#5B5EA6", "#9B2335", "#DFCFBE",
    "#55B4B0", "#E15D44", "#7FCDCD", "#BC243C", "#C3447A",
    "#98B4D4", "#C1C6C8", "#F7786B", "#34B3F1", "#FFD662",
    "#CE3175", "#6C4F3D", "#BDC3C7", "#935116"]

nhbh_individuals = {i: [] for i in df['Neighborhood']}
nhbh_color = {nhbh: color for nhbh, color in zip(nhbh_individuals.keys(), palette_28)}

# 각 동네의 점들 그룹화
for nhbh, lat, lon in zip(df['Neighborhood'], df['Latitude'], df['Longitude']):
    nhbh_individuals[nhbh].append([lat, lon])

# Plotly의 기본 객체 생성
fig = go.Figure()

# 각 동네에 대해 Convex Hull 계산 및 Polygon 추가
for nhbh in nhbh_individuals.keys():
    points = np.array(nhbh_individuals[nhbh])
    
    if len(points) >= 3:
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]
        hull_points = np.vstack([hull_points, hull_points[0]])  # 다각형을 닫기 위해 첫 번째 점을 다시 추가

        # rgba() 형식으로 색상 지정
        fill_color_rgba = f"rgba({int(nhbh_color[nhbh][1:3], 16)}, {int(nhbh_color[nhbh][3:5], 16)}, {int(nhbh_color[nhbh][5:7], 16)}, 0.6)"
        
        fig.add_trace(go.Scattermapbox(
            lat=hull_points[:, 0],
            lon=hull_points[:, 1],
            mode='lines',
            fill='toself',
            fillcolor=fill_color_rgba,  # 다각형의 투명도 설정
            line=dict(color=nhbh_color[nhbh]),
            name=nhbh
        ))
    
    elif len(points) == 2:
        fig.add_trace(go.Scattermapbox(
            lat=points[:, 0],
            lon=points[:, 1],
            mode='lines+markers',
            line=dict(color=nhbh_color[nhbh]),
            name=nhbh
        ))

    elif len(points) == 1:
        fig.add_trace(go.Scattermapbox(
            lat=[points[0][0]],
            lon=[points[0][1]],
            mode='markers',
            marker=dict(color=nhbh_color[nhbh]),
            name=nhbh
        ))

# Mapbox 스타일 설정
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(
        center=go.layout.mapbox.Center(lat=42.034482, lon=-93.642897),
        zoom=13
    ),
    margin={"r":0,"t":0,"l":0,"b":0}
)

# 결과물 표시
fig.show()

##############################


import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull
import webbrowser

# 데이터 로드 및 전처리
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df = df.rename(columns={'Unnamed: 0':'Id'})

# 색상 팔레트 정의
palette_28 = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1",
    "#955251", "#B565A7", "#009B77", "#DD4124", "#D65076",
    "#45B8AC", "#EFC050", "#5B5EA6", "#9B2335", "#DFCFBE",
    "#55B4B0", "#E15D44", "#7FCDCD", "#BC243C", "#C3447A",
    "#98B4D4", "#C1C6C8", "#F7786B", "#34B3F1", "#FFD662",
    "#CE3175", "#6C4F3D", "#BDC3C7", "#935116"]

nhbh_individuals = {i: [] for i in df['Neighborhood']}
nhbh_color = {nhbh: color for nhbh, color in zip(nhbh_individuals.keys(), palette_28)}

# 각 동네의 점들 그룹화
for nhbh, lat, lon in zip(df['Neighborhood'], df['Latitude'], df['Longitude']):
    nhbh_individuals[nhbh].append([lat, lon])

# Plotly의 기본 객체 생성
fig = go.Figure()

# 각 동네에 대해 Convex Hull 계산 및 Polygon 추가
for nhbh in nhbh_individuals.keys():
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
        zoom=13
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        font=dict(
            size=10  # 범례 텍스트 크기를 10으로 설정
        )
    )
)

# 결과물 표시
fig.show()

fig.write_html("file.html")
webbrowser.open_new('file.html')