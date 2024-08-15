import pandas as pd
import plotly.graph_objs as go
import numpy as np
from scipy.spatial import ConvexHull
import webbrowser

# 데이터 로드 및 전처리
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df = df.rename(columns={'Unnamed: 0':'Id'})

# Exterior 1st와 2nd 개수 비교(5위까지 순위 같음, 1st기준 분석시작)
exteriors = set(df['Exterior_1st'].unique()) | set(df['Exterior_2nd'].unique())
Exterior_all = pd.DataFrame()
Exterior_all['Exterior'] = sorted(list(exteriors))
first = df.groupby(['Exterior_1st'], as_index=False).agg(first=('Exterior_1st', 'count'))
second = df.groupby(['Exterior_2nd'], as_index=False).agg(second=('Exterior_2nd', 'count'))
first.columns = ['Exterior', 'Exterior_1st']
second.columns = ['Exterior', 'Exterior_2nd']

# left join 수행
Exterior_all = pd.merge(Exterior_all, first, on='Exterior', how='left')
Exterior_all = pd.merge(Exterior_all, second, on='Exterior', how='left')
Exterior_all = Exterior_all.sort_values(['Exterior_1st', 'Exterior_1st'], ascending=False)
Exterior_all.reset_index(drop=True, inplace=True)

palette_exterior = ["#FF6F61", "#6F9FD8", "#F7C94C", "#6DBE45", "#FF8C00"] + ["#D3D3D3"] * 11
exterior = Exterior_all.dropna(subset=['Exterior_1st'])['Exterior']
exteriors_color = {ext: color for ext, color in zip(exterior, palette_exterior)}

# Plotly의 기본 객체 생성
fig = go.Figure()

# Exterior 1st 트레이스 추가
for ext in exterior:
    filtered_df = df[df['Exterior_1st'] == ext]
    fig.add_trace(go.Scattermapbox(
        lat=filtered_df['Latitude'],
        lon=filtered_df['Longitude'],
        mode='markers',
        marker=dict(color=exteriors_color[ext], opacity=0.6),  # 투명도 설정
        hovertext=filtered_df['Exterior_1st'],
        hoverinfo='text',
        name=f'Exterior: {ext}',  # 각 트레이스에 고유한 이름을 부여
        showlegend=True  # 범례 표시
    ))

# Neighborhood 트레이스 추가
palette_nhbh = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1"] * 6
sorted_neighborhoods = sorted(df['Neighborhood'].unique())
nhbh_color = {nhbh: color for nhbh, color in zip(sorted_neighborhoods, palette_nhbh)}

for nhbh in sorted_neighborhoods:
    points = df[df['Neighborhood'] == nhbh][['Latitude', 'Longitude']].values
    if len(points) >= 3:
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]
        hull_points = np.vstack([hull_points, hull_points[0]])

        fig.add_trace(go.Scattermapbox(
            lat=hull_points[:, 0],
            lon=hull_points[:, 1],
            mode='lines',
            line=dict(color=nhbh_color[nhbh], width=2),
            hovertext=nhbh,
            hoverinfo='text',
            name=f'Neighborhood: {nhbh}',  # Neighborhood별로 트레이스 추가
            showlegend=True
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
    legend_title=dict(text='Categories',
                      font=dict(
                          size=12,
                          color="black",
                          family="Arial",
                          weight="bold"
    )),
)

# 결과를 HTML 파일로 저장하고 브라우저에서 열기
fig.write_html("combined_map.html")
webbrowser.open_new("combined_map.html")
