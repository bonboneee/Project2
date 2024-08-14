import pandas as pd
import webbrowser
import folium
import seaborn as sns
# !pip install folium branca matplotlib
import branca.colormap as cm
import matplotlib.cm as mpl_cm
import matplotlib.colors as mcolors

df = pd.read_csv('data/houseprice-with-lonlat.csv')
df['Neighborhood'].unique()

df[['Longitude', 'Latitude']].mean()
df[['Longitude', 'Latitude']].min()
df[['Longitude', 'Latitude']].max()

map_house = folium.Map(location=[42.034482,-93.642897 ],
                       zoom_start=13,
                       tiles='cartodbpositron')
N_array = df['Neighborhood'].unique()
palette = sns.color_palette("viridis", len(N_array)).as_hex()
N_dict = { N:color for N,color in zip(N_array, palette)}


for i in range(len(df['Longitude'])):
    folium.CircleMarker([df['Latitude'][i], df['Longitude'][i]],
                        popup=f"위도: {df['Latitude'][i]}, 경도: {df['Longitude'][i]}, Price: ${df['Sale_Price'][i]}",
                        radius=df['Sale_Price'][i]/100000,
                        color=N_dict.get(df['Neighborhood'][i]),
                        fill = True,
                        fill_color= N_dict.get(df['Neighborhood'][i]),
                        fill_opacity=0.7
                        ).add_to(map_house)
# 범례 생성
colormap = cm.LinearColormap(palette , vmin=0, vmax=len(N_array)-1, caption="Color Legend")
colormap.add_to(map_house)

map_house.save('map_house.html')
webbrowser.open_new('map_house.html')

house_train = pd.read_csv("posts/house_price/train.csv")
house_train.info()

import pandas as pd
import matplotlib.pyplot as plt
    
# pairplot
df = house_train[['SalePrice', 'YearBuilt', 'LotFrontage', 'LotArea', 'OverallQual', \
                 'MasVnrArea', 'BsmtQual', 'TotalBsmtSF', 'GrLivArea', 'FullBath', \
                 'TotRmsAbvGrd', 'GarageArea', 'PoolArea']]
df
plt.figure(figsize=(12, 10))
sns.pairplot(df, plot_kws={'s': 5})
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
plt.show()
plt.clf()

# 위도: 42.022745, 경도: -93.577427, 
# 위도: 42.022745, 경도: -93.6928668, 

# 위도: 42.063342, 경도: -93.644366, Price: $173500
# 위도: 41.986502, 경도: -93.644366, Price: $143000


