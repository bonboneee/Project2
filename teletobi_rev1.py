import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.spatial import ConvexHull
import webbrowser

# 데이터 로드 및 전처리
df = pd.read_csv('data/houseprice-with-lonlat.csv')
df = df.rename(columns={'Unnamed: 0':'Id'})
df

# Exterior 1st와 2nd 개수 비교(5위까지 순위 같음, 1st기준 분석시작)
exteriors = set(df['Exterior_1st'].unique()) | set(df['Exterior_2nd'].unique())
Exterior_all = pd.DataFrame()
Exterior_all['Exterior'] = sorted(list(exteriors))

first = df.groupby(['Exterior_1st'], as_index=False).agg(first=('Exterior_1st', 'count'))
second = df.groupby(['Exterior_2nd'], as_index=False).agg(second=('Exterior_2nd', 'count'))
first.columns = ['Exterior', 'Exterior_1st']
second.columns = ['Exterior', 'Exterior_2nd']
Exterior_all = pd.merge(Exterior_all, first, on='Exterior', how='left')
Exterior_all = pd.merge(Exterior_all, second, on='Exterior', how='left')
Exterior_all = Exterior_all.sort_values(['Exterior_1st', 'Exterior_1st'], ascending=False)
Exterior_all.reset_index(drop=True, inplace=True)
Exterior_all

# 1~6위 순위 같으므로 Exterior 1st 로 분석 시작
exterior = df.groupby('Exterior_1st',as_index=False).agg(count=('Exterior_1st','count')).sort_values('count',ascending=False)['Exterior_1st'].reset_index(drop=True)
exterior = list(exterior)

# Exterior 1st 연도별 막대그래프 확인
year_grouped = df.groupby(['Year_Built','Exterior_1st'],as_index=False).agg(count = ('Exterior_1st','count'))

fig = px.bar(year_grouped, x="Year_Built", y="count", color="Exterior_1st",
             labels={"Exterior_1st": "Exterior"},
             category_orders={"Exterior_1st": exterior})
fig.update_xaxes(dtick=1,title_text='')
fig.update_yaxes(title_text='')
fig.update_layout(
    plot_bgcolor='#f9f6f1',  # 배경색 변경
    xaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # x축 그리드 색상 변경
    yaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # y축 그리드 색상 변경
    legend=dict(
        font=dict(
            size=12  # 범례 텍스트 크기를 10으로 설정
        ),
        y=1.2,  # 범례의 y 위치를 상단으로 설정 (1이 위)
        yanchor="top",  # y 위치의 기준을 상단으로 설정
        x=0.5,  # 범례의 x 위치를 중앙으로 설정 (0이 왼쪽, 1이 오른쪽)
        xanchor="center",  # x 위치의 기준을 중앙으로 설정
        orientation="h",  # 범례를 수평으로 배치
        
    ),
    legend_title=dict(text='Exterior',
                        font=dict(
                            size=12,  # 제목의 크기 설정
                            color="black",  # 제목의 색상 설정
                            family="Arial",  # 폰트 설정
                            weight="bold"  # 굵게 표시
    )),
)

fig.write_html("graph/year_exterior.html")

# TOP6 제외 색상 회색으로 변경
palette_exterior = ["#FF6F61", "#6F9FD8", "#F7C94C", "#6DBE45", "#FF8C00","#4DB6AC"] + ["#D3D3D3"] * 10
exteriors_color = {ext: color for ext, color in zip(exterior, palette_exterior)}

fig = px.bar(year_grouped, x="Year_Built", y="count", color="Exterior_1st",
             labels={"Exterior_1st": "Exterior"},
             category_orders={"Exterior_1st": exterior},
             color_discrete_map=exteriors_color)
fig.update_xaxes(dtick=1,title_text='')
fig.update_yaxes(title_text='')
fig.update_layout(
    plot_bgcolor='#f9f6f1',  # 배경색 변경
    xaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # x축 그리드 색상 변경
    yaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # y축 그리드 색상 변경
    legend=dict(
        font=dict(
            size=12  # 범례 텍스트 크기를 10으로 설정
        ),
        y=1.2,  # 범례의 y 위치를 상단으로 설정 (1이 위)
        yanchor="top",  # y 위치의 기준을 상단으로 설정
        x=0.5,  # 범례의 x 위치를 중앙으로 설정 (0이 왼쪽, 1이 오른쪽)
        xanchor="center",  # x 위치의 기준을 중앙으로 설정
        orientation="h",  # 범례를 수평으로 배치
        
    ),
    legend_title=dict(text='Exterior',
                        font=dict(
                            size=12,  # 제목의 크기 설정
                            color="black",  # 제목의 색상 설정
                            family="Arial",  # 폰트 설정
                            weight="bold"  # 굵게 표시
    )),
)

fig.write_html("graph/year_exterior_gray.html")


# 10년 단위로 데이터 그룹화
df['Decade'] = (df['Year_Built'] // 10) * 10
df.groupby(['Decade', 'Exterior_1st'],as_index=False).agg(count=('Exterior_1st','count')).sort_values(['Decade','count'],ascending=False).head(20)

decade_grouped = df.groupby(['Decade', 'Exterior_1st']).agg(count=('Exterior_1st', 'count')).reset_index()
decade_grouped['Decade_Label'] = decade_grouped['Decade'].astype(str) + 's'
decade_grouped.query('Decade == 2000').sort_values('count', ascending=False)

fig = px.bar(decade_grouped, x='Decade', y='count', color='Exterior_1st',
             labels={"Exterior_1st": "Exterior"},
             category_orders={"Exterior_1st": exterior},
             color_discrete_map=exteriors_color)

fig.update_xaxes(dtick=10,    tickvals=decade_grouped['Decade'].unique(),
    ticktext=decade_grouped['Decade_Label'].unique(),
    title_text='')
fig.update_yaxes(title_text='')
fig.update_layout(
    plot_bgcolor='#f9f6f1',  # 배경색 변경
    xaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # x축 그리드 색상 변경
    yaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # y축 그리드 색상 변경
    legend=dict(
        font=dict(
            size=12  # 범례 텍스트 크기를 10으로 설정
        ),
        y=1.2,  # 범례의 y 위치를 상단으로 설정 (1이 위)
        yanchor="top",  # y 위치의 기준을 상단으로 설정
        x=0.5,  # 범례의 x 위치를 중앙으로 설정 (0이 왼쪽, 1이 오른쪽)
        xanchor="center",  # x 위치의 기준을 중앙으로 설정
        orientation="h",  # 범례를 수평으로 배치
        
    ),
    legend_title=dict(text='Exterior',
                        font=dict(
                            size=12,  # 제목의 크기 설정
                            color="black",  # 제목의 색상 설정
                            family="Arial",  # 폰트 설정
                            weight="bold"  # 굵게 표시
    )),
)


fig.write_html("graph/decade_exterior.html")

# 선그래프 생성
fig = px.line(decade_grouped, x='Decade', y='count', color='Exterior_1st',
             labels={"Exterior_1st": "Exterior"},
             category_orders={"Exterior_1st": exterior},
             color_discrete_map=exteriors_color)

fig.update_xaxes(dtick=10, tickvals=decade_grouped['Decade'].unique(),
    ticktext=decade_grouped['Decade_Label'].unique(),
    title_text='')
fig.update_yaxes(title_text='')

fig.update_layout(
    plot_bgcolor='#f9f6f1',  # 배경색 변경
    xaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # x축 그리드 색상 변경
    yaxis=dict(showgrid=True, gridcolor='#d3cbb8'),  # y축 그리드 색상 변경
    legend=dict(
        font=dict(
            size=12  # 범례 텍스트 크기를 10으로 설정
        ),
        y=1.2,  # 범례의 y 위치를 상단으로 설정 (1이 위)
        yanchor="top",  # y 위치의 기준을 상단으로 설정
        x=0.5,  # 범례의 x 위치를 중앙으로 설정 (0이 왼쪽, 1이 오른쪽)
        xanchor="center",  # x 위치의 기준을 중앙으로 설정
        orientation="h",  # 범례를 수평으로 배치
        
    ),
    legend_title=dict(text='Exterior',
                        font=dict(
                            size=12,  # 제목의 크기 설정
                            color="black",  # 제목의 색상 설정
                            family="Arial",  # 폰트 설정
                            weight="bold"  # 굵게 표시
    )),
)

fig.write_html("graph/decade_exterior_line.html")

# 특정 년도대(10년단위) 외장재별 건축 수, 전년도대 수, 증감 
def count_built(decade, exterior):
    if exterior == "all":
        that_decade = decade_grouped.query(f'Decade == {decade}')['count'].sum()
        last_decade = decade_grouped.query(f'Decade == {decade-10}')['count'].sum()
    else:
        that_decade = decade_grouped.query(f'Decade == {decade} & Exterior_1st == "{exterior}"')['count']
        last_decade = decade_grouped.query(f'Decade == {decade-10} & Exterior_1st == "{exterior}"')['count']
        
        that_decade = that_decade.sum() if not that_decade.empty else 0
        last_decade = last_decade.sum() if not last_decade.empty else 0
    
    return that_decade, last_decade, that_decade - last_decade

count_built(2000, "all") # (np.int64(780), np.int64(334), np.int64(446))
count_built(2000, "VinylSd") # (np.int64(645), np.int64(185), np.int64(460))
count_built(2000, "MetalSd") # (np.int64(645), np.int64(185), np.int64(460))
count_built(2000, "HdBoard") # (np.int64(3), np.int64(86), np.int64(-83))
count_built(2000, "CemntBd") # (np.int64(64), np.int64(7), np.int64(57))

# 10년단위 연도별 외장재별 동네별 건물수
exterior_nhbh = df.query('Decade == 2000').groupby(['Exterior_1st', 'Neighborhood'], as_index=False).agg(count=('Exterior_1st','count')).sort_values('count', ascending=False)
exterior_nhbh.query('Exterior_1st == "VinylSd"').head(5)
exterior_nhbh.query('Exterior_1st == "MetalSd"').head(5)
exterior_nhbh.query('Exterior_1st == "HdBoard"').head(5)
exterior_nhbh.query('Exterior_1st == "CemntBd"').head(5)

# 연도별 외장재 분포 현황 지도 (1111입력시 전체년도)
def creat_map(decade):

    # Plotly의 기본 객체 생성
    fig = go.Figure()

    # 지도에 집 표시(외장재별 색 다르게 선택)
    for ext in exterior:
        if(decade == 1111):
            filtered_df = df[df['Exterior_1st'] == ext ]
        else:
            filtered_df = df[ (df['Exterior_1st'] ==  ext ) & (df['Decade'] == decade )]
        
        # hovertext에 위도, 경도, 가격을 추가
        hover_text = (
            "Exterior: " + filtered_df['Exterior_1st'].astype(str) +
            "<br>Latitude: " + filtered_df['Latitude'].astype(str) +
            "<br>Longitude: " + filtered_df['Longitude'].astype(str) +
            "<br>Price: $" + filtered_df['Sale_Price'].astype(str)
        )        
        
        fig.add_trace(go.Scattermapbox(
            lat=filtered_df['Latitude'],
            lon=filtered_df['Longitude'],
            mode='markers',
            marker=dict(color=exteriors_color[ext]),
            hovertext=hover_text,
            hoverinfo='text',
            name=ext,  # 각 트레이스에 고유한 이름을 부여
            showlegend=True  # 범례에 표시
        ))
       
    # Neighborhood 선으로 표시
    sorted_neighborhoods = sorted(df['Neighborhood'].unique())

    # Neighborhood 선을 구하기 위해 위도, 경도를 동네별로 분류
    nhbh_individuals = {i: [] for i in df['Neighborhood']}

    for nhbh, lat, lon in zip(df['Neighborhood'], df['Latitude'], df['Longitude']):
        nhbh_individuals[nhbh].append([lat, lon])

    for nhbh in sorted_neighborhoods:
        points = np.array(nhbh_individuals[nhbh])
        
        # 여러 점이 있을때 가장 밖의 점들을 구해주는 패키지 사용
        if len(points) >= 3:
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
            hull_points = np.vstack([hull_points, hull_points[0]])  # 다각형을 닫기 위해 첫 번째 점을 다시 추가

            # 폴리곤 선 추가 (범례에 표시되지 않음)
            fig.add_trace(go.Scattermapbox(
                lat=hull_points[:, 0],
                lon=hull_points[:, 1],
                mode='lines',
                line=dict(color="gray", width=2),
                hovertext= nhbh,
                hoverinfo='text',
                showlegend=False  # 범례에 표시하지 않음
            ))

            # 폴리곤 중심에 텍스트 레이블 추가 (범례에 표시되지 않음)
            centroid_lat = np.mean(hull_points[:, 0])
            centroid_lon = np.mean(hull_points[:, 1])

            fig.add_trace(go.Scattermapbox(
                lat=[centroid_lat],
                lon=[centroid_lon],
                mode='text',
                text=[nhbh],
                textposition="middle center",
                showlegend=False  # 범례에 표시하지 않음
            ))

        elif len(points) == 2:
            fig.add_trace(go.Scattermapbox(
                lat=points[:, 0],
                lon=points[:, 1],
                mode='lines+markers',
                line=dict(color="gray"),
                hovertext= nhbh,
                hoverinfo='text',
                showlegend=False  # 범례에 표시하지 않음
            ))

        elif len(points) == 1:
            fig.add_trace(go.Scattermapbox(
                lat=[points[0][0]],
                lon=[points[0][1]],
                mode='markers',
                marker=dict(color="gray"),
                hovertext= nhbh,
                hoverinfo='text',
                showlegend=False  # 범례에 표시하지 않음
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
                size=12  # 범례 텍스트 크기를 10으로 설정
            ),
            y=1,  # 범례의 y 위치를 상단으로 설정 (1이 위)
            yanchor="top",  # y 위치의 기준을 상단으로 설정
            x=0.5,  # 범례의 x 위치를 중앙으로 설정 (0이 왼쪽, 1이 오른쪽)
            xanchor="center",  # x 위치의 기준을 중앙으로 설정
            orientation="h",  # 범례를 수평으로 배치
           
        ),
        legend_title=dict(text='Exterior',
                          font=dict(
                                size=12,  # 제목의 크기 설정
                                color="black",  # 제목의 색상 설정
                                family="Arial",  # 폰트 설정
                                weight="bold"  # 굵게 표시
        )),
    )
    
    return fig.write_html("graph/map_exterior_"+str(decade)+".html")


creat_map(1111)
creat_map(2000)

